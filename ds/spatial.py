import os
import sys
import json
import argparse
import pickle


import pandas as pd

from mpi4py import MPI

import pysal

from utils import (
    add_paths_to_jobs,
    load_params,
    make_jobs_merge,
    make_work_data,
    split,
    worker_merge,
    get_list_groupvars
    )

def make_weight_name(job):
    name = "_".join([job['srule'], str(job['first']), str(job['last'])])
    return name

def make_weigth_path(job, dir_spatial):
    path = dir_spatial + job['weight_name'] + ".p"
    return path

def make_shapefile_groupvar(groupvar):
    if groupvar=="pg_id":
        shapefile_groupvar="GID"
    elif groupvar=="country_id":
        shapefile_groupvar="ID"
    return shapefile_groupvar

def shape_to_weight(path_shp, path_weight, srule, first, last, groupvar,
    list_groupvars, rowstand=True):

    shapefile_groupvar = make_shapefile_groupvar(groupvar)


    if srule == 'r':
        w = pysal.rook_from_shapefile(path_shp, shapefile_groupvar)
    elif srule == 'q':
        w = pysal.queen_from_shapefile(path_shp, shapefile_groupvar)
    elif srule == 'b':
        wq = pysal.queen_from_shapefile(path_shp, shapefile_groupvar)
        wr = pysal.rook_from_shapefile(path_shp, shapefile_groupvar)
        w = pysal.w_difference(wq, wr, constrained = False)
    else:
        print("You passed an unsupported srule")
        raise NotImplementedError

    if rowstand:
        w.transform = 'r'

    # we only want weight matrix values for the groupvars in our data
    w = pysal.w_subset(w, list_groupvars)

    # if simple first order weights
    if first == last == 1:
        # simple first order weights
        pass

    # calculate higher order weights one by one and union to make higher order
    else:
        # first order
        w_ho = pysal.higher_order(w, first)

        for order in range(first+1, last+1):
            print("Computing:", str(order), "for srule", srule)
            w_this_order = pysal.higher_order(w, order)
            # first and higher
            w_ho = pysal.w_union(w_ho, w_this_order)
        w = w_ho

    return w


def worker_shape_to_weight(job, rank):
    print(rank, "starting weight job for", job['weight_name'])

    srule = job['srule']
    path_shp = job['path_shp']
    first = job['first']
    last = job['last']
    list_groupvars = job['list_groupvars']
    path_weight = job['path_weight']
    groupvar = job['groupvar']

    w = shape_to_weight(path_shp, path_weight, srule, first, last, groupvar, list_groupvars)

    with open(path_weight, 'wb') as p:
        pickle.dump(w, p)
        print("Wrote", path_weight)


def select_shapefile(params, dir_spatial_shapes):

    if params['data']['groupvar'] == "pg_id":
            filename_shp = "priogrid.shp"
            print("Data grouped by pg_id, shapefile is", filename_shp)

    elif params['data']['groupvar'] == "country_id":
        filename_shp = "country.shp"

    elif params['data']['groupvar'] == "gwno":
        filename_shp = "FAIL!"
        print("WARNING!")
    else:
        print("I don't have a shapefile for that groupvar ",
        params['data']['groupvar'])
        raise NotImplementedError

    path_shp = dir_spatial_shapes + filename_shp
    print("path_shp:", path_shp)
    return path_shp

def make_jobs_weights(jobs, dir_data, dir_spatial, path_shp, groupvar):
    """Returns a list of unique weight job dicts, such as q_1_2 or r_1_1"""
    list_groupvars = get_list_groupvars(dir_data)

    jobs_weights = []
    for job in jobs:
        job.update({'weight_name' : make_weight_name(job)})
        keys_weight = ['srule', 'first', 'last', 'weight_name']
        job_weight = {a:job[a] for a in keys_weight}
        job_weight['path_shp'] = path_shp
        job_weight['path_weight'] = make_weigth_path(job, dir_spatial)
        job_weight['groupvar'] = groupvar

        jobs_weights.append(job_weight.copy())

    # Drop duplicates from jobs_weights so we only compute each weight once
    # We don't care which variable to lag at this stage, only the rule and order
    # We do this by making the dict items into tuples (that are hashable, unlike dicts)
    # and the getting their set() and then to list.
    jobs_weights = [dict(t) for t in set([tuple(d.items()) for d in jobs_weights])]
    # add the list of list_groupvars after dropping duplicates because lists can't be hashed
    for job in jobs_weights:
        job.update({'list_groupvars' : list_groupvars})
    return jobs_weights

