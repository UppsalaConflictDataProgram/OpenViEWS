"""Database import script for ViEWS of the Future of Violent Politics Masterdata

Example:
    python GetFVP.py \
        --uname VIEWSADMIN \
        --path_input /Users/VIEWSADMIN/Dropbox/CntData/Masterdata/MasterData.csv
"""

import sys
import os
import argparse

import pandas as pd 

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils
import views_utils.datautils as datautils

parser = argparse.ArgumentParser()

parser.add_argument("--uname", type=str, required=True,
    help="DB username")
parser.add_argument("--path_input", type=str, required=True,
    help="path to .csv to import")

args = parser.parse_args()

path_input = args.path_input
db_uname = args.uname

db_prefix           = "postgresql"
db_db               = "views"
db_port             = "5432"
db_hostname         = "VIEWSHOST"   #Janus
db_connectstring    = dbutils.make_connectstring(db_prefix, db_db, 
                                                 db_uname, db_hostname, db_port)

db_schema = "dataprep_test"
db_table = "fvp"

path_varlist = "../varlists/fvp/rawnames.txt"
path_renames = "../varlists/fvp/renames.txt"
varlist = datautils.read_varlist(path_varlist)
renames = datautils.read_renames(path_renames)

df = dbutils.file_to_df(path_input)
df.columns = df.columns.str.lower()

available = list(df.columns)
wanted_not_in_data  = [col for col in varlist if col not in available]
wanted_in_data      = [col for col in varlist if col in available]

if len(wanted_not_in_data)>0:
    message = "There are variables in " + path_varlist + " that aren't in" + path_input
    for v in wanted_not_in_data:
        print("\t", v)
    raise ValueError(message)

# Subset the df to only those requested and existing in the data
df = df[wanted_in_data]

df = datautils.apply_renames(df, renames)


dbutils.df_to_db(db_connectstring, df, db_schema, db_table, if_exists="replace")
