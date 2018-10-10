import os
import sys

import pandas as pd
import numpy as np

from run1_features import ( features_canon_sb, features_canon_ns, 
    features_canon_os, features_acled_sb, 
    features_acled_ns, features_acled_os)

sys.path.insert(0, "../..")

import views_utils.dbutils as dbutils
import nstep.utils as nstep

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier




# db parameters
uname    = "VIEWSADMIN"
prefix   = "postgresql"
db       = "views"
port     = "5432"
hostname = "VIEWSHOST"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

output_schema   = "landed"
output_table    = "step_run1_rf_ones_test"

table_input = {
    'connectstring' : connectstring,
    'schema'    : 'launched',
    'table'     : 'ds_w_acled',
    'timevar'   : 'month_id',
    'groupvar'  : 'pg_id'
}

share_zeros = 0.1
share_ones = 1
steps = [1, 6, 12, 24, 36]

rf_500 =  RandomForestClassifier(n_estimators = 500)
scaler =  StandardScaler()


pipe_rf_500 = Pipeline([
    ('scaler', scaler),
    ('rf', rf_500)
])

rf_canon_ones_calib_sb = {
    'name' : 'rf_canon_ones_calib_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  121,
    'train_end' :  372,
    'forecast_start' :  373,
    'forecast_end' :  408,
    'table' : table_input}

rf_canon_ones_calib_ns = {
    'name' : 'rf_canon_ones_calib_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  121,
    'train_end' :  372,
    'forecast_start' :  373,
    'forecast_end' :  408,
    'table' : table_input}

rf_canon_ones_calib_os = {
    'name' : 'rf_canon_ones_calib_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  121,
    'train_end' :  372,
    'forecast_start' :  373,
    'forecast_end' :  408,
    'table' : table_input}



rf_canon_ones_test_sb = {
    'name' : 'rf_canon_ones_test_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  121,
    'train_end' :  408,
    'forecast_start' :  409,
    'forecast_end' :  444,
    'table' : table_input}

rf_canon_ones_test_ns = {
    'name' : 'rf_canon_ones_test_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  121,
    'train_end' :  408,
    'forecast_start' :  409,
    'forecast_end' :  444,
    'table' : table_input}

rf_canon_ones_test_os = {
    'name' : 'rf_canon_ones_test_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  121,
    'train_end' :  408,
    'forecast_start' :  409,
    'forecast_end' :  444,
    'table' : table_input}



rf_acled_ones_calib_sb = {
    'name' : 'rf_acled_ones_calib_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  205,
    'train_end' :  372,
    'forecast_start' :  373,
    'forecast_end' :  408,
    'table' : table_input}

rf_acled_ones_calib_ns = {
    'name' : 'rf_acled_ones_calib_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  205,
    'train_end' :  372,
    'forecast_start' :  373,
    'forecast_end' :  408,
    'table' : table_input}

rf_acled_ones_calib_os = {
    'name' : 'rf_acled_ones_calib_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  205,
    'train_end' :  372,
    'forecast_start' :  373,
    'forecast_end' :  408,
    'table' : table_input}


rf_acled_ones_test_sb = {
    'name' : 'rf_acled_ones_test_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  205,
    'train_end' :  408,
    'forecast_start' :  409,
    'forecast_end' :  444,
    'table' : table_input}

rf_acled_ones_test_ns = {
    'name' : 'rf_acled_ones_test_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  205,
    'train_end' :  408,
    'forecast_start' :  409,
    'forecast_end' :  444,
    'table' : table_input}

rf_acled_ones_test_os = {
    'name' : 'rf_acled_ones_test_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros,
    'share_ones_keep' : share_ones,
    'train_start' :  205,
    'train_end' :  408,
    'forecast_start' :  409,
    'forecast_end' :  444,
    'table' : table_input}

models = [
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

print("VICTORY!")