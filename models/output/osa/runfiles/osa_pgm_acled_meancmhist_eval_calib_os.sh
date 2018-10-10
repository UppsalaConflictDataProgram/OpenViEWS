#!/bin/bash -l
#SBATCH -A snic2018-3-380
#SBATCH -p core
#SBATCH -n 10


#SBATCH -t 8:00:00
#SBATCH -J osa_pgm_acled_meancmhist_eval_calib_os
#SBATCH -o /proj/snic2018-3-380/runs/current/osa/logs/osa_pgm_acled_meancmhist_eval_calib_os.log

export MKL_NUM_THREADS=10
export NUMEXPR_NUM_THREADS=10
export OMP_NUM_THREADS=10

mkdir -p  $SNIC_TMP/osa/pickles


cd ~/github/Views/models/output/osa/paramfiles

python -u osa_pgm_acled_meancmhist_eval_calib_os.py


echo 'running estimator_output to get regtables etc'
cd ~/github/Views/osa
python estimator_output.py

echo 'deleting all pickles'
find $SNIC_TMP/osa/pickles -name '*.pickle' -delete

echo 'syncing regtables etc'
rsync -av $SNIC_TMP/osa/pickles/ /proj/snic2018-3-380/runs/current/osa/results/

echo 'finished'
