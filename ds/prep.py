""" Prepfile for data going into dynasim

Todo:
    Check which times are in the data, compare to times (train/sim)*(start/end)
    Check for inf and -inf values
    Check for missingness
"""

from __future__ import print_function
from __future__ import division

import pandas as pd
import numpy as np
import json
import argparse
import shutil

from utils import (load_params,
    fill_all_missing,
    get_paths_from_dir,
    get_model_vars,
    make_list_sourcevars,
    add_varsets_to_modeljobs)

def get_allvars(params):
    # this is horrible, I'm sorry.
    vars_models = get_model_vars(add_varsets_to_modeljobs(params['models']))
    vars_ts = make_list_sourcevars(params['ts'])
    vars_spatial = make_list_sourcevars(params['spatial'])
    vars_transforms = make_list_sourcevars(params['transforms'])
    vars_plots = params['vars_plots']
    try:
        vars_transforms_post = make_list_sourcevars(params['transforms_post'])
    except:
        vars_transforms_post = []



    allvars = vars_models + vars_ts + vars_spatial + vars_plots + vars_transforms + vars_transforms_post
    allvars = list(set(allvars))
    allvars = sorted(allvars)
    print("All the vars:")
    for v in allvars:
        print("\t", v)
    return allvars

def forget_future_model_outcomes(df, params):
    """ Forget the future for outcomes """

    models = params['models']
    sim_start = params['times']['sim_start']

    for model in models:
        outcome = model['formula'].split("~")[0].strip()
        print(f"Removing all values of {outcome} after {sim_start}")
        df.loc[sim_start:, outcome] = np.nan

    return df


def worker_prep(job):
    df = pd.read_hdf(job['path_input'])
    print("Prep read", job['path_input'])
    df.set_index([job['timevar'], job['groupvar']], inplace=True)
    df.sort_index(inplace=True)
    print("Prep set index by", job['timevar'], job['groupvar'], "and sorted.")

    # Keep only the vars we need
    allvars = job['allvars']
    vars_in_data = list(df.columns)
    vars_to_keep = [v for v in allvars if v in vars_in_data]
    df = df[vars_to_keep]

    df = forget_future_model_outcomes(df, job['params'])
    df = fill_all_missing(df)

    df.to_hdf(job['path_output'], key='data')
    print("Prep wrote", job['path_output'])

def main_prep():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch",   type=str,
        help="temp directory in which to save data")
    parser.add_argument("--dir_input", type=str,
    help="directory to read data from")
    args = parser.parse_args()

    dir_scratch = args.dir_scratch
    dir_input = args.dir_input

    path_params = dir_scratch + "params.json"
    params = load_params(path_params)

    params_data = params['data']
    groupvar = params_data['groupvar']
    timevar = params_data['timevar']

    allvars = get_allvars(params)

    # @TODO: This is stupid, remove
    if groupvar == "pg_id" and timevar == "month_id":
        dir_input += "pgm/"
    elif groupvar == "country_id" and timevar == "month_id":
        dir_input += "cm/"
    elif groupvar == "country_id" and timevar == "year_id":
        dir_input +="cy/"
    elif groupvar == "gwno" and timevar == "year":
        dir_input += "gwy/"

    dir_input_data = dir_input + "data/"
    dir_input_spatial = dir_input + "spatial/"
    dir_data = dir_scratch + "data/"
    dir_spatial = dir_scratch + "spatial/"
    dir_spatial_shapes = dir_spatial + "shapes/"

    paths_input_data = get_paths_from_dir(dir_input_data, extension=".hdf5")
    print("found:")
    for p in paths_input_data:
        print("\t", p)
    if len(paths_input_data)==0:
        raise FileNotFoundError("Didn't find any input files, did you specify --dir_input correctly?")


    jobs_prep = []
    for path in paths_input_data:
        filename = path.split("/")[-1]
        job = { 'path_input' : path,
                'path_output' : dir_data + filename,
                'timevar' : timevar,
                'groupvar' : groupvar,
                'allvars' : allvars,
                'params' : params}
        jobs_prep.append(job)

    for job in jobs_prep:
        worker_prep(job)

    # Simply copy all files from input/spatial/ to rundir/spatial/shapes/
    paths_input_shapes = get_paths_from_dir(dir_input_spatial)
    for path_input in paths_input_shapes:
        filename = path_input.split("/")[-1]
        destination = dir_spatial_shapes + filename
        shutil.copyfile(path_input, destination)
        print("Prep copied", path_input, "to", destination)


    print("Prep finished")

if __name__ ==  "__main__":
    main_prep()