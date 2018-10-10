import sys

import pandas as pd

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils


dir_results_osa = "/storage/runs/current/osa/results"
dir_results_ensemble = "/storage/runs/current/ensemble/results"
dir_results_agg = "/storage/runs/current/agg/results"
dir_results_cl = "/storage/runs/current/cl/results"
dir_results_calibrated = "/storage/runs/current/calibrated/results"


schema = "landed"
prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

tables_osa = [
    "osa_cm_eval_calib",
    "osa_cm_eval_test",
    "osa_cm_fcast_calib",
    "osa_cm_fcast_test",
    "osa_pgm_eval_calib",
    "osa_pgm_eval_test",
    "osa_pgm_fcast_calib",
    "osa_pgm_fcast_test"]

tables_ensemble = [
    "ensemble_pgm_fcast_test",
    "ensemble_pgm_eval_test",
    "ensemble_cm_fcast_test",
    "ensemble_cm_eval_test",
    ]

tables_agg = ["agg_cm_eval_test",
              "agg_cm_eval_calib",
              "agg_cm_fcast_test",
              "agg_cm_fcast_calib"]

tables_cl = ["cl_pgm_eval_calib",
             "cl_pgm_eval_test",
             "cl_pgm_fcast_calib",
             "cl_pgm_fcast_test"]

tables_calibrated = ["calibrated_cm_eval_test",
                     "calibrated_cm_fcast_test",
                     "calibrated_pgm_eval_test",
                     "calibrated_pgm_fcast_test",]



for table in tables_osa:
    path = dir_results_osa + "/" + table + ".hdf5"
    df = dbutils.db_to_df(connectstring, schema, table)
    df.to_hdf(path, key='data', complevel=9)
    print("wrote", path)

for table in tables_ensemble:
    path = dir_results_ensemble + "/" + table + ".hdf5"
    df = dbutils.db_to_df(connectstring, schema, table)
    df.to_hdf(path, key='data', complevel=9)
    print("wrote", path)

for table in tables_agg:
    path = dir_results_agg + "/" + table + ".hdf5"
    df = dbutils.db_to_df(connectstring, schema, table)
    df.to_hdf(path, key='data', complevel=9)
    print("wrote", path)

for table in tables_cl:
    path = dir_results_cl + "/" + table + ".hdf5"
    df = dbutils.db_to_df(connectstring, schema, table)
    df.to_hdf(path, key='data', complevel=9)
    print("wrote", path)

for table in tables_calibrated:
    path = dir_results_calibrated + "/" + table + ".hdf5"
    df = dbutils.db_to_df(connectstring, schema, table)
    df.to_hdf(path, key='data', complevel=9)
    print("wrote", path)
