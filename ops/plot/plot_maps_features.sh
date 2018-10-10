#!/bin/bash
source ../config.sh

cd $DIR_GITHUB/plot/maps

python -u $DIR_GITHUB/plot/maps/plot_table.py\
    --schema landed\
    --table rescaled_pgm\
    --timevar month_id\
    --groupvar pg_id\
    --crop africa\
    --scale interval\
    --run_id $RUN_ID &

python -u $DIR_GITHUB/plot/maps/plot_cols.py\
    --schema launched\
    --table transforms_pgm_imp_1\
    --timevar month_id\
    --groupvar pg_id\
    --crop africa\
    --plotvar decay_12_cw_acled_dummy_pr_0\
    --plotvar decay_12_cw_ged_dummy_sb_0\
    --plotvar decay_12_cw_ged_dummy_ns_0\
    --plotvar decay_12_cw_ged_dummy_os_0\
    --scale interval\
    --run_id $RUN_ID &

wait