import os
import sys
import argparse

import pandas as pd

sys.path.insert(0, "..")
from views_utils.dbutils import make_connectstring, df_to_db

def get_paths_from_dir(dir, extension=None):
    paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root,file)
            paths.append(path)
    if extension:
        print("Selecting paths containing", extension, "from", dir)
        paths = [path for path in paths if extension in path.split("/")[-1]]
    return paths

parser = argparse.ArgumentParser()
parser.add_argument("--dir_data", type=str,
    help="dir_data")
parser.add_argument("--table_prefix", type=str,
    help="table_prefix to add to table name")
args_main = parser.parse_args()

dir_data = args_main.dir_data
table_prefix = args_main.table_prefix

prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = make_connectstring(prefix, db, uname, hostname, port)

schema = "launched"
paths_data = get_paths_from_dir(dir_data)
for path in sorted(paths_data):
    fname = os.path.basename(path)
    fname = fname.split(".")[0]
    df = pd.read_hdf(path)
    print("Read", fname)
    print("From", path)
    table = "_".join([table_prefix, fname])
    print("tablename", table)
    df_to_db(connectstring, df, schema, table, if_exists="replace", write_index=True)
