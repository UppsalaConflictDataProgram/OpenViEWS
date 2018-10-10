import os
import sys

sys.path.append("..")

import views_utils.dbutils as dbutils

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
                                           port="5432", prefix="postgres",
                                           uname="VIEWSADMIN")


times_tables = {
    "fcast_test": [
        "ds_pgm_fcast_test",
        "osa_pgm_fcast_test",
        "ensemble_pgm_fcast_test"
    ],
    "fcast_calib": [
        "ds_pgm_fcast_calib",
        "osa_pgm_fcast_calib"
    ],
    "eval_test": [
        "ds_pgm_eval_test",
        "osa_pgm_eval_test",
        "ensemble_pgm_eval_test"
    ],
    "eval_calib": [
        "ds_pgm_eval_calib",
        "osa_pgm_eval_calib"
    ]
}

# Get the country_id for each pgm
df_country_keys = dbutils.db_to_df(connectstring, "staging_test", "cpgm")
df_country_keys.set_index(["month_id", "pg_id"], inplace=True)

for time in times_tables:
    df = df_country_keys.copy()
    for table in times_tables[time]:
        print("Fetching {}".format(table))
        df_scratch = dbutils.db_to_df(connectstring, "landed", table, 
                          ids = ["month_id", "pg_id"])
        print("Merging {}".format(table))
        df = df.merge(df_scratch, left_index=True, right_index=True)
    print("Computing mean {}".format(time))
    df.reset_index(inplace=True)
    df = df.drop(columns=['pg_id'])
    df_mean = df.groupby(["month_id", "country_id"]).mean()

    table_out = "agg_cm_" + time
    print("table_out: {}".format(table_out))

    dbutils.df_to_db(connectstring, df_mean, "landed", table_out, 
                     if_exists="replace", write_index=True)
    
