import pandas as pd

from mpi4py import MPI
import argparse

from utils import (
    add_nsim_to_jobs,
    add_paths_to_jobs,
    load_params,
    make_data_subset,
    split,
    add_varsets_to_modeljobs,
    get_model_vars
    )

from models_sm import load_model


def worker_train(job):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    message = str(rank) + " started job for " + job['name']
    print(message)

    # Don't load from file, we haven't trained it yet!
    model = load_model(job, from_file=False)
    model.from_description()

    df = pd.read_hdf(job['path_input'], key='data')
    model.train(df)
    model.populate(job['nsim'])
    model.save()

def main_train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_data = dir_scratch + "data/"
    dir_train = dir_scratch + "train/"


    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Use half the cores for mergin to keep mem within bounds
    size_half = int(size/2)
    if size_half==0:
        size_half=1

    # load jobs from json in the root process
    if rank==0:
        params = load_params(path_params)
        jobs = params['models']

        jobs = add_paths_to_jobs(jobs, dir_data, dir_train)
        jobs = add_varsets_to_modeljobs(jobs)
        jobs = add_nsim_to_jobs(jobs, params['nsim'])

        train_start = params['times']['train_start']
        train_end = params['times']['train_end']
        allvars = get_model_vars(jobs)

        print("ALLVARS:")
        for v in allvars:
            print(v)

        make_data_subset(allvars, train_start, train_end, dir_data, dir_train)

        jobs = split(jobs, size)

    else:
        jobs = None

    jobs = comm.scatter(jobs, root=0)

    for job in jobs:
        worker_train(job)

if __name__ == "__main__":
    main_train()
