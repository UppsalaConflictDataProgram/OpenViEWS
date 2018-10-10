#!/bin/bash -l
#SBATCH -A snic2018-3-380
#SBATCH -p node

#SBATCH -t 48:00:00
#SBATCH -J pgm_acled_nat_fcast_calib
#SBATCH -o /proj/snic2018-3-380/runs/current/ds/logs/pgm_acled_nat_fcast_calib.log



export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

module load gcc/7.2.0
module load openmpi/2.1.1

mkdir -p  $SNIC_TMP/ds

cd ~/github/Views/ds

python main.py  --dir_scratch  $SNIC_TMP/ds \
                --run_id pgm_acled_nat_fcast_calib \
                --dir_input /proj/snic2018-3-380/runs/current/ds/input \
                --dir_paramfiles ../models/output/ds/paramfiles \
                --ncores 20

echo 'copying all .tex .txt and .png files'

rsync -av --include "*/" --include "*.tex" --include "*.txt" --include "*.png" \
          --include "*aggregated.hdf5" --exclude "*" \
          --prune-empty-dirs \
           $SNIC_TMP/ds/pgm_acled_nat_fcast_calib \
          /proj/snic2018-3-380/runs/current/ds/results \

echo 'finished'
