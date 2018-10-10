#!/bin/bash

export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

# bla bla
source /srv/datastore/envs/py3/bin/activate

python main.py --dir_scratch /srv/datastore/runs --run_id long_hh_dec11 --dir_input /srv/datastore/not_imputed/input --ncores 2
