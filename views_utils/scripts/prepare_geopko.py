'''Script to fetch and merge to create ViEWS-GeoPKO dataset'''

import sys
import pandas as pd
import numpy as np
import datetime
import math

sys.path.append("..")
import dbutils

# set up connectstring
uname = "VIEWSADMIN"
connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
    port="5432", prefix="postgres",uname=uname)

# -- prepare pgm data --
# get pgm and subset to 1994-2014
columns = ['month_id', 'pg_id', 'ged_dummy_sb', 'ged_dummy_ns', 'ged_dummy_os',
           'l12_ged_dummy_sb', 'l12_ged_dummy_ns', 'l12_ged_dummy_os',
           'ln_bdist3', 'ln_ttime', 'ln_capdist', 'ln_pop', 'gcp_li_mer', 
           'imr_mean', 'mountains_mean', 'urban_ih_li', 'excluded_dummy_li', 
           'decay_12_cw_ged_dummy_sb_0', 'decay_12_cw_ged_dummy_ns_0',
           'decay_12_cw_ged_dummy_os_0', 'q_1_1_l1_ged_dummy_sb',
           'q_1_1_l1_ged_dummy_ns', 'q_1_1_l1_ged_dummy_os']

df = dbutils.db_to_df(connectstring, schema="launched",
                       table="transforms_pgm_imp_1",
                       columns=columns)

limit = (df['month_id']>=169) & (df['month_id']<=420)
df = df[limit]

# add log imr
df['ln_imr_mean'] = np.log1p(df['imr_mean'])

# add dummy variables for border areas (+2 here due to small ds error)
df['border'] = np.where(df['ln_bdist3'] < np.log(25 + 2), 1, 0)

# set index
df.set_index(['pg_id', 'month_id'], inplace=True)

# print finish
print(df.head())
print(len(df))
print("Finished preparing PGM data.")


# -- prepare geopko data --
# get geopko data
pk_df = dbutils.db_to_df(connectstring, schema="dataprep", table="geo_pko")

# subset this on relevant columns
columns = ['source', 'mission', 'year', 'month', 'latitude', 'longitude',
           'no_troops', 'hesup', 'avia', 'hq']
pk_df = pk_df[columns]

# shift split Ivory Coast month 
pk_df.loc[pk_df['month'] == "March (late)", 'month'] = "April"
pk_df.loc[pk_df['month'] == "March (early)", 'month'] = "March"

# replace month column with regular month counter via datetime conversion
pk_df['month'] = pd.to_datetime(pk_df['month'], format='%B')
pk_df['month'] = pd.DatetimeIndex(pk_df['month']).month
#pk_df['yearmonth'] = pk_df['year'] + '-' + pk_df['month']

# function to get monthid
def fetch_df_months(connectstring):
  q_months = """
  SELECT id, month, year_id
  FROM staging.month;
  """
  df_months = dbutils.query_to_df(connectstring, q_months)
  df_months.rename(columns={'id': 'month_id'}, inplace=True)
  df_months.rename(columns={'year_id': 'year'}, inplace=True)
  df_months.set_index(['year', 'month'], inplace=True)
  return df_months

# get monthid and merge into pk_df
df_months = fetch_df_months(connectstring)
pk_df.set_index(['year', 'month'], inplace=True)
pk_df = pk_df.merge(df_months, left_index=True, right_index=True)

# function to get gridcells associated with long lat
def get_priogrid(lat, lon):
  lat_component = ((((90 + (math.floor(lat*2)/2))*2)+1)-1)*720 
  lon_component = ((180+(math.floor(lon*2)/2))*2)
  gid = lat_component + lon_component + 1
  return int(gid)

# apply function on non-NULL (this excludes one case in Cote D'Ivoire 2008),
# creating pg_id column
pk_df.reset_index(inplace=True)
pk_df['pg_id'] = pk_df[pk_df.latitude.notnull()].apply(lambda row: get_priogrid(row['latitude'], 
                                                                row['longitude']), axis=1)

pk_df.set_index(["pg_id", "month_id"], inplace=True)

# print finish
print(pk_df.head())
print("Finished preparing GeoPKO data. Merging now...")


# -- left merge pko data into pgm and clean up --
df = pd.merge(df, pk_df, how='left', left_index=True, right_index=True)
print("after main merge:", len(df))

