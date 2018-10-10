#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/maps
python -u $DIR_GITHUB/plot/maps/plot_cols.py\
    --schema launched\
    --table transforms_cm_imp_1\
    --timevar month_id\
    --groupvar country_id\
    --crop africa\
    --plotvar decay_12_cw_acled_dummy_pr_0\
    --plotvar decay_12_cw_ged_dummy_sb_0\
    --plotvar decay_12_cw_ged_dummy_ns_0\
    --plotvar decay_12_cw_ged_dummy_os_0\
    --scale interval\
    --run_id $RUN_ID


python -u $DIR_GITHUB/plot/maps/plot_cols.py\
    --schema launched\
    --table transforms_cm_imp_1\
    --timevar month_id\
    --groupvar country_id\
    --crop africa\
    --plotvar ln_fvp_population200\
    --run_id $RUN_ID\
    --scale interval\

