import os
import pandas as pd
import numpy as np
import json
import random
from mpi4py import MPI
import h5py


import gc

from numba import vectorize


def split(jobs, n_workers, targetsize = None):
    """
    https://gist.github.com/krischer/2c7b95beed642248487a
    
    """
    if targetsize == None:
        targetsize = n_workers

    random.shuffle(jobs)
    jobs = [jobs[_i::n_workers] for _i in range(n_workers)]
    jobs = pad_list(jobs, targetsize)
    return jobs

def pad_list(l, target_len):
    
    while len(l) < target_len:
        l.append([])
    return l

def make_call(pyfile, ncores, args, mpi):
    def argdicts_to_string(argdicts):
        argstring = ""
        for arg in argdicts:
            for key,val in arg.items():
                arg = "--" + key + " " + val + " "
            argstring += arg
        return argstring        
    
    args = argdicts_to_string(args)
    if mpi:
        call = "mpiexec -n " + str(ncores) + " python -u " + pyfile + " " + args
    else:
        call = "python -u " + pyfile + " " + args 
    return call 

def merge_dfs(df, dir_data):
    paths_data = []
    for root, dirs, files in os.walk(dir_data):
        for file in files:
            p=os.path.join(root,file)
            paths_data.append(p)

    for f in paths_data:
        print("Loading ", f, "for merging", end = " ... ")
        df_scratch = pd.read_hdf(f, key='data')
        print(" done!")
        print("Deleting ", f, end = " ... ")
        os.remove(f)
        print(" done!")
        print("Merging ", f, end = " ... ")
        df = df.merge(df_scratch, left_index=True, right_index=True)
        print(" done!")
    return df

def load_params(path_params):
    with open(path_params, 'r') as j:
        jobs = json.load(j)
    return jobs

def make_tempdata_path(directory, varname):
    filename = varname + ".hdf5"
    path = directory + filename
    return path

def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)

def make_dirstructure(basedir):
    # empty string is for the basedir
    dirs = ["",
            "ts", 
            "spatial",
            "spatial/shapes", 
            "train", 
            "sim",
            "input",
            "data",
            "imputer",
            "models",
            "transforms",
            "aggregate",
            "plots",
            "output"]
    fulldirs = []
    for d in dirs:
        fd = basedir + d
        fulldirs.append(fd)

    create_dirs(fulldirs)

def write_json(path, d):
    with open (path, 'w') as j:
        json.dump(d, j)
        print("Wrote", path)

def load_params(path):
    with open(path, 'r') as j:
        params = json.load(j)
    return params

def randomize_dummy(s):
    """Returns dummies with same groupwise mean as input series,
    useful for making fake imputations"""
    a = s.groupby(level=1).transform("mean")
    nature = np.random.random(size=len(a))
    bools = a > nature
    bools = bools.astype(int)
    return bools

def make_list_sourcevars(jobs):
    # list of vars needed to compute the tsvars
    sourcevars = []
    for job in jobs:
        keys = job.keys()
        msg = "jobdict must have a AND b XOR var in its keys"
        assert ('a' in keys and 'b' in keys) or ('var' in keys) or ('varlist' in keys), msg

        if 'var' in keys:
            sourcevars.append(job['var'])
        elif 'a' in keys and 'b' in keys:
            sourcevars.append(job['a'])
            sourcevars.append(job['b'])
        elif 'varlist' in keys:
            sourcevars += job['varlist']

    sourcevars = sorted(list(set(sourcevars)))
    return sourcevars

def make_pathdicts_data(dir_data):
    # paths to all datasets
    paths_inputdata = []
    for root, dirs, files in os.walk(dir_data):
        for file in files:
            path = os.path.join(root,file)
            f_noext = file.split(".hdf5")[0]
            pathdict = {'path' : path,
                        'filename_noext' : f_noext}
            paths_inputdata.append(pathdict)
    return paths_inputdata

def copy_sourcevars(sourcevars, pathdicts_data, dir_work):
    for pathdict in pathdicts_data:
        df = pd.read_hdf(pathdict['path'])
        df = df[sourcevars]
        print("Read", pathdict['path'])
        dir_work_df = dir_work + pathdict['filename_noext'] + "/"
        create_dirs([dir_work_df])
        path_source = dir_work_df + "workdata.hdf5"
        df.to_hdf(path_source, key='data', mode='w')
        print("Wrote", path_source)
        del df
        gc.collect()


