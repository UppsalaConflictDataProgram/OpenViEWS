'''Returns a .csv containing the actuals and ensemble preds with iso-datestrings. 
pgm return is massive making to_csv suffer - needs subsetting'''

import sys
import pandas as pd

sys.path.append("..")
import dbutils

# set up connectstring
uname = "VIEWSADMIN"
connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
    port="5432", prefix="postgres",uname=uname)

## preparation of cm_actuals_preds
# indexes for cm_evalpreds
timevar = "month_id"
groupvar = "country_id"

# get cm evalpreds from db (change to SQL query)
cm_preds = dbutils.db_to_df(connectstring, schema="landed",
                          table="calibrated_cm_eval_test",
                          ids=[timevar, groupvar])
cm_ensemble = dbutils.db_to_df(connectstring, schema="landed",
                          table="ensemble_cm_eval_test",
                          ids=[timevar, groupvar])
cm_actuals = dbutils.db_to_df(connectstring, schema="launched",
                          table="transforms_cm_imp_1",
                          ids=[timevar, groupvar], 
                          columns=["ged_dummy_sb", "ged_dummy_ns", "ged_dummy_os"])
df_cm_actualspreds = cm_actuals.merge(cm_preds, left_index=True, right_index=True)
df_cm_actualspreds = df_cm_actualspreds.merge(cm_ensemble, left_index=True, right_index=True) 

# get country information
df_c = dbutils.db_to_df(connectstring, schema="staging",
                        table="country", columns=["id", "name"])

# set schema/table/columns of interest
schema = "staging"
table = "country"
columns = ["id", "name", "isoab"]

# get df containing names and iso
df_names = dbutils.db_to_df(connectstring, schema, table, columns)
df_names.rename(columns={'id': 'country_id'}, inplace=True)
df_names.set_index(["country_id"], inplace=True)

# merge these two
df = df_cm_actualspreds.merge(df_names, left_index=True, right_index=True)
df.reset_index(inplace=True)

# get datestring functions
def fetch_df_months(connectstring):
    q_months = """
    SELECT id, month, year_id
    FROM staging.month;
    """
    df_months = dbutils.query_to_df(connectstring, q_months)
    df_months.rename(columns={'id': 'month_id'}, inplace=True)
    #df_months['month_id'] = df_months['id']
    df_months.set_index(['month_id'], inplace=True)
    return df_months

def month_id_to_datestr(df_months, month_id):
    datestr = str(df_months.loc[month_id]['year_id']) + "-" + str(df_months.loc[month_id]['month'])
    return datestr

# get datestring via merge
df_months = fetch_df_months(connectstring)
df.set_index(['month_id'], inplace=True)
df = df.merge(df_months, left_index=True, right_index=True)
df.sort_index(inplace=True)

# adjust types, create monthstring and iso-date
df['month'] = df['month'].astype(str)
df['month'] = df['month'].str.zfill(2)
df['year_id'] = df['year_id'].astype(str)
df['month_str'] = df['year_id'] + "-" + df['month']
df['iso_date'] = df['isoab'] + " " + df['month_str']
df.reset_index(inplace=True)

# reindex again
df.set_index(['country_id', 'month_id'], inplace=True)

# drop and then write to csv
df.drop(columns=['month', 'year_id'], inplace=True)
print(df.head(20))
df.to_csv("cm_actuals_preds_08.csv")
print("Wrote cm_actuals_preds to file.")

## preparation of pgm_actuals_preds
# indexes for pgm_evalpreds
timevar = "month_id"
groupvar = "pg_id"

# get pgm evalpreds from db
pgm_preds = dbutils.db_to_df(connectstring, schema="landed",
                          table="calibrated_pgm_eval_test",
                          ids=[timevar, groupvar])
pgm_ensemble = dbutils.db_to_df(connectstring, schema="landed",
                          table="ensemble_pgm_eval_test",
                          ids=[timevar, groupvar])
pgm_actuals = dbutils.db_to_df(connectstring, schema="launched",
                          table="transforms_pgm_imp_1",
                          ids=[timevar, groupvar], 
                          columns=["ged_dummy_sb", "ged_dummy_ns", "ged_dummy_os"])
df_pgm_actualspreds = pgm_actuals.merge(pgm_preds, left_index=True, right_index=True)
df_pgm_actualspreds = df_pgm_actualspreds.merge(pgm_ensemble, left_index=True, right_index=True) 
df_pgm_actualspreds.reset_index(inplace=True)

# get cols and rows and merge into df
df_colrow = dbutils.db_to_df(connectstring, schema="staging",
                        table="priogrid", columns=["gid", "col", "row"])
df_colrow.rename(columns={'gid': 'pg_id'}, inplace=True)
df = df_pgm_actualspreds.merge(df_colrow, on="pg_id")

# add row-col column
df['row'] = df['row'].astype(str)
df['col'] = df['col'].astype(str)
df['row_col'] = df['row'] + "-" + df['col']

# set index on final df
df.set_index([groupvar, timevar], inplace=True)

# add country_id
df_cpgm = dbutils.db_to_df(connectstring, schema="staging_test",
                           table="cpgm", ids=[groupvar, timevar])
df = df.merge(df_cpgm, left_index=True, right_index=True)

# add country name
df_c = dbutils.db_to_df(connectstring, schema="staging",
                        table="country", columns=["id", "name"])
df_c.rename(columns={'id': 'country_id'}, inplace=True)
df.reset_index(inplace=True)
df = df.merge(df_c, on=["country_id"])
df.set_index([groupvar, timevar], inplace=True)

# inspect/write to csv
print(df.head(20))
df.to_csv("pgm_actuals_preds_08.csv")
print("Wrote pgm_actuals_preds to file.")
