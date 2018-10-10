#!/bin/bash -l
#SBATCH -A snic2018-3-380
#SBATCH -p node

#SBATCH -t 4:00:00
#SBATCH -J cm_transforms
#SBATCH -o /proj/snic2018-3-380/runs/current/ds/logs/cm_transforms.log



export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

module load gcc/7.2.0
module load openmpi/2.1.1

mkdir -p  $SNIC_TMP/ds

cd ~/github/Views/ds

python main.py  --dir_scratch  $SNIC_TMP/ds \
                --run_id cm_transforms \
                --dir_input /proj/snic2018-3-380/runs/current/ds/input \
                --dir_paramfiles ../models/output/ds/paramfiles \
                --ncores 20

echo 'copying all .tex .txt and .png files'

rsync -av --include "*/" --include "*.tex" --include "*.txt" --include "*.png" \
          --include "*aggregated.hdf5" --exclude "*" \
          --prune-empty-dirs \
           $SNIC_TMP/ds/cm_transforms \
          /proj/snic2018-3-380/runs/current/ds/results \


mkdir -p /proj/snic2018-3-380/runs/current/ds/transforms/cm_transforms
rsync -av $SNIC_TMP/ds/cm_transforms/data /proj/snic2018-3-380/runs/current/ds/transforms/cm_transforms
echo 'finished'