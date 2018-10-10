import os
import sys

sys.path.append("..")

import views_utils.dbutils as dbutils

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
                                           port="5432", prefix="postgres",
                                           uname="VIEWSADMIN")

cols_actual = [
    "ged_dummy_sb",
    "ged_dummy_ns",
    "ged_dummy_os",
    "acled_dummy_pr"
    ]

# Get the country_id for each pgm
df_country_keys = dbutils.db_to_df(connectstring, "staging_test", "cpgm")
df_country_keys.set_index(["month_id", "pg_id"], inplace=True)

df = df_country_keys.copy()
df_actuals = dbutils.db_to_df(connectstring, "preflight", "flight_pgm", 
                              ids = ["month_id", "pg_id"], columns=cols_actual)
df_actuals = df_actuals.add_prefix("pgm_")


df = df.merge(df_actuals, left_index=True, right_index=True)
df_mean = df.groupby(["month_id", "country_id"]).mean()

table_out = "agg_cm_actuals"
print("table_out: {}".format(table_out))

dbutils.df_to_db(connectstring, df_mean, "landed", table_out, 
                 if_exists="replace", write_index=True)
    
