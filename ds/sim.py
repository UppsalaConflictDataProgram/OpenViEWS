import argparse

import h5py
import json

import numpy as np
import pandas as pd

import pickle
import pysal

import sys
import os

from mpi4py import MPI
from spatial import spatial_lag, make_weight_name, make_weigth_path

import streamers

from models_sm import load_model

from utils import ( load_params, split, add_paths_to_jobs, make_data_subset, 
                    add_varsets_to_modeljobs, get_model_vars)

from transforms import apply_transform


def run_sim(df, start, end, sim, models=[], tsvars=[], spatvars=[], 
    transformvars=[], transformvars_post=[]):
    
    nunits = len(df.loc[start].index)
    tsstreams = [streamers.init_order(nunits, tsvar) for tsvar in tsvars]
    # Seed the streamers
    for stream in tsstreams:
        for value, streamer in zip(
            df.loc[start-1, 
            stream['name']].values, 
            stream['streamers']):
            streamer.seed(value)

    # load the weight matrices
    for sdict in spatvars:
        with open(sdict['path_weight'], 'rb') as p:
            w = pickle.load(p)
            #print(sdict['name'], "loaded", sdict['path_weight'])
        sdict.update({'w' : w})

    for t in range(start, end+1):

        for stream in tsstreams:
            update = streamers.tick(
                stream['streamers'], df.loc[t - 1, stream['var']].values)
            df.loc[t, stream['name']] = update

        for sdict in spatvars:
            update = pysal.lag_spatial(sdict['w'], df.loc[t, sdict['var']].values)
            df.loc[t, sdict['name']] = update

        for transform in transformvars:
            df = apply_transform(df, transform)

        for model in models:
            outputs,varnames = model.predict(sim=sim, data=df.ix[t])
            for output, varname in zip(outputs, varnames):
                    df.loc[t, varname] = output

        for transform in transformvars_post:
            df = apply_transform(df, transform)


    return df

def worker_sim(job):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    
    sim = job['sim']

    print(rank, "starting sim", sim, "for", job['name_source'])
    
    start = job['sim_start']
    end = job['sim_end']

    df = pd.read_hdf(job['path_input'])
    print(rank, "read", job['path_input'])

    outputvars = []
    models = []
    for jm in job['models']:
        model = load_model(jm)
        models.append(model)
        outputvars.append(model.outputvars)
    
    outputvars.append(job['outputvars_extra'])

    # flatten outputvars, which is list of lists, then drop duplicates
    outputvars = [item for sublist in outputvars for item in sublist]
    outputvars = list(set(outputvars))
    outputvars = sorted(outputvars)


    df = run_sim(df, start, end, sim, models, job['ts'], job['spatial'], 
        job['transforms'],
        job['transforms_post'])
    # Drop the first year, which is sim_start - 1 used only to init streamers
    df.drop(df.index.get_level_values(0).min(), inplace=True) 
    df[outputvars].to_hdf(job['path_output'], key='data')
    # for every sim0, store a non-subseted version with the complete state of the simdata as of the end of sim for debug purposes
    if sim == 0:
        path_sim0_allvars = job['path_output'].replace("sim0.hdf5", "sim0_allvars.hdf5")
        df.to_hdf(path_sim0_allvars, key='data')
        print("wrote", path_sim0_allvars)
    print(rank, "wrote", job['path_output'])

def make_jobs_sim(params, dir_data, dir_sim, dir_train, dir_spatial):
    nsim = params['nsim']
    sim_start = params['times']['sim_start']
    # include year before simstart to seed streamers
    sim_start_data = sim_start - 1
    sim_end = params['times']['sim_end']

    jobs_models = params['models']
    jobs_ts = params['ts']
    jobs_spatial = params['spatial']
    jobs_transforms = params['transforms']
    if 'transforms_post' in params.keys():
        jobs_transforms_post = params['transforms_post']
    else:
        jobs_transforms_post = []
    
    for job in jobs_spatial:
        job.update({'weight_name' : make_weight_name(job)})
        job.update({'path_weight' : make_weigth_path(job, dir_spatial)})

    try:
        outputvars_extra = params['outputvars_extra']
    except:
        outputvars_extra = []

    jobs_sim = []
    for sim in range(nsim):
        job = { 'sim' : sim,
                'name' : "sim" + str(sim),
                'sim_start' : sim_start,
                'sim_end' : sim_end,
                'ts' : jobs_ts,
                'spatial' : jobs_spatial,
                'transforms' : jobs_transforms,
                'transforms_post' : jobs_transforms_post,
                'models' : jobs_models,
                'outputvars_extra' : outputvars_extra}
        jobs_sim.append(job.copy())
    
    # Multiplies the joblist to each dataset    
    jobs_sim = add_paths_to_jobs(jobs_sim, dir_data, dir_sim)
    
    # Add paths to models for each dataset
    for job in jobs_sim:
        job.update({'dir_models' : dir_train + job['name_source'] + "/"})
    
    # Nested dicts are weird with .update()
    for job in jobs_sim:
        job_models = job['models']
        jms = []
        for jm in job_models:
            jm['path_output'] = job['dir_models'] + jm['name'] + ".hdf5"
            jms.append(jm.copy())
        job.update({'models' : jms})


    allvars = []
    for j in jobs_ts:
        allvars.append(j['var'])
        allvars.append(j['name'])
    for j in jobs_spatial:
        allvars.append(j['var'])
        allvars.append(j['name'])
    for j in jobs_transforms + jobs_transforms_post:
        try:
            allvars.append(j['var'])
            allvars.append(j['name'])
        except:
            #print("No 'var' or 'name' in", j)
            pass
        try:
            allvars.append(j['a'])
            allvars.append(j['b'])
            allvars.append(j['name'])
        except:
            #print("no 'a' 'b' or 'name' in ", j)
            pass
        try:
            for v in j['varlist']:
                allvars.append(v)
            allvars.append(j['name'])
        except:
            pass


    allvars += get_model_vars(add_varsets_to_modeljobs(jobs_models))
    allvars = list(set(allvars))

    # for job in jobs_sim:
    #     print("#"*80)
    #     print(json.dumps(job, indent=4, sort_keys=True))
    
    make_data_subset(allvars, sim_start_data, sim_end, dir_data, dir_sim)

    return jobs_sim

def main_sim():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch",   type=str, 
        help="temp directory in which to save data")

    args = parser.parse_args()
    dir_scratch = args.dir_scratch
    path_params = dir_scratch + "params.json"

    dir_data = dir_scratch + "data/"
    dir_sim = dir_scratch + "sim/"
    dir_train = dir_scratch + "train/"
    dir_spatial = dir_scratch + "spatial/"

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        params = load_params(path_params)
        jobs = make_jobs_sim(params, dir_data, dir_sim, dir_train, dir_spatial)
        jobs = split(jobs, size)
    else:
        jobs = None
    
    jobs = comm.scatter(jobs, root = 0)

    for job in jobs:
        worker_sim(job)

if __name__ == "__main__":
    main_sim()