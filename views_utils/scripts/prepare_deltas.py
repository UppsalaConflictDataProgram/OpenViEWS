import os
import sys
import pandas as pd

sys.path.append("..")

import dbutils

## to do:
# add other deltas
# add delta between vtypes
# change in log odds might be interesting too 

# connectstring
connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST",
                                           port="5432", prefix="postgres",
                                           uname="VIEWSADMIN")

schema = "landed"
if_exists = "replace"

# set index on
id_dict = {"cm": ["month_id", "country_id"],
           "pgm": ["month_id", "pg_id"]}

# inserts
tables = ["ensemble_cm_fcast_test", "ensemble_cm_eval_test",
          "ensemble_pgm_fcast_test", "ensemble_pgm_eval_test"]

# get startmonth
table = tables[1]
df_current = dbutils.db_to_df(connectstring, "landed", table)
df_current.set_index(id_dict["cm"], inplace=True)
startmonth = int(df_current.index.get_level_values('month_id').min())
# get endmonth
table = tables[0]
df_current = dbutils.db_to_df(connectstring, "landed", table)
df_current.set_index(id_dict["cm"], inplace=True)
endmonth = int(df_current.index.get_level_values('month_id').min())

print(f"Getting deltas for decay between {startmonth} and {endmonth}.")

# loop over ensemble tables
for table in tables:
    # set table name for the deltas
    tablename = f"deltapred_{table}"
    # get data from previous and landed
    df_prev = dbutils.db_to_df(connectstring, "previous", table)
    df_current = dbutils.db_to_df(connectstring, "landed", table)
    # get ids and set index
    if "cm" in table:
        df_prev.set_index(id_dict["cm"], inplace=True)
        df_current.set_index(id_dict["cm"], inplace=True)
    if "pgm" in table:
        df_prev.set_index(id_dict["pgm"], inplace=True)
        df_current.set_index(id_dict["pgm"], inplace=True)
    # add prefix and merge
    df_prev = df_prev.add_prefix("prev_")
    df = df_current.merge(df_prev, left_index=True, right_index=True)
    # generate the deltas and drop other columns
    for col in df_current:
        name_prev = "prev_" + col
        name_delta = "delta_" + col
        df[name_delta] = df[col] - df[name_prev]
        df = df.drop(columns=[col, name_prev])
    # check
    print(f"writing {table}")
    print(df.head(20))
    # push to db
    dbutils.df_to_db(connectstring, df, schema, tablename, if_exists, 
                     write_index=True)

# decay tables
for level in ["cm", "pgm"]:
    # set table name used in db
    table = f"transforms_{level}_imp_1"
    # set name to give to new table
    tablename = f"deltafeat_{level}"
    # get column names
    colnames = dbutils.get_colnames_table(connectstring, "launched", table)
    cols = [col for col in colnames if "decay" in col]
    # get ids
    ids = id_dict[level]
    # get data from previous and launched
    df_prev = dbutils.db_to_df(connectstring, "previous", table, ids=ids)
    df_current = dbutils.db_to_df(connectstring, "launched", table, columns=cols, ids=ids)
    # set indices
    df_current.sort_index(inplace=True)
    # limit to relevant monthids
    df_prev = df_prev.loc[startmonth:endmonth]
    df_current = df_current.loc[startmonth:endmonth]
    # add prefix and merge
    df_prev = df_prev.add_prefix("prev_")
    df = df_current.merge(df_prev, left_index=True, right_index=True)
    # generate the deltas and drop other columns
    for col in df_current:
        name_prev = "prev_" + col
        name_delta = "delta_" + col
        df[name_delta] = df[col] - df[name_prev]
        df = df.drop(columns=[col, name_prev])
    # check
    print(f"writing {tablename}")
    print(df.head(20))
    # push table
    dbutils.df_to_db(connectstring, df, schema, tablename, if_exists, 
                     write_index=True)
    