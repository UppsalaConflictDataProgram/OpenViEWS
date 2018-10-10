import os
import sys

import pandas as pd

sys.path.insert(0, "../../..")

import views_utils.dbutils as dbutils
import osa.utils as osa

from common import (connectstring,
                         logit_canon_full_train_sb,
                         logit_canon_full_train_ns,
                         logit_canon_full_train_os,
                         logit_acled_full_train_sb,
                         logit_acled_full_train_ns,
                         logit_acled_full_train_os,
                         logit_canon_ones_train_sb,
                         logit_canon_ones_train_ns,
                         logit_canon_ones_train_os,
                         logit_acled_ones_train_sb,
                         logit_acled_ones_train_ns,
                         logit_acled_ones_train_os,
                         rf_canon_ones_train_sb,
                         rf_canon_ones_train_ns,
                         rf_canon_ones_train_os,
                         rf_acled_ones_train_sb,
                         rf_acled_ones_train_ns,
                         rf_acled_ones_train_os)


output_schema   = "landed"
output_table    = "osa_train"

models = [
    logit_canon_full_train_sb,
    logit_canon_full_train_ns,
    logit_canon_full_train_os,
    logit_acled_full_train_sb,
    logit_acled_full_train_ns,
    logit_acled_full_train_os,
    logit_canon_ones_train_sb,
    logit_canon_ones_train_ns,
    logit_canon_ones_train_os,
    logit_acled_ones_train_sb,
    logit_acled_ones_train_ns,
    logit_acled_ones_train_os,
    rf_canon_ones_train_sb,
    rf_canon_ones_train_ns,
    rf_canon_ones_train_os,
    rf_acled_ones_train_sb,
    rf_acled_ones_train_ns,
    rf_acled_ones_train_os
]

df_results = osa.forecast_many(models)

# Write forecast to db
dbutils.df_to_db(connectstring, 
    df_results, 
    output_schema, output_table,
    if_exists="replace", write_index=True)

print("test complete!")
