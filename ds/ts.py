import pandas as pd

from mpi4py import MPI
import argparse

from utils import (
    split,
    load_params,
    make_work_data,
    add_paths_to_jobs,
    make_jobs_merge,
    worker_merge
    )

def worker_ts(job):
    def count_while(var, criteria, seed=0):
        '''
        Count time as long as variable meets criteria, then resets
        '''
        def rolling_count(var, criteria):
            if eval('var'+criteria):
                rolling_count.count += 1
                return rolling_count.count
            else:
                previous = rolling_count.count + 1
                rolling_count.count = 0
                return previous

        rolling_count.count = seed
        return var.apply(rolling_count, criteria=criteria)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    print(rank, "starting", job['name'])

    df = pd.read_hdf(job['path_input'])
    print("\t", rank, "read", job['path_input'])

    d = job

    varname = d['name']

    if 'lag' in d.keys():
        df[d['name']] = (df.groupby(level=1)[d['var']].shift(d['lag']))

    if 'value' in d.keys():
        df[d['name']] = df[d['name']] == d['value']

    if 'cw' in d.keys():
        if 'seed' in d.keys():
            df[d['name']] = (df.groupby(level=1)[d['var']].apply(
                            count_while,
                            criteria=d['cw'],
                            seed=d['seed'])
                            )
        else:
            df[d['name']] = (df.groupby(level=1)[d['var']].apply(
                            count_while,
                            criteria=d['cw'])
                            )

    if 'ma' in d.keys():
        df[d['name']] = (df.groupby(level=1)[d['var']].apply(lambda x:x.rolling(window=d['ma']).mean()))

    df.sort_index(inplace=True)
    df[[varname]].to_hdf(job['path_output'], key='data', mode='w')
    print("\t", rank, "wrote", job['path_output'])

def main_ts():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_data = dir_scratch + "data/"
    dir_ts = dir_scratch + "ts/"

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Use half the cores for merging to keep mem within bounds
    size_half = int(size/4)
    if size_half == 0:
        size_half = 1

    print(rank, "hello")

    # load jobs from json in the root process
    if rank == 0:
        params = load_params(path_params)
        jobs = params['ts']
        jobs_ts = add_paths_to_jobs(jobs, dir_data, dir_ts)
        make_work_data(jobs_ts, dir_data, dir_ts)
        jobs_ts = split(jobs_ts, size)
    else:
        jobs_ts = None

    jobs_ts = comm.scatter(jobs_ts, root=0)

    for j in jobs_ts:
        worker_ts(j)

    print(rank, "barrier")
    comm.Barrier()

    if rank == 0:
        jobs_merge = add_paths_to_jobs(jobs, dir_data, dir_ts)
        jobs_merge = make_jobs_merge(jobs_merge, dir_data, dir_ts)
        jobs_merge = split(jobs_merge, size_half, size)
    else:
        jobs_merge = None

    jobs_merge = comm.scatter(jobs_merge, root=0)

    for j in jobs_merge:
        worker_merge(j)

    print(rank, "barrier")
    comm.Barrier()

if __name__ == "__main__":
    main_ts()
