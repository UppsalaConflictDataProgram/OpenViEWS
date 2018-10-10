#!/bin/bash -l
#SBATCH -A snic2017-1-306
#SBATCH -p core

#SBATCH -n 6
#SBATCH -t 48:00:00
#SBATCH -J run1
#SBATCH -o /proj/snic2017-7-47/nstep/logs/run1.log

export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

cd /proj/snic2017-7-47/private/Views/nstep/runs/run1/

python run1_calib.py &
python run1_test.py &
wait
