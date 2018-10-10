#!/bin/bash -l
#SBATCH -A snic2018-3-380
#SBATCH -p core
#SBATCH -n 1


#SBATCH -t 8:00:00
#SBATCH -J maps_uppmax
#SBATCH -o /proj/snic2018-3-380/runs/current/maps/logs/maps_uppmax.log

source ../config.sh

cd $DIR_GITHUB/plot/maps

export PATH="/home/VIEWSADMIN/miniconda3/bin:$PATH"
source activate views_old

python -u $DIR_GITHUB/plot/maps/plot_table_uppmax.py\
    --schema landed\
    --table ensemble_cm_eval_test\
    --timevar month_id\
    --groupvar country_id\
    --table_actual flight_cm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds

