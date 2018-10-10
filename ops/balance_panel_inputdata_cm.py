import sys
import pandas as pd
import itertools

sys.path.append("..")
import views_utils.dbutils as dbutils

prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)



paths_data = []
path_base = "/storage/runs/current/ds/input/cm/data/cm_imp_N.hdf5"
for i in range(1,6):
    paths_data.append(path_base.replace("N", str(i)))

def balance_df_panel_index(df, timevar, groupvar, t_start=None, t_end=None, groupvars=None):
    """ balances the index of a dataframe between t_end and t_start to contain
    the groups present at t_end, and only those. 

    If a group appears between t_start and t_end it is "filled back" to t_start
    If a group dissappears between t_start and t_end it is removed. 

    Args:
        df: The dataframe to expand the index of
        timevar: column in dataframe to use as timevar
        groupvar: column in dataframe to use as groupvar
        t_start: first t of period to balance, defaults to first t in df
        t_end: last t of period to balance, defaults to last t in df
    Returns:
        df_balanced: a df with altered index columns
         """


    # Check if df has a multiindex already
    if isinstance(df.index, pd.MultiIndex):
        df_has_multiindex = True
    else:
        df_has_multiindex = False

    # Set it if we don't have it
    if not df_has_multiindex:
        df.set_index([timevar, groupvar], inplace=True)
    
    df.sort_index(inplace=True)

    # If no time limits are supplied use the min and max in the data
    if not t_start:
        t_start = int(df.index.get_level_values(timevar).min())
    if not t_end:
        t_end = int(df.index.get_level_values(timevar).max())
    
    # If not supplied, use the groupvars present at last t in data
    if not groupvars:
        groupvars = df.loc[t_end].index.get_level_values(groupvar)
        groupvars = sorted(list(groupvars))

    # Get list of times for the balanced period
    times_balanced = df.loc[t_start:t_end].index.get_level_values(timevar)
    times_balanced = list(set(times_balanced))
    # new index of the balanced period
    idx_balanced = list(itertools.product(times_balanced, groupvars))
    
    t_start_prebalance = int(df.index.get_level_values(timevar).min())
    t_end_prebalance = t_start - 1

    # keep old index for pre-balance period
    idx_unbalanced = list(df.loc[t_start_prebalance:t_end_prebalance].index.values)

    idx_old = list(df.index)
    idx_new = sorted(list(idx_balanced+idx_unbalanced))

    idx_old_not_in_new = sorted(list(set(idx_old) - set(idx_new)))
    idx_new_not_in_old = sorted(list(set(idx_new) - set(idx_old)))


    # Select the rows by this new index to a new df
    df_balanced = df.loc[idx_new]

    # Another sort for good measure
    df_balanced.sort_index(inplace=True)

    # Respect that df had no multiindex set when we got it
    if not df_has_multiindex:
        df_balanced.reset_index(inplace=True)

    print("len df", len(df))
    print("len df_balanced", len(df_balanced))
    delta_rows = len(df_balanced) - len(df)
    print("delta_rows: ", delta_rows)
    print("Index idx_old_not_in_new:", idx_old_not_in_new)
    print("Index idx_new_not_in_old:", idx_new_not_in_old)

    return df_balanced

for path_data in paths_data:
    df = pd.read_hdf(path_data)
    print("read", path_data)
    df = balance_df_panel_index(df, "month_id", "country_id",
        t_start = 360)
    path_output = path_data
    df.to_hdf(path_output, key='data')
    print("wrote", path_output)
