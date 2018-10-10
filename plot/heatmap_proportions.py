'''Script that produces heatmap of predicted proportions
of gid-cells for each outcome variable'''

# RBJ 12-07-2018

import os
import argparse
import sys

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

sys.path.append("..")
import views_utils.dbutils as dbutils


parser = argparse.ArgumentParser()
parser.add_argument("--run_id", type=str,
                    help="Run ID")
# parser.add_argument("--schema", type=str,
#                     help="schema")
# parser.add_argument("--table", type=str,
#                     help="table")
# parser.add_argument("--table", action="store_true",
#                     help="for actuals also")


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
    datestr = str(df_months.loc[month_id]['year_id']) + \
        "-" + str(df_months.loc[month_id]['month'])
    return datestr


args = parser.parse_args()

run_id = args.run_id

timevar = "month_id"
groupvar = "pg_id"
outcomes = ["sb", "ns", "os"]
outcomes = ["ged_dummy_" + outcome for outcome in outcomes]
print("outcomes:", outcomes)

connectstring = dbutils.make_connectstring(prefix="postgresql", db="views",
                                           uname="VIEWSADMIN", hostname="VIEWSHOST",
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


# select predicted probabilities to plot
predictions = ["average_select_sb",
               "average_select_ns",
               "average_select_os",
               "average_wcm_sb",
               "average_wcm_ns",
               "average_wcm_os",
               "average_all_sb",
               "average_all_ns",
               "average_all_os",
               "average_cl_sb",
               "average_cl_ns",
               "average_cl_os",
               "average_nocm_sb",
               "average_nocm_ns",
               "average_nocm_os",
               "average_selectwthematic_sb",
               "average_selectwthematic_ns",
               "average_selectwthematic_os",
               "average_thematiconly_sb",
               "average_thematiconly_ns",
               "average_thematiconly_os"]

# set up manual color gradient
color_dict1 = {'l1': ["#7F50FCFF", "#7A5CF9FF", "#7569F7FF", "#7175F5FF", "#6C82F2FF",
                      "#678FF0FF", "#639BEEFF", "#5EA8EBFF", "#59B5E9FF", "#55C2E7FF"],
               'l2': ["#55C2E7FF", "#5FC7DDFF", "#6ACCD4FF", "#75D1CBFF", "#7FD6C1FF",
                      "#8ADCB8FF", "#94E1AFFF", "#9FE6A5FF", "#AAEB9CFF", "#B5F193FF"],
               'l3': ["#B5F193FF", "#BBEC8EFF", "#C1E78AFF", "#C7E386FF", "#CDDE82FF",
                      "#D3DA7EFF", "#D9D57AFF", "#DFD176FF", "#E5CC72FF", "#ECC86EFF"],
               'l4': ["#ECC86EFF", "#ECC169FF", "#ECBA65FF", "#EDB360FF", "#EDAC5CFF",
                      "#EDA457FF", "#EE9E53FF", "#EE974EFF", "#EE904AFF", "#EF8946FF"],
               'r1': ["#EF8946FF", "#EE8745FF", "#EE8645FF", "#EE8545FF",
                      "#EE8344FF", "#EE8244FF", "#EE8144FF", "#EE8043FF",
                      "#EE7E43FF", "#EE7D43FF", "#ED7C42FF", "#ED7B42FF",
                      "#ED7942FF", "#ED7841FF", "#ED7741FF", "#ED7641FF",
                      "#ED7440FF", "#ED7340FF", "#ED7240FF", "#ED713FFF",
                      "#EC6F3FFF", "#EC6E3FFF", "#EC6D3EFF", "#EC6C3EFF",
                      "#EC6A3EFF", "#EC693DFF", "#EC683DFF", "#EC673DFF",
                      "#EC653CFF", "#EC643CFF", "#EB633CFF", "#EB623CFF",
                      "#EB603BFF", "#EB5F3BFF", "#EB5E3BFF", "#EB5D3AFF",
                      "#EB5B3AFF", "#EB5A3AFF", "#EB5939FF", "#EB5839FF",
                      "#EA5639FF", "#EA5538FF", "#EA5438FF", "#EA5338FF",
                      "#EA5137FF", "#EA5037FF", "#EA4F37FF", "#EA4E36FF",
                      "#EA4C36FF", "#EA4B36FF", "#E94A35FF", "#E94935FF",
                      "#E94735FF", "#E94634FF", "#E94534FF", "#E94434FF",
                      "#E94233FF", "#E94133FF", "#E94033FF", "#E93F33FF"]}

list_of_lists = [
    color_dict1['l1'],
    color_dict1['l2'],
    color_dict1['l3'],
    color_dict1['l4'],
    color_dict1['r1']]

flattened = [val for sublist in list_of_lists for val in sublist]
mycolorbar1 = LinearSegmentedColormap.from_list('mycolorbar1', flattened)


def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)

# functions:


def compute_proportions(df, var):
    '''computes predicted proportion of gid cells with outcome variable.'''
    print("var:", var)
    df_grouped = df.groupby(['name', 'month_str'])[[var]].mean()
    df_grouped.reset_index(inplace=True)
    df_grouped['prop'] = df_grouped[var]
    df_grouped.drop(columns=[var], inplace=True)

    return df_grouped


def plot_heatmap(df, var, output):
    '''pivots data and plots heatmap.'''
    df_merge = compute_proportions(df, var)
    # take logit and pivot for heatmap
    df_merge['prop_logit'] = np.log(df_merge['prop'] / (1-df_merge['prop']))
    df_matrix = df_merge.pivot(
        index='name', columns='month_str', values='prop_logit')
    # plot heatmap:
    # set size
    plt.figure(figsize=(15, 10))
    # set axes
    ax = sns.heatmap(df_matrix, cmap=mycolorbar1, vmin=np.log(.001/(1-.001)),
                     vmax=np.log(.99/(1-.99)), linewidths=.003)
    ax.set_ylabel('')
    ax.set_xlabel('')
    # colorbar
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([np.log(0.005/(1-0.005)), np.log(0.05/(1-0.05)),
                    np.log(0.40/(1-0.40)), np.log(0.90/(1-0.90)),
                    np.log(0.99/(1-0.99))])
    cbar.set_ticklabels(["0.5%", "5%", "40%", "90%", "99%"])
    # finish and save figure
    path_output = "{}heatmap_{}.pdf".format(output, var)
    plt.title("Country proportions for {} \nEnsemble run: {}".format(var, run_id),
              loc='left')
    plt.savefig(path_output)
    plt.close()
    print("Wrote ", path_output)


# set up output path
dir_output = "/storage/runs/current/plot/heatmaps/"
create_dirs([dir_output])

# run:
for outcome in outcomes:
    plot_heatmap(df, outcome, dir_output)

for prediction in predictions:
    plot_heatmap(df, prediction, dir_output)
