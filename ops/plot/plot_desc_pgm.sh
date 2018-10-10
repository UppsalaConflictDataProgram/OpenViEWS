#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/descriptive

python -u plot_table.py\
    --schema landed\
    --table ensemble_pgm_eval_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ensemble_pgm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table ensemble_pgm_fcast_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ensemble_pgm_fcast_test.log &

python -u plot_table.py\
    --schema landed\
    --table calibrated_pgm_eval_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/calibrated_pgm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table calibrated_pgm_fcast_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/calibrated_pgm_fcast_tes.log &

wait

python -u plot_table.py\
    --schema landed\
    --table ds_pgm_eval_calib\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_pgm_eval_calib.log &

python -u plot_table.py\
    --schema landed\
    --table ds_pgm_eval_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_pgm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table ds_pgm_fcast_calib\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_pgm_fcast_calib.log &

python -u plot_table.py\
    --schema landed\
    --table ds_pgm_fcast_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ds_pgm_fcast_test.log &

wait

python -u plot_table.py\
    --schema landed\
    --table osa_pgm_eval_calib\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_pgm_eval_calib.log &

python -u plot_table.py\
    --schema landed\
    --table osa_pgm_eval_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_pgm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table osa_pgm_fcast_calib\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_pgm_fcast_calib.log &

python -u plot_table.py\
    --schema landed\
    --table osa_pgm_fcast_test\
    --groupvar pg_id\
    --timevar month_id\
    --wawa\
    2>&1 | tee $DIR_LOGS_DESCRIPTIVE/osa_pgm_fcast_test.log &

wait

echo "Finished desc pgm"