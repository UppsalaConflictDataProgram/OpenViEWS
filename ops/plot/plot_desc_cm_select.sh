#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/descriptive


python -u plot_table.py\
    --schema landed\
    --table ensemble_cm_eval_test\
    --groupvar country_id\
    --timevar month_id\
    --schema_actuals launched\
    --table_actuals transforms_cm_imp_1\
    --wawa\
 2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ensemble_cm_eval_test.log &

python -u plot_table.py\
    --schema landed\
    --table ensemble_cm_fcast_test\
    --groupvar country_id\
    --timevar month_id\
    --schema_actuals launched\
    --table_actuals transforms_cm_imp_1\
    --wawa\
 2>&1 | tee $DIR_LOGS_DESCRIPTIVE/ensemble_cm_fcast_test.log &

 wait
