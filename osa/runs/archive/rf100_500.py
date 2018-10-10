
# coding: utf-8

# # N-STEP demo
# 
# ## Quickstart:
# 
# * Change uname to your db username
# * Run all the cells
# * Make coffee
# * Check the table landed_test.nstep_notebook in the database
# 
# ## Overview
# This notebook contains an example of how to use the N-step ahead forecasting tools.
# The models are terrible, they are just an illustration. 
# Everything is based around the model dictionaries. 
# 
# A model dictionary contains all the information of a forecast:
# 
# * outcome
# * list of features
# * estimator object (Usually a scikit Pipeline)
# * time limits for training and forecasting
# * which time steps to forecast for
# * which input table to use
# * downsampling factors for y=1 and y=0
# 
# The nstep.forecast_many() method is the key component:
# given a list of model dictionaries it returns a dataframe of forecasted values.
# 
# 
# It does:
# 
# * Reading from database
# * Fitting the model for each step
# * Forecasting for each step, both predicted probs and predicted outcomes (discrete)
# * Interpolate between the steps
# * Merging the forecast of many models to one dataframe
# 
# For each model 5 columns go into the database
# 
# * actual_model : The actual value of the outcome
# * model : predicted value from the model, usually binary (predict())
# * p_model : predicted probability (predict_proba())
# * model_li : linear interpolation of predicted value
# * p_model_li : linear prediction of predicted probability
# 
# The last cell then writes these predictions to the specified output table using 
# dbutils.df_to_db().
# 



import os
import sys

import pandas as pd
import numpy as np

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

output_schema   = "landed_test"
output_table    = "nstep_notebook"

# specify as many as you want
table_input = {
    'connectstring' : connectstring,
    'schema'    : 'launched',
    'table'     : 'imp_imp_1',
    'timevar'   : 'month_id',
    'groupvar'  : 'pg_id'
}

table_input_noimp = {
    'connectstring' : connectstring,
    'schema'    : 'preflight',
    'table'     : 'flight_pgm',
    'timevar'   : 'month_id',
    'groupvar'  : 'pg_id'
}




# Following vars had missingness, dropped
# excluded, bdist1, ssp2_gdppercap_oecd, ssp2_gdppercap_iiasa, acled_count_pr
features_all = ["ged_dummy_sb",
"ged_dummy_ns",
"ged_dummy_os",
"col",
"row",
"latitude",
"longitude",
"cmr_max",
"cmr_mean",
"cmr_min",
"cmr_sd",
"diamprim_s",
"diamsec_s",
"gem_s",
"goldplacer_s",
"goldvein_s",
"goldsurface_s",
"petroleum_s",
"ttime_max",
"ttime_mean",
"ttime_min",
"ttime_sd",
"mountains_mean",
"imr_max",
"imr_mean",
"imr_min",
"rainseas",
"growstart",
"dist_diaprim_s_wgs",
"dist_diamsec_s_wgs",
"dist_petroleum_s_wgs",
"dist_goldsurface_s_wgs",
"dist_goldplace_s_wgs",
"dist_goldvein_s_wgs",
"dist_gem_s_wgs",
"growend",
"pop_li_gpw_sum",
"gcp_li_mer",
"droughtcrop_speibase",
"droughtcrop_speigdm",
"droughtyr_speibase",
"droughtyr_speigdm",
"droughtstart_speibase",
"droughtstart_speigdm",
"agri_ih_li",
"barren_ih_li",
"forest_ih_li",
"grass_ih_li",
"savanna_ih_li",
"pasture_ih_li",
"shrub_ih_li",
"urban_ih_li",
"bdist2",
"bdist3",
"nlights_mean",
"nlights_calib_mean",
"bdist1_li",
"capdist_li",
"fvp_polity2",
"v2x_libdem",
"v2x_polyarchy_li",
"fvp_lngdp200_li",
"fvp_population200_li",
"ged_dummy_sb_tlag1",
"ged_dummy_sb_tlag2",
"ged_dummy_sb_tlag3",
"ged_dummy_sb_tlag4",
"ged_dummy_sb_tlag5",
"ged_dummy_sb_tlag6",
"ged_dummy_sb_tlag7",
"ged_dummy_sb_tlag8",
"ged_dummy_sb_tlag9",
"ged_dummy_sb_tlag10",
"ged_dummy_sb_tlag11",
"ged_dummy_sb_tlag12",
"ged_dummy_ns_tlag1",
"ged_dummy_ns_tlag2",
"ged_dummy_ns_tlag3",
"ged_dummy_ns_tlag4",
"ged_dummy_ns_tlag5",
"ged_dummy_ns_tlag6",
"ged_dummy_ns_tlag7",
"ged_dummy_ns_tlag8",
"ged_dummy_ns_tlag9",
"ged_dummy_ns_tlag10",
"ged_dummy_ns_tlag11",
"ged_dummy_ns_tlag12",
"ged_dummy_os_tlag1",
"ged_dummy_os_tlag2",
"ged_dummy_os_tlag3",
"ged_dummy_os_tlag4",
"ged_dummy_os_tlag5",
"ged_dummy_os_tlag6",
"ged_dummy_os_tlag7",
"ged_dummy_os_tlag8",
"ged_dummy_os_tlag9",
"ged_dummy_os_tlag10",
"ged_dummy_os_tlag11",
"ged_dummy_os_tlag12"]




# RF
rf1 =  RandomForestClassifier(n_estimators = 100)
scaler =  StandardScaler()


pipeline1 = Pipeline([
    ('scaler', scaler),
    ('rf', rf1)
])



rf_100 = { 
        'name'      : 'rf_100',
        'outcome'   : 'ged_dummy_sb',
        'estimator' : pipeline1,
        'features'  : features_all,
        'steps'     : [1, 12, 36],
        'share_zeros_keep'  : 0.1,
        'share_ones_keep'   : 0.1,
        'train_start'   : 150,
        'train_end'     : 408,
        'forecast_start': 409,
        'forecast_end'  : 444,
        'table' : table_input
        }




# RF
rf2 =  RandomForestClassifier(n_estimators = 250)
scaler =  StandardScaler()


pipeline2 = Pipeline([
    ('scaler', scaler),
    ('rf', rf2)
])



rf_250 = { 
        'name'      : 'rf_250',
        'outcome'   : 'ged_dummy_sb',
        'estimator' : pipeline2,
        'features'  : features_all,
        'steps'     : [1, 12, 36],
        'share_zeros_keep'  : 0.1,
        'share_ones_keep'   : 0.1,
        'train_start'   : 150,
        'train_end'     : 408,
        'forecast_start': 409,
        'forecast_end'  : 444,
        'table' : table_input
        }




# RF
rf3 =  RandomForestClassifier(n_estimators = 500)
scaler =  StandardScaler()


pipeline3 = Pipeline([
    ('scaler', scaler),
    ('rf', rf3)
])



rf_500 = { 
        'name'      : 'rf_500',
        'outcome'   : 'ged_dummy_sb',
        'estimator' : pipeline3,
        'features'  : features_all,
        'steps'     : [1, 12, 36],
        'share_zeros_keep'  : 0.1,
        'share_ones_keep'   : 0.1,
        'train_start'   : 150,
        'train_end'     : 408,
        'forecast_start': 409,
        'forecast_end'  : 444,
        'table' : table_input
        }




# Forecast the models
models = [rf_100, rf_250, rf_500]
df_results = nstep.forecast_many(models)




# Write forecast to db
dbutils.df_to_db(connectstring, df_results, output_schema, output_table, 
    if_exists="replace", write_index=True)

