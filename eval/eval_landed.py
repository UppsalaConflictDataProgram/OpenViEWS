import sys
import pandas as pd
import numpy as np
import json

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils

import utils as evalutils

uname    = "VIEWSADMIN"
prefix   = "postgresql"
db       = "views"
port     = "5432"
hostname = "VIEWSHOST"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

schema_pred = "landed"
schema_actuals = "preflight"

table_ds = "ds_pgm_eval_test"
table_osa = "osa_pgm_eval_test"
table_ebma = "ebma_pgm_eval_test"

table_actuals = "flight_pgm"

timevar = "month_id"
groupvar = "pg_id"
ids = [timevar, groupvar]

outcomes = ["ged_dummy_sb", "ged_dummy_ns", "ged_dummy_os", "acled_dummy_pr"]
outcomes_suffix = [outcome[-3:] for outcome in outcomes]

try:
    df_ds = dbutils.db_to_df(connectstring, schema_pred, table_ds)
    df_osa = dbutils.db_to_df(connectstring, schema_pred, table_osa)
    df_ebma = dbutils.db_to_df(connectstring, schema_pred, table_ebma)
    df_ds.set_index(ids, inplace=True)
    df_osa.set_index(ids, inplace=True)
    df_ebma.set_index(ids, inplace=True)

    t_start_ds = df_ds.index.get_level_values(timevar).min()
    t_start_osa = df_osa.index.get_level_values(timevar).min()
    t_start_ebma = df_ebma.index.get_level_values(timevar).min()
    t_end_ds = df_ds.index.get_level_values(timevar).max()
    t_end_osa = df_osa.index.get_level_values(timevar).max()
    t_end_ebma = df_ebma.index.get_level_values(timevar).max()

    start_same = t_start_ds == t_start_osa == t_start_ebma
    end_same = t_end_ds == t_end_osa == t_end_ebma
except:
    print ("Error")

    if not start_same and end_same:
        raise RuntimeError("The time indexes for ds, osa and ebma don't match")

    df = dbutils.db_to_df_limited(connectstring, 
        schema_actuals, table_actuals, columns=outcomes+ids, 
        timevar=timevar, groupvar=groupvar, tmin=t_start_ds, tmax=t_end_ds)

    df = df.merge(df_ds, left_index=True, right_index=True)
    df = df.merge(df_osa, left_index=True, right_index=True)
    df = df.merge(df_ebma, left_index=True, right_index=True)

    df.to_hdf("temp.hdf5", key='data')

cols = df.columns
cols = [col.replace("_eval_test", "") for col in cols]
cols = [col.replace("_pgm", "") for col in cols]
cols = [col.replace("_downsampled", "_dsmp") for col in cols]
cols = [col.replace("_fullsample", "_fsmp") for col in cols]
df.columns = cols



jobs = []
for outcome in outcomes:
    suffix = outcome[-3:]
    cols_pred = [col for col in df.columns if col[-3:]==suffix and col != outcome]
    cols_pred = sorted(cols_pred)
    job = {
        'outcome' : outcome,
        'suffix' : suffix,
        'cols_pred' : cols_pred
    }
    jobs.append(job)

for job in jobs:
    path = job['outcome'] + ".png"
    evalutils.plot_prs(path, df, job['outcome'], job['cols_pred'])
