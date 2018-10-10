import pandas as pd
import numpy as np

import argparse
import os
import sys
import h5py
import time

from utils import get_paths_sims

def merge_sims(paths_sims, dir_agg):
    def make_shape(path_sim, nsim):
        sim = 0
        placeholder_df = df=pd.read_hdf(path_sim, key='data')
        shp = placeholder_df.values.shape
        shp = list(shp)
        shp.insert(0, nsim)
        return shp

    def make_placeholder_file(path_merged, shape, nsim, compression, chunks):
        with h5py.File(path_merged, 'w') as f:
            result = f.create_dataset("simulation_results",
                                      tuple(shape),
                                      dtype='float64',
                                      compression=compression,
                                      chunks=chunks)
        print("Created", path_merged)
    
    def insert_results(path_merged, paths_sims):
        with h5py.File(path_merged, 'a') as f:
            result = f['simulation_results']
            i = 0
            for path_sim in paths_sims:
                print("inserting", path_sim, end = " ... ")
                t1 = time.time()
                df = pd.read_hdf(path_sim, key='data')
                result[i, :, :] = np.array(df.values, dtype=np.float64)
                print("Time: ", str(time.time()-t1))
                i += 1

    nsim = len(paths_sims)
    path_sim = paths_sims[0]
    shape = make_shape(path_sim, nsim)

    path_merged = dir_agg + "merged.hdf5"
    compression = 'lzf'
    chunks = (1, shape[1], shape[2])
    make_placeholder_file(path_merged, shape, nsim, compression, chunks)
    insert_results(path_merged, paths_sims)



def merger_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_data = dir_scratch + "data/"
    dir_sim = dir_scratch + "sim/"
    dir_agg = dir_scratch + "aggregate/" 


    paths_sims = get_paths_sims(dir_sim)
    merge_sims(paths_sims, dir_agg)




if __name__ == "__main__":
    merger_main()