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
output_table    = "osa_cm_canon_meaneco_fcast_test_os"

models = [
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_cm_canon_meaneco_fcast_test_os/cm_canon_meaneco_fcast_test_logit_fullsample_os",
    "estimator": SMLogit(),
    "features": [
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "mean_ged_dummy_os_fcast_test"
    ],
    "forecast_end": 502,
    "forecast_start": 465,
    "name": "cm_canon_meaneco_fcast_test_logit_fullsample_os",
    "outcome": "ged_dummy_os",
    "share_ones_keep": 1,
    "share_zeros_keep": 1,
    "steps": [
      1,
      6,
      12,
      24,
      36,
      38
    ],
    "table": {
      "connectstring": "postgresql://VIEWSADMIN@VIEWSHOST:5432/views",
      "groupvar": "country_id",
      "schema": "launched",
      "table": "transforms_cm_imp_1",
      "timevar": "month_id"
    },
    "train_end": 464,
    "train_start": 121
  },
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_cm_canon_meaneco_fcast_test_os/cm_canon_meaneco_fcast_test_logit_downsampled_os",
    "estimator": SMLogit(),
    "features": [
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "mean_ged_dummy_os_fcast_test"
    ],
    "forecast_end": 502,
    "forecast_start": 465,
    "name": "cm_canon_meaneco_fcast_test_logit_downsampled_os",
    "outcome": "ged_dummy_os",
    "share_ones_keep": 1,
    "share_zeros_keep": 0.1,
    "steps": [
      1,
      6,
      12,
      24,
      36,
      38
    ],
    "table": {
      "connectstring": "postgresql://VIEWSADMIN@VIEWSHOST:5432/views",
      "groupvar": "country_id",
      "schema": "launched",
      "table": "transforms_cm_imp_1",
      "timevar": "month_id"
    },
    "train_end": 464,
    "train_start": 121
  },
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_cm_canon_meaneco_fcast_test_os/cm_canon_meaneco_fcast_test_rf_downsampled_os",
    "estimator": pipe_rf_500,
    "features": [
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "mean_ged_dummy_os_fcast_test"
    ],
    "forecast_end": 502,
    "forecast_start": 465,
    "name": "cm_canon_meaneco_fcast_test_rf_downsampled_os",
    "outcome": "ged_dummy_os",
    "share_ones_keep": 1,
    "share_zeros_keep": 0.1,
    "steps": [
      1,
      6,
      12,
      24,
      36,
      38
    ],
    "table": {
      "connectstring": "postgresql://VIEWSADMIN@VIEWSHOST:5432/views",
      "groupvar": "country_id",
      "schema": "launched",
      "table": "transforms_cm_imp_1",
      "timevar": "month_id"
    },
    "train_end": 464,
    "train_start": 121
  }
]

df_results = osa.forecast_many(models)

# Write forecast to db
dbutils.df_to_db(connectstring,
    df_results,
    output_schema, output_table,
    if_exists="replace", write_index=True)

print("finished!")
