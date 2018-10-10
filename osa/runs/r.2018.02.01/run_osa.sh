#!/bin/bash -l
#SBATCH -A snic2017-1-306
#SBATCH -p core

#SBATCH -n 10
#SBATCH -t 48:00:00
#SBATCH -J osa
#SBATCH -o /proj/snic2017-1-306/runs/r.2018.02.01/osa/logs/run.log

export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

cd /proj/snic2017-1-306/private/Views/osa/runs/r.2018.02.01/

python train.py &
python calib.py &
python test.py &
wait