def make_work_data(jobs, dir_data, dir_work):
    sourcevars = make_list_sourcevars(jobs)
    pathdicts_data = make_pathdicts_data(dir_data)
    copy_sourcevars(sourcevars, pathdicts_data, dir_work)

def get_list_groupvars(dir_data):
    """Return list of all groupvars (gids) from one dataset in /data/ 
    Used for subsetting weight matrix"""
    print("Getting list of groupvars from data")
    pathdicts_data = make_pathdicts_data(dir_data)
    pdd = pathdicts_data[0]
    df = pd.read_hdf(pdd['path'])
    print("read", pdd['path'], "in get_list_groupvars()")
    groupvars = df.index.levels[1].values.tolist()    
    return groupvars

def add_paths_to_jobs(jobs, dir_data, dir_work):
    pathdicts_data = make_pathdicts_data(dir_data)
    jobs_w_paths = []
    
    for pdd in pathdicts_data:
        dir_work_df = dir_work + pdd['filename_noext'] + "/"
        for job in jobs:
            j = job.copy()
            path_workdata = dir_work_df + "workdata.hdf5"
            j['path_source_df'] = pdd['path']
            j['path_input'] = path_workdata
            j['path_output'] = dir_work_df + j['name'] + ".hdf5"
            j['name_source'] = pdd['filename_noext']

            jobs_w_paths.append(j)
    return jobs_w_paths
    
def make_jobs_merge(jobs, dir_data, dir_work):
    pathdicts_data = make_pathdicts_data(dir_data)

    mergejobs = []
    for pdd in pathdicts_data:
        workpaths = []
        for job in jobs:
            if job['path_source_df']==pdd['path']:
                workpaths.append(job['path_output'])
        mergejob = {'path_source' : pdd['path'],
                    'paths_work' : workpaths}
        mergejobs.append(mergejob)
    return mergejobs

def worker_merge(job):

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    print(rank, "starting mergejob for", job['path_source'])

    df = pd.read_hdf(job['path_source'])
    for path in job['paths_work']:
        df_work = pd.read_hdf(path)
        os.remove(path)
        print("\t", rank, "read and removed", path)
        
        df = df.merge(df_work, left_index=True, right_index=True)
    
    df.to_hdf(job['path_source'], key='data', format='table', mode='w')
    print(rank, "wrote", job['path_source'])

    del df
    gc.collect()
        
def add_varsets_to_modeljobs(jobs):

    def sanitize_minus(lhsvars):
        # From individual term strings remove what comes after a -
        # The purpose is to replace strings like "varname - 1" with just 
        # "varname"
        lhsvars_temp = []
        for v in lhsvars:
            if "-" in v:
                print("found - in {}".format(v))
                v = v.split("-")[0]
                print("changed to {}".format(v))
            else:
                pass
            lhsvars_temp.append(v)

        return lhsvars_temp


    # inserts valeus for right hand side and left hand side vars to a model
    # description job based on the formula
    jobs_w_varsets = []
    for j in jobs:
        job_w_varset = j
        f = j['formula']

        sides = f.split("~")
        rhsvar = sides[0].strip()
        lhsvars = sides[1].split("+")
        lhsvars = sanitize_minus(lhsvars)

        
        lhsvars = list(map(str.strip, lhsvars))

        job_w_varset['rhsvar'] = rhsvar
        job_w_varset['lhsvars'] = lhsvars
        job_w_varset['allvars'] = [rhsvar] + lhsvars 
        jobs_w_varsets.append(job_w_varset)

    return jobs_w_varsets

def get_model_vars(jobs):
    allvars = []
    for j in jobs:
        allvars += j['allvars']
    allvars = list(set(allvars))
    return allvars

def inv_logit(x):
    return (1 + np.tanh(x / 2)) / 2

@vectorize
def vdecide(nature, risk):
    if nature < risk:
        return 1
    else:
        return 0

