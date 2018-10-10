#!/bin/bash -l
#SBATCH -A snic2017-1-306
#SBATCH -p node

#SBATCH -t 48:00:00
#SBATCH -J pgm_sbonly_wcm_naive_eval_test
#SBATCH -o /proj/snic2017-1-306/projects/geoimp_evaluation/current/ds/logs/pgm_sbonly_wcm_naive_eval_test.log



export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

module load gcc/7.2.0
module load openmpi/2.1.1 

mkdir -p  $SNIC_TMP/ds

cd ~/github/Views/ds

python main.py  --dir_scratch  $SNIC_TMP/ds \
                --run_id pgm_sbonly_wcm_naive_eval_test \
                --dir_input /proj/snic2017-1-306/projects/naive_evaluation/current/ds/input_naive \
                --dir_paramfiles ../projects/geoimp_evaluation/ds/paramfiles \
                --ncores 20

echo 'copying all .tex .txt and .png files'

rsync -av --include "*/" --include "*.tex" --include "*.txt" --include "*.png" \
          --include "*aggregated.hdf5" --exclude "*" \
          --prune-empty-dirs \
           $SNIC_TMP/ds/pgm_sbonly_wcm_naive_eval_test \
          /proj/snic2017-1-306/projects/geoimp_evaluation/current/ds/results \

echo 'finished'
