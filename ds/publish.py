""" Publish one or multiple dynasim runs to database table

The purpose of this script is to keep results from dynasim neat and tidy in
the database. Outputs from multiple runs are collected into a single table,
renamed, and pushed to the database. 

It reads the main output file, aggregated.hdf5, from dynasim runs
and pushes them to a single table in the database.
Several runs are specified by passing --run_id multiple times.

Three options are given for naming and variable selection: 
outcome, stripname and prefix.

Stripname
Stripname removes a string from each column name, if stripname ged_dummy_ is
passed then  "ged_dummy_sb" is renamed to just "sb" as ged_dummy_ is removed.
This is done for all literal matches (no regex).

Prefix
Simply adds a prefix to each column name. 

Example call:
    python publish.py \
        --uname VIEWSADMIN \
        --schema landed \
        --table ds_run1_test \
        --run_id restricted_eval_pred \
        --run_id with_acled_eval_pred \
        --run_id full_eval_pred \
        --outcome ged_dummy_sb_mean \
        --outcome ged_dummy_ns_mean \
        --outcome ged_dummy_os_mean \
        --stripname ged_dummy_ \
        --stripname _mean \
        --prefix ds_ \
        --dir_scratch /proj/snic2017-7-47/ds/runs \
        --printswitch \
        --push \

"""

import sys
import argparse
import functools

import pandas as pd

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils


parser = argparse.ArgumentParser()

parser.add_argument("--push", action='store_true',
    help="Push merged results to db")
parser.add_argument("--printswitch", action='store_true',
    help="Print merged results")

parser.add_argument("--uname", type=str, required=True,
    help="DB username")
parser.add_argument("--schema", type=str, required=True,
    help="DB schema")
parser.add_argument("--table", type=str, required=True,
    help="DB table")


parser.add_argument("--dir_scratch", type=str, required=True,
    help="Where to find the dynasim runs")

parser.add_argument("--run_id", type=str, action='append', required=True,
    help="Which run_id's to publish, pass once for each")

parser.add_argument("--outcome", type=str, action='append', required=True,
    help="Variable names of outcomes to include. pass once for each")
parser.add_argument("--stripname", type=str, action='append', 
    help="Substring to strip from column names,  pass once for each")

parser.add_argument("--prefix", type=str, 
    help="Prefix to add to column names")


args = parser.parse_args()

dir_scratch = args.dir_scratch
run_ids = args.run_id

args_outcomes = args.outcome
stripnames = args.stripname

push = args.push
printswitch = args.printswitch

uname = args.uname
schema = args.schema
table = args.table


# db parameters
prefix   = "postgresql"
db       = "views"
port     = "5432"
hostname = "VIEWSHOST"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

dfs = []
for run_id in run_ids:
    dir_run = dir_scratch + "/" + run_id
    path = dir_run + "/aggregate/aggregated.hdf5"
    df = pd.read_hdf(path)
    print("read", path)

    outcomes = [outcome for outcome in args_outcomes if outcome in df.columns]
    df = df[outcomes]
    
    for stripname in stripnames:
        df = df.rename(columns=lambda name: name.replace(stripname, ''))


    prefix = "ds_" + run_id + "_"
    df = df.add_prefix(prefix)
    # subset to include only outcomes
    dfs.append(df)

# Merge the runs into one
df = functools.reduce(lambda df1, df2: df1.merge(df2, left_index=True, 
    right_index=True, how='outer'), dfs)

if printswitch:
    print(df.head())

if push:
    dbutils.df_to_db(connectstring, df, schema, table, 
        if_exists="replace", write_index=True)

