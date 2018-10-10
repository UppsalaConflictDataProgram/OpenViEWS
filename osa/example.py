import os
import sys 

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils
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
output_table    = "osa_cm_eval_test"

models = [
  {
    "name": "cm_canon_base_eval_test_rf_downsampled_sb",
    "estimator": pipe_rf_500,
    "outcome": "ged_dummy_sb",
    "features": [
      "l2_ged_dummy_sb",
      "l3_ged_dummy_sb",
      "l4_ged_dummy_sb",
      "l5_ged_dummy_sb",
      "l6_ged_dummy_sb",
      "l7_ged_dummy_sb",
      "l8_ged_dummy_sb",
      "l9_ged_dummy_sb",
      "l10_ged_dummy_sb",
      "l11_ged_dummy_sb",
      "l12_ged_dummy_sb",
      "l1_ged_dummy_sb",
      "l1_ged_dummy_ns",
      "l1_ged_dummy_os",
      "decay_12_cw_ged_dummy_sb_0",
      "decay_12_cw_ged_dummy_ns_0",
      "decay_12_cw_ged_dummy_os_0",
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "ln_fvp_population200",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "ln_fvp_timeindep",
      "ln_fvp_timesincepreindepwar",
      "ln_fvp_timesinceregimechange",
      "fvp_demo",
      "fvp_semi",
      "ssp2_edu_sec_15_24_prop",
      "fvp_prop_excluded",
      "ssp2_urban_share_iiasa"
    ],
    "steps": [
      1,
      6,
      12,
      24,
      36
    ],
    "share_zeros_keep": 0.1,
    "share_ones_keep": 1,
    "train_start": 121,
    "train_end": 420,
    "forecast_start": 421,
    "forecast_end": 456,
    "table": {
      "connectstring": connectstring,
      "schema": "launched",
      "table": "transforms_cm_imp_1",
      "timevar": "month_id",
      "groupvar": "country_id"
    }
  }
]

df_results = osa.forecast_many(models)

# Write forecast to db
dbutils.df_to_db(connectstring, 
    df_results, 
    output_schema, output_table,
    if_exists="replace", write_index=True)

print("finished!")