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
    --table calibrated_pgm_eval_test\
    --timevar month_id\
    --groupvar pg_id\
    --table_actual flight_pgm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/calibrated_pgm_eval_test.log &

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table calibrated_pgm_fcast_test\
    --timevar month_id\
    --groupvar pg_id\
    --table_actual flight_pgm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/calibrated_pgm_fcast_test.log &

wait

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_pgm_eval_calib\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_pgm_eval_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_pgm_eval_test\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_pgm_eval_test.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_pgm_fcast_calib\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_pgm_fcast_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_pgm_fcast_test\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_pgm_fcast_test.log &

# wait

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_pgm_eval_calib\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_pgm_eval_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_pgm_eval_test\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_pgm_eval_test.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_pgm_fcast_calib\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_pgm_fcast_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_pgm_fcast_test\
#     --timevar month_id\
#     --groupvar pg_id\
#     --table_actual flight_pgm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_pgm_fcast_test.log &

wait

echo "Finished maps pgm"

