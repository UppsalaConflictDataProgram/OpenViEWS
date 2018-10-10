import os
import sys

import pandas as pd

sys.path.append("..")

import views_utils.dbutils as dbutils

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST",
                                           port="5432", prefix="postgres",
                                           uname="VIEWSADMIN")


schema = "previous"
if_exists = "replace"

# set index on
ids_cm = ["month_id", "country_id"]
ids_pgm = ["month_id", "pg_id"]

# inserts
tables = ["ensemble_cm_fcast_test", "ensemble_cm_eval_test",
          "ensemble_pgm_fcast_test", "ensemble_pgm_eval_test"]

# ensemble
for table in tables:
    path = f"/storage/runs/archive/r.2018.08.01/ensemble/results/{table}.hdf5"
    df_prev = pd.read_hdf(path)
    # set index
    if "cm" in table:
        df_prev.set_index(ids_cm, inplace=True)
    if "pgm" in table:
        df_prev.set_index(ids_pgm, inplace=True)
    # push table
    dbutils.df_to_db(connectstring, df_prev, schema, table, if_exists, write_index=True)

#decay
for level in ["cm", "pgm"]:
    path = f"/storage/runs/archive/r.2018.08.01/ds/transforms/{level}_transforms/data/{level}_imp_1.hdf5"
    table = f"transforms_{level}_imp_1"
    df_prev = pd.read_hdf(path)
    # isolate the decay columns
    cols = [col for col in df_prev if "decay" in col]
    if level == "cm":
        df_prev = df_prev[cols]
    if level == "pgm":
        df_prev = df_prev[cols]
    # push table
    dbutils.df_to_db(connectstring, df_prev, schema, table, if_exists, write_index=True)