def copy_subset_data(modelvars, start, end, pathdicts_data, dir_work):
    
    for pathdict in pathdicts_data:
        # Read only columns included in model vars
        df = pd.read_hdf(pathdict['path'], columns = modelvars)
        print("Read", pathdict['path'])

        # subset df to include time [start, end] 
        # index level 0 is timevar
        df = df.loc[(   df.index.get_level_values(0) <= end) 
                    &  (df.index.get_level_values(0) >= start)]

        # ex. /runid/train/df0/
        dir_work_df = dir_work + pathdict['filename_noext'] + "/"
        create_dirs([dir_work_df])
        # ex. /runid/train/df0/workdata.hdf5
        path_workdata = dir_work_df + "workdata.hdf5"
        df.to_hdf(path_workdata, key='data', mode='w')
        del df
        gc.collect()
        print("Wrote", path_workdata)

def make_data_subset(allvars, start, end, dir_data, dir_work):
    """ For each imputed dataset create subset of 
        data in runid/(train/sim)/dfX/workdata.hdf5

        Note:
             data is subsetted by
            * start and end (including endpoints)
            * Variables used in models, 
              all vars from all models incldued in every training dataset"""
    
    pathdicts_data = make_pathdicts_data(dir_data)
    copy_subset_data(allvars, start, end, pathdicts_data, dir_work)

def add_nsim_to_jobs(jobs, nsim):
    for job in jobs:
        job.update({'nsim' : nsim})
    return jobs

def fill_all_missing(df):
    
    def nan_to_mean(df, varlist):
        """Imputes missing values for single variable var in df with group level means (index level 0 is group level), 
        if still missing, fills mean from entire df"""
        print("Imputing mean: ")
        for var in varlist:
            print("\t", var)
            #impute with group level mean 
            df[var].fillna(df.groupby(level=1)[var].transform("mean"), inplace=True)
            # fill remaining NaN with df level mean
            df[var].fillna(df[var].mean(), inplace=True)
        return df

    def nan_to_zero(df, varlist):
        df[varlist] = df[varlist].fillna(value=0)
        return df

    def get_binaries(df):
        binaries = []
        print("Binary variables: ")
        for col in df.columns:
            if len(df[col].value_counts())==2:
                print("\t" , col)
                binaries.append(col)
        return binaries

    def f_bfill(df, varlist):
        # group by groupvar and forward fill
        print("Filling forwards")
        df[varlist] = df[varlist].groupby(level=1).fillna(method='ffill')
        print("Filling backwards")
        df[varlist] = df[varlist].groupby(level=1).fillna(method='bfill')
        return df




    print("SHARES MISSING IN DF PRE fill_all_missing()")
    print(df.isnull().sum()/len(df))
    
    excludevars = [ "country_month_id", "pg_id", "month_id", "row",
                        "col", "latitude", "longitude", "gwcode"]

    numerics = list(df.select_dtypes(include=[np.number]).columns)
    binaries = get_binaries(df[numerics])

    # never impute excludevars
    numerics = [item for item in numerics if item not in excludevars]
    binaries = [item for item in binaries if item not in excludevars]

    # fill missing binaries with zero
    df = nan_to_zero(df, binaries)
    # try forward filling numerics 
    df = f_bfill(df, numerics)

    numerics_not_filled = []
    print("Remaining missing after filling zeroes and forward filling")
    for col in numerics:
        n_missing = df[col].isnull().sum()
        print("\t", n_missing, "\t", col)
        if n_missing != 0:
            numerics_not_filled.append(col)

    # If forward filling didn't do it we just impute the mean
    df = nan_to_mean(df, numerics_not_filled)
    print("SHARES MISSING IN DF POST fill_all_missing()")
    print(df.isnull().sum()/len(df))

    return df

def get_paths_sims(dir_sim):
    paths = []
    for root, dirs, files in os.walk(dir_sim):
        for file in files:
            if not file == "workdata.hdf5" and not file == "sim0_allvars.hdf5":
                path = os.path.join(root,file)
                paths.append(path)
    return paths

def get_paths_from_dir(dir, extension=None):
    paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root,file)
            paths.append(path)
    if extension:
        print("Selecting paths containing", extension, "from", dir)
        paths = [path for path in paths if extension in path.split("/")[-1]]
    return paths    

def get_predictions_training(path_model):
    print("Opening", path_model)
    with  h5py.File(path_model, 'r') as h5f:
        predictions_training = h5f['predictions_training'][:]
    print("Read training predictions from", path_model)
    return predictions_training