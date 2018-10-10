'''Script that produces a lineplot of predicted proportions
of gid-cells for each outcome variable'''

# instructions:
# set username, runid, and select countries before running.

# RBJ 12-07-2018

import sys
import os

import pandas as pd
import matplotlib.pyplot as plt

sys.path.append("..")
import views_utils.dbutils as dbutils

# set username
uname = "VIEWSADMIN"

# set runid
runid = "r.2018.08.01"

# select countries to include in lineplot
countries = ["Nigeria", "Sudan", "Rwanda", "Kenya"]


###
def fetch_df_months(connectstring):
    q_months = """
    SELECT id, month, year_id
    FROM staging.month;
    """
    df_months = dbutils.query_to_df(connectstring, q_months)
    df_months['month_id'] = df_months['id']
    df_months.set_index(['month_id'], inplace=True)
    return df_months

def month_id_to_datestr(df_months, month_id):
    datestr = str(df_months.loc[month_id]['year_id']) + "-" + str(df_months.loc[month_id]['month'])
    return datestr

timevar = "month_id"
groupvar = "pg_id"
outcomes = ["sb", "ns", "os"]
outcomes = ["ged_dummy_" + outcome for outcome in outcomes]
print("outcomes:", outcomes)

connectstring = dbutils.make_connectstring(prefix="postgresql", db="views",
                                           uname=uname, hostname="VIEWSHOST",
                                           port="5432")

df_pgm = dbutils.db_to_df(connectstring, schema="landed",
                          table="ensemble_pgm_fcast_test",
                          ids=[timevar, groupvar])
df_c = dbutils.db_to_df(connectstring, schema="staging",
                        table="country", columns=["id", "name"])
df_c.rename(columns={'id': 'country_id'}, inplace=True)

df_cpgm = dbutils.db_to_df(connectstring, schema="staging_test",
                           table="cpgm", ids=[timevar, groupvar])


df = df_pgm.merge(df_cpgm, left_index=True, right_index=True)
df.reset_index(inplace=True)
df = df.merge(df_c, on=["country_id"])
df.set_index([timevar, groupvar], inplace=True)

tmin = df.index.get_level_values(timevar).min()
tmax = df.index.get_level_values(timevar).max()
df_actuals = dbutils.db_to_df_limited(connectstring, schema="preflight",
                                      table="flight_pgm",
                                      timevar="month_id",
                                      groupvar=groupvar,
                                      tmin=tmin, tmax=tmax,
                                      columns=outcomes.copy()
                                      )

df_actuals.fillna(0, inplace=True)
print(outcomes)
df = df.merge(df_actuals, left_index=True, right_index=True)
df.reset_index(inplace=True)

df_months = fetch_df_months(connectstring)

df.set_index(['month_id'], inplace=True)
df = df.merge(df_months, left_index=True, right_index=True)
df.sort_index(inplace=True)
df['month'] = df['month'].astype(str)
df['month'] = df['month'].str.zfill(2)
df['year_id'] = df['year_id'].astype(str)
df['month_str'] = df['year_id'] + "-" + df['month']

# select outcome variable to plot
predictions = ["average_calib_select_sb",
               "average_calib_select_ns",
               "average_calib_select_os"]
# functions:
def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)

def compute_proportions(df, var):
    '''computes predicted proportion of gid cells with outcome variable.'''
    print("var:", var)
    df_grouped = df.groupby(['name', 'month_str'])[[var]].mean()
    df_grouped.reset_index(inplace=True)
    df_grouped['prop'] = df_grouped[var]
    df_grouped.drop(columns=[var], inplace=True)

    return df_grouped

def plot_proplines(df, out, countrylist, output):
    '''subsets data and plots proportion lines for selected countries.'''
    df_merge = compute_proportions(df, out)
    # subset and initiate plot
    df_line = df_merge[df_merge.name.isin(countrylist)]
    fig, ax = plt.subplots(figsize=(10, 6))
    # plot country lines
    for k, g in df_line.groupby('name'):
        plt.plot(g['month_str'], g['prop'], label=k)
    # fix x axis and title padding
    for item in ax.get_xticklabels():
        item.set_rotation(90)
    plt.tight_layout()
    plt.subplots_adjust(top=.90)
    # finish and save figure
    plt.legend()
    plt.title('Proportion trends for {} \nEnsemble run: {}'.format(out, runid), 
              loc='left')
    plt.savefig("{}lineplot_{}.pdf".format(output, out))
    print("Wrote ", output)

# set up output path
dir_output = "/storage/runs/current/plot/lineplots/"
create_dirs([dir_output])

# run:
for prediction in predictions:
    plot_proplines(df, prediction, countries, dir_output)
