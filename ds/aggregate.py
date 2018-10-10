from mpi4py import MPI
import argparse
import h5py
import numpy as np
import os
import pandas as pd
import pickle
import scipy.stats as spstats
import sys
import time

from utils import (
    split,
    load_params,
    get_paths_sims,
    create_dirs
    )

def get_aggregate(statistic, rank, results, varnames, index, chunksize):
    """Calculate aggregate statistic for all variables in results array
    
    Args:
        statistic: a dict containing name and optionally q:
                   supported values of statistic['name']:
                        "mean", "var", "skew", "kurtosis", "pctile".
                    if statistic['name'] is "pctile" then statistic['q'] must
                    also be provided

        results: numpy-array with dimensions [nsim, row, var]
        varnames: list of variable names in the input array (results)
        index: indexes to assign to the finished percentiles
        chunksize: how many rows to consider at a time
    
    Returns:
        output: A pandas DataFrame containing the chosen statistic for all
                variables in the results array
    """
    def chunker(seq, size):
        """Returns seq as an iterable over chunks of seq of size
        Used for splitting ranges of rows in an array into managable subsets."""
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))


    # Empty placeholder
    nrows = results.shape[1]
    nvars = results.shape[2]
    output = np.empty((nrows, nvars))

    # Iterate over chunksize of the rows at a time
    for rows in chunker(range(nrows), chunksize):
        progress = rows[0]/nrows
        print("progress:", rank, statistic['stat'], "\t", "%.3f" % progress)

        if statistic['stat'] == "mean":
            output[rows, :] = np.mean(results[:, rows, :], axis=0)
        
        elif statistic['stat'] == "var":
            output[rows, :] = np.var(results[:, rows, :], axis=0)
        
        elif statistic['stat'] == "skew":
            output[rows, :] = spstats.skew(results[:, rows, :], axis=0)
        
        elif statistic['stat'] == "kurtosis":
            output[rows, :] = spstats.kurtosis(results[:, rows, :], axis=0)
        
        elif statistic['stat'] == "pctile":
            q = statistic['q']
            output[rows, :] = np.percentile(results[:, rows, :], q=q, axis=0)


    # Create the variable names
    if statistic['stat'] == "pctile":
        suffix = "_pct" + str(statistic['q'])
    else:
        suffix = "_"+statistic['stat']
    colnames = [var + suffix for var in varnames]

    output = pd.DataFrame(output,
                          columns=colnames,
                          index=index)
    return(output)

def worker_aggregate(job, rank):
    print(rank, "starting job", job['name'])


    chunksize = 5000

    with open(job['path_index'], 'rb') as f:
        index = pickle.load(f)
        print(rank, "read", job['path_index'])
    with open(job['path_varnames'], 'rb') as f:
        varnames = pickle.load(f)
        print(rank, "read", job['path_varnames'])

    # Pass driver='core' to read everything into memory, omit it to read chunkwise from the file
    #with h5py.File(path_merged, 'r', driver='core') as f:
    with h5py.File(job['path_input'], 'r') as f:
        print(rank, "opened", job['path_input'])
        results = f['simulation_results']
        df = get_aggregate(job, rank, results, varnames, index, chunksize)

    df.to_hdf(job['path_output'], key='data')
    print(rank, "wrote", job['path_output'])

def save_sim_index_and_varnames(dir_sim, dir_agg):
    path_any_sim = get_paths_sims(dir_sim)[0]
    df = pd.read_hdf(path_any_sim, key='data')
    print("read", path_any_sim, "to get index and varnames")
    
    index = df.index
    varnames = df.columns

    path_p_index = dir_agg + "index.p"
    path_p_varnames = dir_agg + "varnames.p"
    with open(path_p_index, 'wb') as p:
        pickle.dump(index, p)
        print("wrote", path_p_index)
    with open(path_p_varnames, 'wb') as p:
        pickle.dump(varnames, p)
        print("wrote", path_p_varnames)


def prep_jobs_agg(jobs, dir_agg):
    dir_agg_stats = dir_agg + "stats/"
    create_dirs([dir_agg_stats])

    path_input = dir_agg + "merged.hdf5"

    for job in jobs:
        if "q" in job.keys():
            job['name'] = job['stat'] + str(job['q'])
        else:
            job['name'] = job['stat']

        path_output = dir_agg_stats + job['name'] + ".hdf5"
        job['path_input'] = path_input
        job['path_output'] = path_output
        job['path_index'] = dir_agg + "index.p"
        job['path_varnames'] = dir_agg + "varnames.p" 
    
    return jobs

def merge_aggs(dir_agg, rank):
    dir_agg_stats = dir_agg + "stats/"
    paths_aggs = []
    for root, dirs, files in os.walk(dir_agg_stats):
        for file in files:
            path = os.path.join(root,file)
            paths_aggs.append(path)

    df_base = pd.read_hdf(paths_aggs[0])
    print(rank, "read", paths_aggs[0], "to use as base for merge")
    for path in paths_aggs[1:]:
        df_scratch = pd.read_hdf(path)
        print(rank, "read", path)
        df_base = df_base.merge(df_scratch, left_index = True, right_index = True)

    path_output = dir_agg + "aggregated.hdf5"
    df_base.to_hdf(path_output, key = 'data')
    print(rank, "wrote", path_output)

def cleanup(dir_agg):
    path_merged = dir_agg + "merged.hdf5"
    print("removing merged file ", path_merged)
    os.remove(path_merged)
    print("done")

def aggregate_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_agg = dir_scratch + "aggregate/"
    dir_sim = dir_scratch + "sim/"

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        params = load_params(path_params)
        jobs_agg = params['stats']
        save_sim_index_and_varnames(dir_sim, dir_agg)
        jobs_agg = prep_jobs_agg(jobs_agg, dir_agg)
        jobs_agg = split(jobs_agg, size)
    else:
        jobs_agg = None

    jobs_agg = comm.scatter(jobs_agg, root=0)


    for job in jobs_agg:
        worker_aggregate(job, rank)

    print(rank, "barrier")
    comm.Barrier()
    if rank == 0:
        merge_aggs(dir_agg, rank)

    # CLEANUP
    if rank == 0:
        cleanup(dir_agg)
        

if __name__ == "__main__":
    aggregate_main()