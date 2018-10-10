import os
import sys
import argparse

import pandas as pd

sys.path.append("..")
from views_utils import dbutils


parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str,
    help="dir_data")
parser.add_argument("--schema", type=str,
    help="schema")
parser.add_argument("--table", type=str,
    help="table")
args_main = parser.parse_args()

path = args_main.path
table = args_main.table
schema = args_main.schema

prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

df = pd.read_hdf(path)
print(f"read {path}")
dbutils.df_to_db(connectstring=connectstring,
                 df=df,
                 schema=schema,
                 table=table,
                 if_exists="replace",
                 write_index=True)
