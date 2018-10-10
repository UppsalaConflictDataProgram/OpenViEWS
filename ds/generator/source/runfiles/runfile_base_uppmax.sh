#!/bin/bash -l
#SBATCH -A snic2017-1-306
#SBATCH -p node

#SBATCH -t 48:00:00
#SBATCH -J $run_id
#SBATCH -o /proj/snic2017-1-306/runs/current/ds/logs/$run_id.log



export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

module load gcc/7.2.0
module load openmpi/2.1.1 

mkdir -p /scratch/ds

#cd /proj/snic2017-1-306/private/Views/ds
cd ~/github/Views/ds

python main.py  --dir_scratch /scratch/ds \
                --run_id $run_id \
                --dir_input /proj/snic2017-1-306/runs/current/ds/input \
                --dir_paramfiles ./generator/output/paramfiles \
                --ncores 20



echo 'copying all .tex .txt and .png files'

rsync -av --include "*/" --include "*.tex" --include "*.txt" --include "*.png" \
          --include "*aggregated.hdf5" --exclude "*" \
          --prune-empty-dirs \
          /scratch/ds/$run_id \
          /proj/snic2017-1-306/runs/current/ds/results \

echo 'finished!'
