import pandas as pd
import numpy as np
import pysal
import matplotlib
matplotlib.use('Agg')  # For plotting on the server
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid # for shiftedColorMap
import argparse
import h5py
import json
import numpy as np
import pandas as pd
from random import shuffle
import pickle
import sys
import os
from mpi4py import MPI
from utils import ( load_params, 
    split, 
    get_model_vars, 
    get_paths_from_dir, 
    add_varsets_to_modeljobs, 
    get_paths_sims,
    create_dirs)

# for shiftedColorMap
from mpl_toolkits.axes_grid1 import AxesGrid

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Credit: #https://gist.github.com/phobson/7916777

    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero
    
    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and 1.0.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          0.0 and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }
      
    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])
    
    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))
        
    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def makesize(df):
    xmax = df['row'].max()
    xmin = df['row'].min()
    ymax = df['col'].max()
    ymin = df['col'].min()
    width = xmax-xmin
    height = ymax-ymin
    scale = 0.1
    size = (width*scale, height*scale)
    return size

def prune_africa(df):
    #The sea-cells closesest to each tip of mainland Africa
    rowmin = 110
    rowmax = 256
    colmin = 324
    colmax = 464

    df = df[df['row']>= rowmin]
    df = df[df['row']<= rowmax]
    df = df[df['col']>= colmin]
    df = df[df['col']<= colmax]
    return df

def make_df_geo(dir_data, dir_plots):
    latlong_vars = ['longitude', 'latitude', 'col', 'row']

    print("making geo df containing")
    for v in latlong_vars:
        print("\t", v)


    paths_data = get_paths_from_dir(dir_data)
    path_data = paths_data[0] # just use the first dataset found
    df = pd.read_hdf(path_data)
    print("read", path_data)
    # Make df time-invariant, containing only our latlong vars
    df = df[latlong_vars]
    df.reset_index(inplace=True)
    df.set_index(['pg_id'], inplace=True)
    del df['month_id']
    df.drop_duplicates(inplace=True)

    path_output = dir_plots + "geo.hdf5"
    df.to_hdf(path_output, key='data')
    print("wrote", path_output)

def make_data_maps(dir_agg, dir_sim, dir_plots, debug=False):
    print("Making data for maps")
    path_geo = dir_plots + "geo.hdf5"
    df_geo = pd.read_hdf(path_geo)
    print("read", path_geo)

    path_agg = dir_agg + "aggregated.hdf5"
    df_agg = pd.read_hdf(path_agg)
    print("read", path_agg)
    df = df_agg.merge(df_geo, left_index = True, right_index = True)


    if debug:
        # get a single path to a sim0_allvars.hdf5 dataframe from the sims dir
        paths_sims_all = get_paths_from_dir(dir_sim)
        path_sim0_allvars = [p for p in paths_sims_all if "sim0_allvars.hdf5" in p][0]
        df_sim0 = pd.read_hdf(path_sim0_allvars)
        print("read", path_sim0_allvars)
        df_sim0 = df_sim0.add_prefix("sim0_")
        df = df.merge(df_sim0, left_index = True, right_index = True)

    df = prune_africa(df)

    dir_maps = dir_plots + "maps/"
    create_dirs([dir_maps])

    path_data_maps = dir_maps + "workdata.hdf5"
    df.to_hdf(path_data_maps, key='data')
    print("wrote", path_data_maps)

def make_jobs_maps(dir_plots):
    dir_maps = dir_plots + "maps/"
    path_workdata = dir_maps + "workdata.hdf5"
    df = pd.read_hdf(path_workdata)

    start = df.index.get_level_values(0).min()
    end = df.index.get_level_values(0).max()
    print("START:", start)
    print("END:", end)

    latlong_vars = ['longitude', 'latitude', 'col', 'row']

    # get the vars we wan't to plot, 
    # that is all we have in the data excluding the latlongs
    mapvars = list(df.columns)
    mapvars = [v for v in mapvars if v not in latlong_vars]
    jobs_maps = []
    for v in mapvars:
        print(v)
        dir_output = dir_maps + v + "/"
        create_dirs([dir_output])
        job = { 'var' : v,
                'path_input' : path_workdata,
                'dir_output' : dir_output,
                'start' : start,
                'end' : end
                }
        jobs_maps.append(job)
    return jobs_maps

def subset_df_times(df, start, end):
    df = df.loc[(   df.index.get_level_values(0) <= end) 
                    &  (df.index.get_level_values(0) >= start)]
    return df

def make_jobs_spaghetti(dir_plots, dir_sim, dir_data, outcomes, start, end):
    dir_spaghetti = dir_plots + "spaghetti/"

    path_data_long = get_paths_from_dir(dir_data)[0]

    jobs = []
    for outcome in outcomes:
        for longbool in [True, False]:
            job = {}
            dir_spaghetti_outcome = dir_spaghetti + outcome + "/"
            create_dirs([dir_spaghetti_outcome])
            path_output = dir_spaghetti_outcome + "spaghetti.png"

            job['long'] = longbool            
            job['outcome'] = outcome
            job['path_data_long'] = path_data_long
            job['dir_input'] = dir_sim
            job['path_output'] = path_output

            if longbool:
                path_output = dir_spaghetti_outcome + "spaghetti_long.png"
                job['path_output'] = path_output
                job['start'] = start
                job['end'] = end

            jobs.append(job)

    for job in jobs:
        #print(job)
        pass

    return jobs

