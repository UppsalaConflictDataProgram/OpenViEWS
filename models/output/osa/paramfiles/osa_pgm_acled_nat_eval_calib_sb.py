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
output_table    = "osa_pgm_acled_nat_eval_calib_sb"

models = [
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_acled_nat_eval_calib_sb/pgm_acled_nat_eval_calib_logit_fullsample_sb",
    "estimator": SMLogit(),
    "features": [
      "ln_dist_diamsec",
      "ln_dist_petroleum",
      "agri_ih_li",
      "barren_ih_li",
      "forest_ih_li",
      "mountains_mean",
      "savanna_ih_li",
      "shrub_ih_li",
      "pasture_ih_li",
      "urban_ih_li"
    ],
    "forecast_end": 420,
    "forecast_start": 385,
    "name": "pgm_acled_nat_eval_calib_logit_fullsample_sb",
    "outcome": "ged_dummy_sb",
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
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_acled_nat_eval_calib_sb/pgm_acled_nat_eval_calib_logit_downsampled_sb",
    "estimator": SMLogit(),
    "features": [
      "ln_dist_diamsec",
      "ln_dist_petroleum",
      "agri_ih_li",
      "barren_ih_li",
      "forest_ih_li",
      "mountains_mean",
      "savanna_ih_li",
      "shrub_ih_li",
      "pasture_ih_li",
      "urban_ih_li"
    ],
    "forecast_end": 420,
    "forecast_start": 385,
    "name": "pgm_acled_nat_eval_calib_logit_downsampled_sb",
    "outcome": "ged_dummy_sb",
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
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_acled_nat_eval_calib_sb/pgm_acled_nat_eval_calib_rf_downsampled_sb",
    "estimator": pipe_rf_500,
    "features": [
      "ln_dist_diamsec",
      "ln_dist_petroleum",
      "agri_ih_li",
      "barren_ih_li",
      "forest_ih_li",
      "mountains_mean",
      "savanna_ih_li",
      "shrub_ih_li",
      "pasture_ih_li",
      "urban_ih_li"
    ],
    "forecast_end": 420,
    "forecast_start": 385,
    "name": "pgm_acled_nat_eval_calib_rf_downsampled_sb",
    "outcome": "ged_dummy_sb",
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
