"""Database import script for ViEWS of the Future of Violent Politics Masterdata

The script loads any .csv file, subsets it by a list of variables and pushes it to the data.

Example:
    python GetFromFile.py \
        --uname VIEWSADMIN \
        --path_input /Users/VIEWSADMIN/Dropbox/CntData/Masterdata/MasterData.csv
        --path_varlist varlist_fovp.txt
"""


from __future__ import print_function
from __future__ import division

import pandas as pd 
import sys
import argparse


sys.path.insert(0, "..")
import views_utils.dbutils as dbutils

def read_varlist(path_varlist):
    with open(path_varlist, 'r') as f:
        varlist = f.readlines()

    # Lowercase and strip whitespace
    varlist = [line.lower().strip() for line in varlist]

    # Drop comment lines
    varlist = [line for line in varlist if not line[0]=="#"]

    # Get only what comes before "," on each line
    # Varlist is formatted like so: name_in_source, name_in_db
    varlist = [line.split(",")[0] for line in varlist]
    print("Read varlist from containing", len(varlist), "vars from", path_varlist)

    return varlist


parser = argparse.ArgumentParser()

parser.add_argument("--uname", type=str, required=True,
    help="DB username")
parser.add_argument("--path_input", type=str, required=True,
    help="path to .csv to import")
parser.add_argument("--path_varlist", type=str, required=True,
    help="path to one-var-per-line varlist to include")
parser.add_argument("--schema", type=str, required=True,
    help="schema to push to")
parser.add_argument("--table", type=str, required=True,
    help="table to push to")
parser.add_argument("--force", action='store_true',
    help="force pushing even if not all variables are present in input file")

args = parser.parse_args()

path_input = args.path_input
path_varlist = args.path_varlist
db_schema = args.schema
db_table = args.table
db_uname = args.uname
force = args.force

db_prefix           = "postgresql"
db_db               = "views"
db_port             = "5432"
db_hostname         = "VIEWSHOST"   #Janus
db_connectstring    = dbutils.make_connectstring(db_prefix, db_db, 
                                                 db_uname, db_hostname, db_port)

varlist = read_varlist(path_varlist)

df = dbutils.file_to_df(path_input)
df.columns = df.columns.str.lower()

available = list(df.columns)
wanted_not_in_data  = [col for col in varlist if col not in available]
wanted_in_data      = [col for col in varlist if col in available]

# Ugly logic but it works
if len(wanted_not_in_data)>0:
    print("There are vars specified in ", path_varlist, "that aren't in ", 
            path_input)
    print("Missing vars are:")
    for var in wanted_not_in_data:
        print("\t", var)

if not force:
    assert (len(wanted_not_in_data)==0) , ( 
        "Variables in ", path_varlist, " missing from ", path_input, 
        "Pass --force to continue")

if len(wanted_not_in_data)>0 and force:
    print("WARNING: There are variables in varlist but not in data.")
    print("--force is specified. Pushing anyway")

# Subset the df to only those requested and existing in the data
df = df[wanted_in_data]

dbutils.df_to_db(db_connectstring, df, db_schema, db_table, if_exists="replace")
