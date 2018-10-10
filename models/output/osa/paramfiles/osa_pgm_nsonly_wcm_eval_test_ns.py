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
output_table    = "osa_pgm_nsonly_wcm_eval_test_ns"

models = [
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_nsonly_wcm_eval_test_ns/pgm_nsonly_wcm_eval_test_logit_fullsample_ns",
    "estimator": SMLogit(),
    "features": [
      "l2_ged_dummy_ns",
      "l3_ged_dummy_ns",
      "l4_ged_dummy_ns",
      "l5_ged_dummy_ns",
      "l6_ged_dummy_ns",
      "l7_ged_dummy_ns",
      "l8_ged_dummy_ns",
      "l9_ged_dummy_ns",
      "l10_ged_dummy_ns",
      "l11_ged_dummy_ns",
      "l12_ged_dummy_ns",
      "q_1_1_l2_ged_dummy_ns",
      "q_1_1_l3_ged_dummy_ns",
      "l1_ged_dummy_ns",
      "decay_12_cw_ged_dummy_ns_0",
      "q_1_1_l1_ged_dummy_ns",
      "ln_dist_diamsec",
      "ln_dist_petroleum",
      "agri_ih_li",
      "barren_ih_li",
      "forest_ih_li",
      "mountains_mean",
      "savanna_ih_li",
      "shrub_ih_li",
      "pasture_ih_li",
      "urban_ih_li",
      "ln_bdist3",
      "ln_ttime",
      "ln_capdist",
      "ln_pop",
      "gcp_li_mer",
      "imr_mean",
      "excluded_dummy_li",
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "ln_fvp_timeindep",
      "ln_fvp_timesincepreindepwar",
      "ln_fvp_timesinceregimechange",
      "fvp_demo",
      "fvp_semi",
      "fvp_prop_excluded",
      "ln_fvp_population200",
      "ssp2_edu_sec_15_24_prop",
      "ssp2_urban_share_iiasa"
    ],
    "forecast_end": 456,
    "forecast_start": 421,
    "name": "pgm_nsonly_wcm_eval_test_logit_fullsample_ns",
    "outcome": "ged_dummy_ns",
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
    "train_end": 420,
    "train_start": 121
  },
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_nsonly_wcm_eval_test_ns/pgm_nsonly_wcm_eval_test_logit_downsampled_ns",
    "estimator": SMLogit(),
    "features": [
      "l2_ged_dummy_ns",
      "l3_ged_dummy_ns",
      "l4_ged_dummy_ns",
      "l5_ged_dummy_ns",
      "l6_ged_dummy_ns",
      "l7_ged_dummy_ns",
      "l8_ged_dummy_ns",
      "l9_ged_dummy_ns",
      "l10_ged_dummy_ns",
      "l11_ged_dummy_ns",
      "l12_ged_dummy_ns",
      "q_1_1_l2_ged_dummy_ns",
      "q_1_1_l3_ged_dummy_ns",
      "l1_ged_dummy_ns",
      "decay_12_cw_ged_dummy_ns_0",
      "q_1_1_l1_ged_dummy_ns",
      "ln_dist_diamsec",
      "ln_dist_petroleum",
      "agri_ih_li",
      "barren_ih_li",
      "forest_ih_li",
      "mountains_mean",
      "savanna_ih_li",
      "shrub_ih_li",
      "pasture_ih_li",
      "urban_ih_li",
      "ln_bdist3",
      "ln_ttime",
      "ln_capdist",
      "ln_pop",
      "gcp_li_mer",
      "imr_mean",
      "excluded_dummy_li",
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "ln_fvp_timeindep",
      "ln_fvp_timesincepreindepwar",
      "ln_fvp_timesinceregimechange",
      "fvp_demo",
      "fvp_semi",
      "fvp_prop_excluded",
      "ln_fvp_population200",
      "ssp2_edu_sec_15_24_prop",
      "ssp2_urban_share_iiasa"
    ],
    "forecast_end": 456,
    "forecast_start": 421,
    "name": "pgm_nsonly_wcm_eval_test_logit_downsampled_ns",
    "outcome": "ged_dummy_ns",
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
    "train_end": 420,
    "train_start": 121
  },
  {
    "dir_pickles": "$SNIC_TMP/osa/pickles/osa_pgm_nsonly_wcm_eval_test_ns/pgm_nsonly_wcm_eval_test_rf_downsampled_ns",
    "estimator": pipe_rf_500,
    "features": [
      "l2_ged_dummy_ns",
      "l3_ged_dummy_ns",
      "l4_ged_dummy_ns",
      "l5_ged_dummy_ns",
      "l6_ged_dummy_ns",
      "l7_ged_dummy_ns",
      "l8_ged_dummy_ns",
      "l9_ged_dummy_ns",
      "l10_ged_dummy_ns",
      "l11_ged_dummy_ns",
      "l12_ged_dummy_ns",
      "q_1_1_l2_ged_dummy_ns",
      "q_1_1_l3_ged_dummy_ns",
      "l1_ged_dummy_ns",
      "decay_12_cw_ged_dummy_ns_0",
      "q_1_1_l1_ged_dummy_ns",
      "ln_dist_diamsec",
      "ln_dist_petroleum",
      "agri_ih_li",
      "barren_ih_li",
      "forest_ih_li",
      "mountains_mean",
      "savanna_ih_li",
      "shrub_ih_li",
      "pasture_ih_li",
      "urban_ih_li",
      "ln_bdist3",
      "ln_ttime",
      "ln_capdist",
      "ln_pop",
      "gcp_li_mer",
      "imr_mean",
      "excluded_dummy_li",
      "fvp_lngdpcap_nonoilrent",
      "fvp_lngdpcap_oilrent",
      "fvp_grgdpcap_oilrent",
      "fvp_grgdpcap_nonoilrent",
      "ln_fvp_timeindep",
      "ln_fvp_timesincepreindepwar",
      "ln_fvp_timesinceregimechange",
      "fvp_demo",
      "fvp_semi",
      "fvp_prop_excluded",
      "ln_fvp_population200",
      "ssp2_edu_sec_15_24_prop",
      "ssp2_urban_share_iiasa"
    ],
    "forecast_end": 456,
    "forecast_start": 421,
    "name": "pgm_nsonly_wcm_eval_test_rf_downsampled_ns",
    "outcome": "ged_dummy_ns",
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
    "train_end": 420,
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