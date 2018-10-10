import argparse
from mpi4py import MPI

import pandas as pd
import numpy as np

from utils import (
    split,
    load_params,
    add_paths_to_jobs,
    make_jobs_merge,
    worker_merge,
    make_work_data
)



def decayer(var, halflife):
    return 2**((-1*var)/halflife)

def natural_logger(a):
    return np.log(a+1)

def apply_transform(data, transform):
    # td is transformation dictionary
    td = transform
    func = td['f']

    if func == "decay":
        var = data[td['var']]
        halflife = td['halflife']
        name = td['name']
        data[name] = decayer(var, halflife)

    elif func == "log_natural":
        data[td['name']] = natural_logger(data[td['var']])

    elif func == "add":
        data[td['name']] = data[td['a']] + data[td['b']]

    elif func == "subtract":
        data[td['name']] = data[td['a']] - data[td['b']]

    elif func == "multiply":
        data[td['name']] = data[td['a']] * data[td['b']]

    elif func == "divide":
        data[td['name']] = data[td['a']] / data[td['b']]

    elif func == "sum":
        data[td['name']] = np.sum(data[td['varlist']], axis=1)

    elif func == "mean":
        data[td['name']] = data[td['var']].groupby(level=1).transform('mean')

    return data

def worker_trans(job, rank):
    df = pd.read_hdf(job['path_input'])
    print(rank, "read", job['path_input'], "for", job['name'])
    df = apply_transform(df, job)
    df[[job['name']]].to_hdf(job['path_output'], key='data')
    print(rank, "wrote", job['path_output'])


def main_transforms():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_data = dir_scratch + "data/"
    dir_ts = dir_scratch + "ts/"
    dir_trans = dir_scratch + "transforms/"

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    print(rank, "hello")

    # Use half the cores for merging to keep mem within bounds
    size_half = int(size/4)
    if size_half == 0:
        size_half = 1

    if rank == 0:
        params = load_params(path_params)
        jobs = params['transforms']
        jobs_trans = add_paths_to_jobs(jobs, dir_data, dir_trans)
        make_work_data(jobs_trans, dir_data, dir_trans)

        jobs_trans = split(jobs_trans, size)
    else:
        jobs_trans = None

    jobs_trans = comm.scatter(jobs_trans, root=0)

    for job in jobs_trans:
        worker_trans(job, rank)


    print(rank, "barrier")
    comm.Barrier()

    if rank == 0:
        jobs_merge = add_paths_to_jobs(jobs, dir_data, dir_trans)
        jobs_merge = make_jobs_merge(jobs_merge, dir_data, dir_trans)
        jobs_merge = split(jobs_merge, size_half, size)
    else:
        jobs_merge = None

    jobs_merge = comm.scatter(jobs_merge, root=0)

    for j in jobs_merge:
        worker_merge(j)

if __name__ == "__main__":
    main_transforms()