# drop year, month columns from pk data
df.drop(columns=['year', 'month'], inplace=True)

# fetch country_ids per pg_id and month_id, via reset index
df.reset_index(inplace=True)
df_cpgm = dbutils.db_to_df(connectstring, schema="staging_test",
                           table="cpgm", ids=['pg_id', 'month_id'])
df.set_index(["pg_id", "month_id"], inplace=True)
df = df.merge(df_cpgm, left_index=True, right_index=True)

# get ViEWS countrynames for good measure, via reset index
df.reset_index(inplace=True)
df_c = dbutils.db_to_df(connectstring, schema="staging",
                        table="country", columns=["id", "name"])
df_c.rename(columns={'id': 'country_id'}, inplace=True)
df = df.merge(df_c, on=["country_id"])

# drop obsolete latitude and longitude columns
df.drop(columns=['longitude', 'latitude'], inplace=True)

# print finish
print(df.head())
print("after other merges:", len(df))
print("Finished merge. Aggregating pg_id-month_id duplicates...")


# -- aggregating duplicates --
# function (selecting latitude based on biggest base)
def merge_duplicate_rows(df):
  # get indices of duplicates
  duplicates = df.duplicated(subset=['month_id', 'pg_id'])
  duplicates_keep = df.duplicated(subset=['month_id', 'pg_id'], keep=False)
  # set up empty dummy column and add one for indices of the duplicates
  df['shared'] = 0
  df['shared'].loc[duplicates_keep] = 1
  # print statement
  print("Due to multiple maps there are", len(df.loc[duplicates]), 
        "duplicated pgms. Aggregating them now...")
  # set up rules to aggregate on (change source and mission rule)
  rules = {'source': 'first',
           'mission': 'first', 
           'no_troops': 'sum', 
           'hesup': 'max',
           'avia': 'max', 
           'hq': 'max'} 
  # hacky fix of '?' and None in hq variable causing error
  df.loc[df.hq == '?', 'hq'] = -1
  df.hq.fillna(-1, inplace=True)
  df.hq = df.hq.astype('int')
  # get columns to group on
  id_cols = [i for i in list(df.columns) if i not in list(rules.keys())]
  print(id_cols)
  print("Duplicates based on groupby on these cols:", len(df.loc[df.duplicated(subset=id_cols)]))
  # aggregate while using a hacky placeholder for the groupby by NA, replaced
  df = df.fillna(-1).groupby(id_cols, as_index=False).agg(rules)
  df = df.replace(-1, np.nan)
  return df

df = merge_duplicate_rows(df)
print("after aggregation:", len(df))

# print finish
print("Done aggregating. Filling missing values and extrapolating...")


# -- fillna and dummy --
# fill function that pads in-between and extends by specified limit
def fillna_extend(df, var_to_follow, var_to_fill, limit):
  try:
    non_nans = df[df[var_to_follow].notnull()]
    start, end = non_nans.index[0], non_nans.index[-1]
    # get last index per group of variable(s) to fill
    realend = df[var_to_fill].index[-1]
    # fill in between first and last group observation
    df.loc[start:end, var_to_fill] = df.loc[start:end, var_to_fill].fillna(method='ffill')
    # fill forward from last known observation by specified limit
    df.loc[end:realend, var_to_fill] = df.loc[end:realend, var_to_fill].fillna(method="ffill", limit=limit)
    # exception for those grid cells with only NA
  except:
    pass
  return df

# select columns to fill, and apply above function after sort
cols = ['source', 'mission', 'latitude', 'longitude',
        'no_troops', 'hesup', 'avia', 'hq']
df.sort_values('month_id', inplace=True)
df = df.groupby('pg_id').apply(lambda group: fillna_extend(group, 'source', 
                                                           cols, 3))

# assign dummy for gridcells in country-months with active PKO
print("after filling and extrapolation:", len(df))
print("Assigning PKO dummy by country-month...")
# function
def get_pkodummy(df, var_to_follow):
  df['pko_dummy'] = 1 if df[var_to_follow].notnull().any() else 0
  return df
# apply through groupby on country_id
df = df.groupby(['country_id', 'month_id']).apply(lambda group: get_pkodummy(group, 'mission'))

# write final product to .csv
df.to_csv("geopko.csv")
print(df.columns.values)
print("Wrote to file 'geopko.csv'")

