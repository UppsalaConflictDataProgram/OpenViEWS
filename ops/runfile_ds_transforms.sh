#!/bin/bash -l
#SBATCH -A snic2018-3-380
#SBATCH -p node

#SBATCH -t 12:00:00
#SBATCH -J push_ds_transforms
#SBATCH -o /home/VIEWSADMIN/github/Views/ops/push_ds_transforms.log


cd ~/github/Views/ops

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/pgm_transforms/data/pgm_imp_1.hdf5\
    --schema launched\
    --table transforms_pgm_imp_1 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/pgm_transforms/data/pgm_imp_2.hdf5\
    --schema launched\
    --table transforms_pgm_imp_2 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/pgm_transforms/data/pgm_imp_3.hdf5\
    --schema launched\
    --table transforms_pgm_imp_3 &\

wait

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/pgm_transforms/data/pgm_imp_4.hdf5\
    --schema launched\
    --table transforms_pgm_imp_4 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/pgm_transforms/data/pgm_imp_5.hdf5\
    --schema launched\
    --table transforms_pgm_imp_5 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/cm_transforms/data/cm_imp_1.hdf5\
    --schema launched\
    --table transforms_cm_imp_1 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/cm_transforms/data/cm_imp_2.hdf5\
    --schema launched\
    --table transforms_cm_imp_2 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/cm_transforms/data/cm_imp_3.hdf5\
    --schema launched\
    --table transforms_cm_imp_3 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/cm_transforms/data/cm_imp_4.hdf5\
    --schema launched\
    --table transforms_cm_imp_4 &\

python push_file_to_table.py\
    --path /home/VIEWSADMIN/proj/runs/current/ds/transforms/cm_transforms/data/cm_imp_5.hdf5\
    --schema launched\
    --table transforms_cm_imp_5 &\


wait
