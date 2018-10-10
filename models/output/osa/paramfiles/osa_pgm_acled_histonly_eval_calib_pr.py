import os
import sys

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, "../../../../")
import views_utils.dbutils as dbutils
sys.path.insert(0, "../../../osa")
from osa.wrapper_sm import SMLogit

import osa.utils as osa

uname    = "VIEWSADMIN"
prefix   = "postgresql"
db       = "views"
port     = "5432"
hostname = "VIEWSHOST"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

rf_500 =  RandomForestClassifier(n_estimators = 500, n_jobs=10)
scaler =  StandardScaler()
pipe_rf_500 = Pipeline([
    ('scaler', scaler),
    ('rf', rf_500)])

output_schema   = "landed_test"
output_table    = "osa_pgm_acled_histonly_eval_calib_pr"

models = [
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_acled_histonly_eval_calib_pr/pgm_acled_histonly_eval_calib_logit_fullsample_pr",
    "estimator": SMLogit(),
    "features": [
      "l2_acled_dummy_pr",
      "l3_acled_dummy_pr",
      "l4_acled_dummy_pr",
      "l5_acled_dummy_pr",
      "l6_acled_dummy_pr",
      "l7_acled_dummy_pr",
      "l8_acled_dummy_pr",
      "l9_acled_dummy_pr",
      "l10_acled_dummy_pr",
      "l11_acled_dummy_pr",
      "l12_acled_dummy_pr",
      "q_1_1_l2_acled_dummy_pr",
      "q_1_1_l3_acled_dummy_pr",
      "l1_ged_dummy_sb",
      "l1_ged_dummy_ns",
      "l1_ged_dummy_os",
      "l1_acled_dummy_pr",
      "decay_12_cw_ged_dummy_sb_0",
      "decay_12_cw_ged_dummy_ns_0",
      "decay_12_cw_ged_dummy_os_0",
      "decay_12_cw_acled_dummy_pr_0",
      "q_1_1_l1_ged_dummy_sb",
      "q_1_1_l1_ged_dummy_ns",
      "q_1_1_l1_ged_dummy_os",
      "q_1_1_l1_acled_dummy_pr"
    ],
    "forecast_end": 420,
    "forecast_start": 385,
    "name": "pgm_acled_histonly_eval_calib_logit_fullsample_pr",
    "outcome": "acled_dummy_pr",
    "share_ones_keep": 1,
    "share_zeros_keep": 1,
    "steps": [
      1,
      6,
      12,
      24,
      36
    ],
    "table": {
      "connectstring": "postgresql://VIEWSADMIN@VIEWSHOST:5432/views",
      "groupvar": "pg_id",
      "schema": "launched",
      "table": "transforms_pgm_imp_1",
      "timevar": "month_id"
    },
    "train_end": 384,
    "train_start": 205
  },
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_acled_histonly_eval_calib_pr/pgm_acled_histonly_eval_calib_logit_downsampled_pr",
    "estimator": SMLogit(),
    "features": [
      "l2_acled_dummy_pr",
      "l3_acled_dummy_pr",
      "l4_acled_dummy_pr",
      "l5_acled_dummy_pr",
      "l6_acled_dummy_pr",
      "l7_acled_dummy_pr",
      "l8_acled_dummy_pr",
      "l9_acled_dummy_pr",
      "l10_acled_dummy_pr",
      "l11_acled_dummy_pr",
      "l12_acled_dummy_pr",
      "q_1_1_l2_acled_dummy_pr",
      "q_1_1_l3_acled_dummy_pr",
      "l1_ged_dummy_sb",
      "l1_ged_dummy_ns",
      "l1_ged_dummy_os",
      "l1_acled_dummy_pr",
      "decay_12_cw_ged_dummy_sb_0",
      "decay_12_cw_ged_dummy_ns_0",
      "decay_12_cw_ged_dummy_os_0",
      "decay_12_cw_acled_dummy_pr_0",
      "q_1_1_l1_ged_dummy_sb",
      "q_1_1_l1_ged_dummy_ns",
      "q_1_1_l1_ged_dummy_os",
      "q_1_1_l1_acled_dummy_pr"
    ],
    "forecast_end": 420,
    "forecast_start": 385,
    "name": "pgm_acled_histonly_eval_calib_logit_downsampled_pr",
    "outcome": "acled_dummy_pr",
    "share_ones_keep": 1,
    "share_zeros_keep": 0.1,
    "steps": [
      1,
      6,
      12,
      24,
      36
    ],
    "table": {
      "connectstring": "postgresql://VIEWSADMIN@VIEWSHOST:5432/views",
      "groupvar": "pg_id",
      "schema": "launched",
      "table": "transforms_pgm_imp_1",
      "timevar": "month_id"
    },
    "train_end": 384,
    "train_start": 205
  },
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_acled_histonly_eval_calib_pr/pgm_acled_histonly_eval_calib_rf_downsampled_pr",
    "estimator": pipe_rf_500,
    "features": [
      "l2_acled_dummy_pr",
      "l3_acled_dummy_pr",
      "l4_acled_dummy_pr",
      "l5_acled_dummy_pr",
      "l6_acled_dummy_pr",
      "l7_acled_dummy_pr",
      "l8_acled_dummy_pr",
      "l9_acled_dummy_pr",
      "l10_acled_dummy_pr",
      "l11_acled_dummy_pr",
      "l12_acled_dummy_pr",
      "q_1_1_l2_acled_dummy_pr",
      "q_1_1_l3_acled_dummy_pr",
      "l1_ged_dummy_sb",
      "l1_ged_dummy_ns",
      "l1_ged_dummy_os",
      "l1_acled_dummy_pr",
      "decay_12_cw_ged_dummy_sb_0",
      "decay_12_cw_ged_dummy_ns_0",
      "decay_12_cw_ged_dummy_os_0",
      "decay_12_cw_acled_dummy_pr_0",
      "q_1_1_l1_ged_dummy_sb",
      "q_1_1_l1_ged_dummy_ns",
      "q_1_1_l1_ged_dummy_os",
      "q_1_1_l1_acled_dummy_pr"
    ],
    "forecast_end": 420,
    "forecast_start": 385,
    "name": "pgm_acled_histonly_eval_calib_rf_downsampled_pr",
    "outcome": "acled_dummy_pr",
    "share_ones_keep": 1,
    "share_zeros_keep": 0.1,
    "steps": [
      1,
      6,
      12,
      24,
      36
    ],
    "table": {
      "connectstring": "postgresql://VIEWSADMIN@VIEWSHOST:5432/views",
      "groupvar": "pg_id",
      "schema": "launched",
      "table": "transforms_pgm_imp_1",
      "timevar": "month_id"
    },
    "train_end": 384,
    "train_start": 205
  }
]

df_results = osa.forecast_many(models)

# Write forecast to db
dbutils.df_to_db(connectstring,
    df_results,
    output_schema, output_table,
    if_exists="replace", write_index=True)

print("finished!")
