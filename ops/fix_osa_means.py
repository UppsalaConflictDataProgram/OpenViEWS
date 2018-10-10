# This naughty script adds 4*4 columns to all the datasets with transformations
# in /storage/runs/current/ds/transforms/
# It adds groupvar-level means restricted
# to the 4 time periods eval/fcast*test/calib where the means are computed
# on all data up to train_end of that period
# for the 4 outcomes sb/ns/os/pr
# prefix mean_ is added to cols and the time period as a suffix
# so cols like mean_acled_dummy_pr_fcast_test are added
#
# Why? Because OSA reads the transformations computed by a DS run
# That DS run has always been a fcast_test run
# So OSA runs like eval_calib, read those transforms that contained, for them,
# future values of the outcomes through the groupvar-level means.
# This script creates time-limited computed groupvar level means instead for
# OSA to use. Hacky and ugly and I feel bad.


import sys
import pandas as pd

sys.path.insert(0, "..")
from views_utils.dbutils import make_connectstring, df_to_db
import models.times as t

prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = make_connectstring(prefix, db, uname, hostname, port)

basedir = "/storage/runs/current/ds/transforms/"
path_template = "{basedir}{loa}_transforms/data/{loa}_imp_{imp}.hdf5"

loas = ["pgm", "cm"]
runtypes = ["eval", "fcast"]
periods = ["calib", "test"]
cols = [
    "ged_dummy_sb",
    "ged_dummy_ns",
    "ged_dummy_os",
    "acled_dummy_pr",]

print("Starting computation of time-limited groupvar-level means")

for loa in loas:
    for imp in range(1, 6):
        path = path_template.format(basedir=basedir, loa=loa, imp=imp)
        df = pd.read_hdf(path)
        print(f"read {path}")
        df.sort_index(inplace=True)
        for rt in runtypes:
            for p in periods:
                train_end = t.times_nested[rt][p]['train_end']
                print(f"computing mean until {train_end} for {rt}_{p}")
                df_means = df.loc[:train_end][cols]
                df_means = df_means.groupby(level=1).mean()
                prefix = "mean_"
                suffix = f"_{rt}_{p}"
                df_means = df_means.add_prefix(prefix=prefix)
                df_means = df_means.add_suffix(suffix=suffix)
                df = df.merge(df_means, left_index=True, right_index=True)

        df.to_hdf(path, key='data')
        print(f"wrote {path}")