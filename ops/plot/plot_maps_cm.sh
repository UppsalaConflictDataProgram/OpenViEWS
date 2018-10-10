#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/maps

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

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table calibrated_cm_eval_test\
    --timevar month_id\
    --groupvar country_id\
    --table_actual flight_cm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/calibrated_cm_eval_test.log &

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table calibrated_cm_fcast_test\
    --timevar month_id\
    --groupvar country_id\
    --table_actual flight_cm\
    --crop africa\
    --run_id $RUN_ID\
    --scale logodds\
     2>&1 | tee $DIR_LOGS_MAPS/calibrated_cm_fcast_test.log &

wait

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_cm_eval_calib\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_cm_eval_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_cm_eval_test\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_cm_eval_test.log &


# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_cm_fcast_calib\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_cm_fcast_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table ds_cm_fcast_test\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/ds_cm_fcast_test.log &

# wait

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_cm_eval_calib\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_cm_eval_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_cm_eval_test\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_cm_eval_test.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_cm_fcast_calib\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_cm_fcast_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table osa_cm_fcast_test\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/osa_cm_fcast_test.log &

# wait

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table agg_cm_eval_calib\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/agg_cm_eval_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table agg_cm_eval_test\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/agg_cm_eval_test.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table agg_cm_fcast_calib\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/agg_cm_fcast_calib.log &

# python -u $DIR_GITHUB/plot/maps/plot_table.py\
#     --schema landed\
#     --table agg_cm_fcast_test\
#     --timevar month_id\
#     --groupvar country_id\
#     --table_actual flight_cm\
#     --crop africa\
#     --run_id $RUN_ID\
#     --scale logodds\
#      2>&1 | tee $DIR_LOGS_MAPS/agg_cm_fcast_test.log &

# wait

echo "Finished maps cm"