#!/bin/bash

# These settings force model training to use only one core
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

DIR_DS=~/github/Views/ds

# Activate the conda env
source activate dynasim

#
cd $DIR_DS
python main.py  --dir_scratch ~/dynasim/scratch \
                --run_id example \
                --dir_input $DIR_DS/example/data \
                --ncores 4 \
                --dir_paramfiles $DIR_DS/example/paramfiles \

echo "If nothing went wrong dynasim done!"
echo "Your results are in ~/dynasim/scratch/example/output/aggregated.csv"