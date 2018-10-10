import os
import sys

import pandas as pd

sys.path.insert(0, "../../..")

import views_utils.dbutils as dbutils
import nstep.utils as nstep

from run1_common import (connectstring,
                         logit_canon_full_test_sb,
                         logit_canon_full_test_ns,
                         logit_canon_full_test_os,
                         logit_acled_full_test_sb,
                         logit_acled_full_test_ns,
                         logit_acled_full_test_os,
                         logit_canon_ones_test_sb,
                         logit_canon_ones_test_ns,
                         logit_canon_ones_test_os,
                         logit_acled_ones_test_sb,
                         logit_acled_ones_test_ns,
                         logit_acled_ones_test_os,
                         rf_canon_ones_test_sb,
                         rf_canon_ones_test_ns,
                         rf_canon_ones_test_os,
                         rf_acled_ones_test_sb,
                         rf_acled_ones_test_ns,
                         rf_acled_ones_test_os)


output_schema   = "landed"
output_table    = "step_run1_test"

models = [
    logit_canon_full_test_sb,
    logit_canon_full_test_ns,
    logit_canon_full_test_os,
    logit_acled_full_test_sb,
    logit_acled_full_test_ns,
    logit_acled_full_test_os,
    logit_canon_ones_test_sb,
    logit_canon_ones_test_ns,
    logit_canon_ones_test_os,
    logit_acled_ones_test_sb,
    logit_acled_ones_test_ns,
    logit_acled_ones_test_os,
    rf_canon_ones_test_sb,
    rf_canon_ones_test_ns,
    rf_canon_ones_test_os,
    rf_acled_ones_test_sb,
    rf_acled_ones_test_ns,
    rf_acled_ones_test_os
]

df_results = nstep.forecast_many(models)

# Write forecast to db
dbutils.df_to_db(connectstring, 
    df_results, 
    output_schema, output_table,
    if_exists="replace", write_index=True)

print("test complete!")
