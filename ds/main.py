import argparse
from subprocess import call
from utils import (make_call, make_dirstructure, create_dirs) 
import sys

# Parse parameters
parser = argparse.ArgumentParser()

parser.add_argument("--dir_scratch", type=str,
    help="directory in which to place the run data directory")
parser.add_argument("--dir_input", type=str,
    help="directory to read data from")
parser.add_argument("--run_id", type=str,
    help="for selecting appropriate paramfile and setting storage folder")
parser.add_argument("--dir_paramfiles", type=str,
    help="directory where the paramfile lives")

parser.add_argument("--ncores", type=int,
    help="number of cores to use")

args_main = parser.parse_args()

# @TODO: figure out correct convention for leading and trailing "/"
dir_scratch = args_main.dir_scratch
run_id = args_main.run_id
dir_input = args_main.dir_input

if args_main.dir_paramfiles is not None:
    dir_paramfiles = args_main.dir_paramfiles
else:
    dir_paramfiles = "./paramfiles"

path_pyfile_params = dir_paramfiles + "/" + run_id + ".py"
dir_scratch = dir_scratch + "/" + run_id + "/"
dir_input = dir_input + "/"

ncores = args_main.ncores

make_dirstructure(dir_scratch)

# Prepare argument dictionaries for component scripts
argdict_dir_scratch = {'dir_scratch' : dir_scratch}
argdict_dir_input = {'dir_input' : dir_input}
args = [argdict_dir_scratch]

#########################################################################################
################################## RUNNING STARTS HERE ##################################
#########################################################################################

# Run params file which writes params.json
pyfile = path_pyfile_params
args = [argdict_dir_scratch]
mpi = False
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

pyfile = "prep.py"
args = [argdict_dir_scratch, argdict_dir_input]
mpi = False
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = True
pyfile = "ts.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = True
pyfile = "spatial.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = True
pyfile = "transforms.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = True
pyfile = "train.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = True
pyfile = "sim.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = False
pyfile = "merger.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = True
pyfile = "aggregate.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

mpi = False
pyfile = "finalize.py"
args = [argdict_dir_scratch]
c = make_call(pyfile, ncores, args, mpi)
print(c)
ret = call(c, shell=True)
if ret != 0:
    sys.exit(1)

# mpi = True
# pyfile = "plots.py"
# args = [argdict_dir_scratch]
# c = make_call(pyfile, ncores, args, mpi)
# print(c)
# ret = call(c, shell=True)
# if ret != 0:
#     sys.exit(1)
