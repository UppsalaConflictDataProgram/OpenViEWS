# Used to fetch data for dynasim

import sys
sys.path.insert(0, "..")

from views_utils.dbutils import make_connectstring, query_to_file

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dir_data", type=str,
    help="dir_data")
parser.add_argument("--path_query", type=str,
    help="name of the query file in SQLSelects")
args_main = parser.parse_args()

dir_data = args_main.dir_data
path_query = args_main.path_query

prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = make_connectstring(prefix, db, uname, hostname, port)

print(path_query)
fformat = "hdf5"
df = query_to_file(connectstring, path_query, dir_data, 
    fformat, verbose=True)
