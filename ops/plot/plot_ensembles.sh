#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/maps

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table ensemble_pgm_eval_test\
    --timevar month_id\
    --groupvar pg_id\
    --table_actual flight_pgm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/ensemble_pgm_eval_test.log &

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table ensemble_pgm_fcast_test\
    --timevar month_id\
    --groupvar pg_id\
    --table_actual flight_pgm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/ensemble_pgm_fcast_test.log &

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table ensemble_cm_eval_test\
    --timevar month_id\
    --groupvar country_id\
    --table_actual flight_cm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/ensemble_cm_eval_test.log &

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table ensemble_cm_fcast_test\
    --timevar month_id\
    --groupvar country_id\
    --table_actual flight_cm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/ensemble_cm_fcast_test.log &


wait

echo "Finished maps ensembles"

