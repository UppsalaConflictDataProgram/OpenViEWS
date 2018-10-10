#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/descriptive


python -u plot_table.py\
    --schema landed\
    --table ensemble_cm_eval_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ensemble_cm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table ensemble_cm_fcast_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ensemble_cm_fcast_test.log &

python -u plot_table.py\
    --schema landed\
    --table calibrated_cm_eval_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/calibrated_cm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table calibrated_cm_fcast_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/calibrated_cm_fcast_test.log &

wait

python -u plot_table.py\
    --schema landed\
    --table ds_cm_eval_calib\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_cm_eval_calib.log &

python -u plot_table.py\
    --schema landed\
    --table ds_cm_eval_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_cm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table ds_cm_fcast_calib\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_cm_fcast_calib.log &

python -u plot_table.py\
    --schema landed\
    --table ds_cm_fcast_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_cm_fcast_test.log &

wait

python -u plot_table.py\
    --schema landed\
    --table osa_cm_eval_calib\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_cm_eval_calib.log &

python -u plot_table.py\
    --schema landed\
    --table osa_cm_eval_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_cm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table osa_cm_fcast_calib\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_cm_fcast_calib.log &

python -u plot_table.py\
    --schema landed\
    --table osa_cm_fcast_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_cm_fcast_test.log &

wait

python -u plot_table.py\
    --schema landed\
    --table agg_cm_eval_calib\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/agg_cm_eval_calib.log &

python -u plot_table.py\
    --schema landed\
    --table agg_cm_eval_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/agg_cm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table agg_cm_fcast_calib\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/agg_cm_fcast_calib.log &

python -u plot_table.py\
    --schema landed\
    --table agg_cm_fcast_test\
    --groupvar country_id\
    --timevar month_id\
    --lpgwa\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/agg_cm_fcast_test.log &
