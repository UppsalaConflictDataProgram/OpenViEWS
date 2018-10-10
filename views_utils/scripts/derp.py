'''Script to fetch and merge to create ViEWS-GeoPKO dataset'''

import sys
import pandas as pd
import numpy as np
import datetime
import math

sys.path.append("..")
import dbutils

# function to get gridcells associated with long lat


def get_priogrid(lat, lon):
    lat_component = ((((90 + (math.floor(lat*2)/2))*2)+1)-1)*720
    lon_component = ((180+(math.floor(lon*2)/2))*2)
    gid = lat_component + lon_component + 1
    return int(gid)


# set up connectstring
uname = "VIEWSADMIN"
connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST",
                                           port="5432", prefix="postgres", uname=uname)

try:
    df = pd.read_hdf("geopko_cached.hdf5")
except:
    df = dbutils.db_to_df(connectstring, schema="dataprep", table="geo_pko")

df = df.drop(columns=["index", "month", "year"])

groupvar = "mission_location"
timevar = "month_id"
# Mission location is the groupvar to use as ID
df[groupvar] = df['mission'] + "__" + df['location']
df.set_index([timevar, groupvar], inplace=True)
df.sort_index(inplace=True)

# To keep our extended group dfs in
dfs = []
# level=1 is mission_location
for key, group in df.groupby(groupvar):

    # I don't really get what a groupby-group is so make sure it's a regular
    # dataframe with no funny business and just month_id as index.
    # dfg stands for df-group
    dfg = pd.DataFrame(group)
    dfg.reset_index(inplace=True)
    dfg.set_index(['month_id'], inplace=True)
    dfg.sort_index(inplace=True)

    # create list of month_ids to serve as our index
    # the list is all months between
    # the first month_id in the current index to the last month_id + 3
    month_id_start = min(dfg.index)
    month_id_end = max(dfg.index) + 3
    # +1 for range inclusiveness
    idx = list(range(month_id_start, month_id_end+1))

    # Call reindex on the group to get all the observations in between
    # This creates a lot of missing values
    print("#"*80)
    print("#"*80)
    print("PRE REINDEX")
    print(dfg)
    print("*"*80)
    dfg = dfg.reindex(idx, method='ffill')
    print("POST REINDEX")
    print(dfg)
    print("#"*80)
    print("#"*80)
    # Remove our month_id index so it's just a default-indexed df for concating
    dfg.reset_index(inplace=True)
    dfs.append(dfg)

# Concat together our list of mission_location dfs
df = pd.concat(dfs)
df.set_index([timevar, groupvar], inplace=True)
print(df.head(50))