def worker_spaghetti(job, rank):
    plt.figure(figsize=(20,10))

    if job['long']:
        df_long = pd.read_hdf(job['path_data_long'])
        print(rank, "read", job['path_data_long'], "for spaghetti long", job['outcome'])
        df_long = df_long[[job['outcome']]]
        df_long = subset_df_times(df_long, job['start'], job['end'])
        df_long = df_long.groupby(level=0).mean()
        plt.plot(df_long, linewidth = 1)

    paths_input = get_paths_sims(job['dir_input'])
    # limit number of spaghetties for memory contraints
    max_spaghetties = 100
    for p in paths_input[:max_spaghetties]:
        # get the filename and remove the extension
        sim = p.split("/")[-1].split(".hdf5")[0]
        dataset = p.split("/")[-2]
        prefix = "_".join([dataset, sim,""])
        df = pd.read_hdf(p)
        print(rank, "read", p)
        varlist = list(df.columns)
        df = df[[job['outcome']]]
        df = df.add_prefix(prefix)
        df_global_means = df.groupby(level=0).mean()
        plt.plot(df_global_means, linewidth = 0.2)
    plt.savefig(job['path_output'])
    print(rank, "wrote", job['path_output'])

def plot_map(rank, df, varname, vartype, cmap, path):
    
    plt.figure(figsize=(10,10))
    
    if vartype == "dummy":
        # subset the data to only include those cells with events
        d_events = df[df[varname]>0]
        # plot all the cells as a background
        plt.scatter(x=df['col'], y=df['row'], marker='s', s=12)
        # plot the events
        plt.scatter(x=d_events['col'], y=d_events['row'], marker='s', s=12)   
    
    elif vartype == "prob":
        plt.scatter(x=df['col'], 
            y=df['row'], 
            c=df[varname], 
            marker='s', 
            s=12, 
            cmap=cmap, 
            vmin=0, 
            vmax=1)

        plt.colorbar()
    
    elif vartype == "continuous":
        plt.scatter(x=df['col'], 
            y=df['row'], 
            c=df[varname], 
            marker='s', 
            s=12, 
            cmap=cmap)
    
        plt.colorbar()

    plt.savefig(path)
    print(rank, "wrote", path)
    plt.close()

def get_vartype(df, v):
    binary = len(df[v].value_counts()) == 2
    bounded_0_1 = df[v].min()>=0 and df[v].max()<=1

    if bounded_0_1 and binary:
        return "dummy"
    elif bounded_0_1 and not binary:
        return "prob"
    else:
        return "continuous"

def worker_map(job, rank):
    print(rank, "starting map job for", job['var'])
    df = pd.read_hdf(job['path_input'])
    print(rank, "read", job['path_input'])

    vartype = get_vartype(df, job['var'])
    print(job['var'], "is", vartype)

    cmap = plt.get_cmap("rainbow")
    if vartype == "prob":
        cmap_probs = shiftedColorMap(cmap, 0, 0.01, 1)
        cmap = cmap_probs
    else:
        cmap = None

    for t in range(job['start'], job['end']):
        path_output = job['dir_output'] + str(t) + ".png"
        plot_map(rank, df.loc[t], job['var'], vartype, cmap, path_output)

def plot_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_scratch = args.dir_scratch
    dir_sim = dir_scratch + "sim/"
    dir_data = dir_scratch + "data/"
    dir_train = dir_scratch + "train/"
    dir_agg = dir_scratch + "aggregate/"
    dir_output = dir_scratch + "output/"
    dir_plots = dir_scratch + "plots/"

    aggvar = "gwcode"

    if rank == 0:
        params = load_params(path_params)
        start = params['times']['full_start']
        end = params['times']['full_end']
        outcomes = params['vars_plots_outcomes']


    # if rank==0:
    #     make_df_geo(dir_data, dir_plots)
    #     make_data_maps(dir_agg, dir_sim, dir_plots)
    #     jobs_maps = make_jobs_maps(dir_plots)
    #     jobs_maps = split(jobs_maps, size)
    # else:
    #     jobs_maps = None

    # jobs_maps = comm.scatter(jobs_maps, root=0)

    # for job in jobs_maps:
    #     worker_map(job, rank)
    #     pass

    # # Use half the cores for merging to keep mem within bounds
    # size_half = int(size/4)
    # if size_half == 0:
    #     size_half = 1

    # if rank == 0:
    #     jobs_spaghetti = make_jobs_spaghetti(dir_plots, dir_sim, dir_data, outcomes, start, end)
    #     jobs_spaghetti = split(jobs_spaghetti, size_half, size)
    # else:
    #     jobs_spaghetti = None
    # jobs_spaghetti = comm.scatter(jobs_spaghetti, root=0)

    # for job in jobs_spaghetti:
    #     worker_spaghetti(job, rank)
    #     pass

    if rank == 0:
        jobs_spaghetti = make_jobs_spaghetti(dir_plots, dir_sim, dir_data, outcomes, start, end)
        for job in jobs_spaghetti:
            worker_spaghetti(job, rank)




if __name__ == "__main__":
    plot_main()