def spatial_lag_autosubset(y, w):
    """
    If the set of groupvars varies over time (like countries appearing and dissappearing)
    then we need a different weight matrix for each time period. This automaticall subsets the
    weight matrix based on the groupvars in the index of the current set of data (y)

    """

    list_groupvars = sorted(list(y.index.get_level_values(1)))
    w_subset = pysal.w_subset(w, list_groupvars)

    return(pysal.lag_spatial(w_subset, y))

def spatial_lag(y, w):
    """
    To be used in pandas.groupby.transform.
    This only switches w any y in pysal.lag_spatial.
    """
    return(pysal.lag_spatial(w, y))


def worker_spatial(job):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    df = pd.read_hdf(job['path_input'])
    print(rank, "read", job['path_input'])

    df = df[[job['var']]]
    df.sort_index(inplace=True)

    with open(job['path_weight'], 'rb') as p:
        w = pickle.load(p)

    df[job['name']] = df.groupby(level=0)[job['var']].transform(spatial_lag_autosubset, w=w)
    # If missing fill with the variable being lagged,
    # So if no neighbours or missing neighbours just use own value for each cell
    df[job['name']].fillna(df[job['var']], inplace=True)

    df[[job['name']]].to_hdf(job['path_output'], key='data', mode='w')
    print(rank, "wrote", job['path_output'])

def main_spat():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch",   type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_data = dir_scratch + "data/"
    dir_spatial = dir_scratch + "spatial/"
    dir_spatial_shapes = dir_spatial + "shapes/"

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Use half the cores for mergin to keep mem within bounds
    size_half = int(size/4)
    if size_half==0:
        size_half=1

    # load jobs from json in the root process
    if rank==0:
        params = load_params(path_params)
        jobs = params['spatial']
        path_shp = select_shapefile(params, dir_spatial_shapes)
        groupvar = params['data']['groupvar']
        jobs_weights = make_jobs_weights(jobs, dir_data, dir_spatial, path_shp,
            groupvar)
        jobs_weights = split(jobs_weights, size)

    else:
        jobs_weights = None

    jobs_weights = comm.scatter(jobs_weights, root=0)

    for job in jobs_weights:
        worker_shape_to_weight(job, rank)

    print(rank, "barrier")
    comm.Barrier()

    if rank == 0:
        jobs_spatial = add_paths_to_jobs(jobs, dir_data, dir_spatial)
        for job in jobs_spatial:
            job.update({'weight_name' : make_weight_name(job)})
            job.update({'path_weight' : make_weigth_path(job, dir_spatial)})
        make_work_data(jobs_spatial, dir_data, dir_spatial)
        jobs_spatial = split(jobs_spatial, size)
    else:
        jobs_spatial = None
    jobs_spatial = comm.scatter(jobs_spatial, root = 0)

    for job in jobs_spatial:
        worker_spatial(job)

    if rank == 0:
        jobs_merge = add_paths_to_jobs(jobs, dir_data, dir_spatial)
        jobs_merge = make_jobs_merge(jobs_merge, dir_data, dir_spatial)
        jobs_merge = split(jobs_merge, size_half, size)
    else:
        jobs_merge = None

    print(rank, "barrier")
    comm.Barrier()

    jobs_merge = comm.scatter(jobs_merge, root=0)

    for j in jobs_merge:
        worker_merge(j)

if __name__ == "__main__":
    main_spat()

