import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

import sys
sys.path.append("../../")
import views_utils.dbutils as dbutils
import plot.maps.maputils as maputils

import itertools

def get_times_actuals(df):
    # Make time limits for actuals so that we can have 2/3 of the ts as 
    # actuals and 1/3 predictions.
    # For use in time series plots
    
    t_start = int(df.index.get_level_values(0).min())
    t_end = int(df.index.get_level_values(0).max())
    t_length_predictions = int(t_end-t_start) + 1
    print("predictions:", t_start, t_end, t_length_predictions)
    t_length_actuals = t_length_predictions*2
    t_end_actuals = t_start - 1
    t_start_actuals = t_end_actuals - t_length_actuals
    print("actuals:", t_start_actuals, t_end_actuals, t_length_actuals)
    return t_start_actuals, t_end_actuals

def make_ticks(df, df_months):
    x_vals = sorted(list(set(df.index.get_level_values(0))))
    x_vals_ids = list(range(0, len(x_vals), 12))
    x_vals = [ x_vals[i] for i in x_vals_ids]
    x_ticks = list(df_months.loc[x_vals]['datestr'])

    return x_vals, x_ticks

def fetch_df_country_names(connectstring):
    cols = ["id", "name"]
    df_names = dbutils.db_to_df(connectstring, "staging", "country", 
                                columns=cols, ids = ["id"])
    return df_names

def fetch_df_months(connectstring):

    cols = ["id", "month", "year_id"]
    df = dbutils.db_to_df(connectstring, "staging", "month", 
                                columns=cols)

    df['datestr'] = df['year_id'].map(str) + "-" + df['month'].map(str)

    df.rename(columns = {'id' : 'month_id'}, inplace=True)
    df.set_index(['month_id'], inplace=True)

    df = df[['datestr']]

    return df

def subset_times(df, start, end):
    df = df.loc[(df.index.get_level_values(0) >= start) 
               &(df.index.get_level_values(0) <= end)]
    return df

def get_numeric_cols(df):
    columns = df.select_dtypes(include=np.number).columns
    columns = sorted(columns)
    return columns

def get_groups(df):
    groups = sorted(list(set(df.index.get_level_values(1))))
    return groups

def get_times(df):
    times = sorted(list(set(df.index.get_level_values(0))))
    return times

def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)

def plot_histograms(df, directory):
    directory = directory + "/histogram/"
    create_dirs([directory])

    columns = get_numeric_cols(df)

    for col in columns:
        path = directory + col + ".png"
        plt.figure()
        plt.hist(df[col].dropna(), bins = 100)
        title = col
        plt.title(title)
        plt.savefig(path)
        print("wrote", path)
        plt.close()

def plot_spaghetties(df, connectstring, directory):
    directory = directory + "/spaghetti/"
    create_dirs([directory])

    lines = ["-","--","-.",":"]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    linecycler = itertools.cycle(lines)
    colorcycler = itertools.cycle(colors)

    #groups = get_groups(df)

    df_actuals = dbutils.db_to_df(connectstring, "landed", "agg_cm_actuals")
    df_actuals.set_index(['month_id', 'country_id'], inplace=True)
    df_actuals = subset_times(df_actuals, *get_times_actuals(df))

    df_months = fetch_df_months(connectstring)
    df_names = fetch_df_country_names(connectstring)

    df = df.merge(df_actuals, left_index=True, right_index=True, how='outer')

    
    columns = get_numeric_cols(df)
    for c in columns:
        path = directory + str(c) + ".png"

        global_median = df[c].median()

        # Plot the spaghetties with the highest mean country first
        df_means = df.groupby(level=1)[c].mean()
        df_means.sort_values(inplace=True, ascending=False)

        max_predicted_value = df[c].max()
        upper_limit_y = max_predicted_value*1.2

        plt.figure(figsize=(24,12))
        plt.ylim=(-0.001, upper_limit_y)


        for g in df_means.index:

            country_name = df_names.loc[g]['name']
            dg = df.xs(g, level=1)

            if dg[c].mean()>global_median:

                actual = maputils.match_plotvar_actual(c)
                actual = "pgm_" + actual

                ls = next(linecycler)
                color = next(colorcycler)
                plt.plot(dg[c], 
                         alpha=0.5, 
                         linestyle=ls,
                         color=color,
                         label=country_name)

                plt.plot(dg[actual], 
                         alpha=0.5, 
                         linestyle=ls,
                         color=color,
                         label=country_name)

        title = "{} - {}".format(g, c)
        plt.title(title)
        plt.legend(prop={'size': 8})
        plt.savefig(path)
        print("wrote", path)
        plt.close()

# def plot_lines_per_group(df, directory):
#     directory = directory + "/lpg/"
#     create_dirs([directory])

#     groups = get_groups(df)
#     columns = get_numeric_cols(df)

#     for g in groups:
#         dg = df.xs(g, level=groupvar)
#         for c in columns:
#             path = directory + str(int(g)) + "_" + str(c) + ".png"
#             plt.figure
#             plt.plot(dg[c])
#             plt.title(c)
#             plt.savefig(path)
#             print("wrote", path)
#             plt.close()

# def plot_cols(df, directory, label):
#     for c in df.columns:
#         plt.figure()
#         plt.plot(df[c])
#         title = "{} : {}".format(label, c)
#         plt.title(title)
#         path = directory + c + ".png"
#         plt.savefig(path)
#         print("wrote", path)
#         plt.close()

# def plot_stats_by_time(df, directory):
#     dir_mean = directory + "/stats_by_time/mean/"
#     dir_var = directory + "/stats_by_time/var/"
#     create_dirs([dir_mean, dir_var])

#     df_mean = df.groupby(level=0).mean()
#     df_var = df.groupby(level=0).var()

#     plot_cols(df_mean, dir_mean, label="mean")
#     plot_cols(df_var, dir_var, label="var")

# def plot_pgcm(df, connectstring, directory):

#     # Use this to create staging_test.cpgm if missing
#     query_country_priogrid_month = """
#     DROP TABLE IF EXISTS staging_test.cpgm;
#     CREATE TABLE staging_test.cpgm AS
#     SELECT
#       pgm.month_id,
#       pgm.priogrid_gid AS pg_id,
#       c.id AS country_id
#     FROM
#       staging.priogrid_month AS pgm
#     INNER JOIN
#       staging.country_month AS cm
#       ON pgm.country_month_id=cm.id
#     INNER JOIN
#       staging.country as c
#         ON cm.country_id=c.id
#     ;"""

#     # Fetch the country_id codes
#     df_cpgm = dbutils.db_to_df(connectstring, "staging_test", "cpgm")
#     df_cpgm.set_index(["month_id", "pg_id"], inplace=True)
#     df = df.merge(df_cpgm, left_index=True, right_index=True)

#     df_mean_by_cid = df.groupby(["country_id", "month_id"]).mean()
#     df_var_by_cid = df.groupby(["country_id", "month_id"]).var()

#     dir_mean = directory + "/pg_agg_by_country/mean/"
#     dir_var = directory + "/pg_agg_by_country/var/"
#     plot_cols(df_mean_by_cid, dir_mean, "mean")
#     plot_cols(df_var_by_cid, dir_mean, "var")

def plot_world_average_with_actuals(df, connectstring, directory, timevar, groupvar):
    directory = directory + "/world_avg_w_actuals/"
    create_dirs([directory])

    columns = get_numeric_cols(df)
    t_start_actuals, t_end_actuals = get_times_actuals(df)

    cols_actuals = ["ged_dummy_sb", "ged_dummy_ns", 
                    "ged_dummy_os", "acled_dummy_pr"]
    schema_actuals = "preflight"
    if groupvar == "pg_id":
        table_actuals = "flight_pgm"
    elif groupvar == "country_id":
        table_actuals = "flight_cm"


    df_actuals = dbutils.db_to_df_limited(connectstring, schema_actuals, 
                                  table_actuals, columns=cols_actuals, 
                                  timevar=timevar, groupvar=groupvar, 
                                  tmin=t_start_actuals,
                                  tmax=t_end_actuals)

    df_months = fetch_df_months(connectstring)

    df = df.merge(df_actuals, left_index=True, right_index=True, how='outer')

    df_mean = df.groupby(level=0).mean()

    for c in columns:

        actual = maputils.match_plotvar_actual(c)

        path = directory + "world_" + str(c) + ".png"
        plt.figure()

        plt.plot(df_mean[actual], label='History')
        plt.plot(df_mean[c], linestyle='--', label=c)

        plt.xticks(*make_ticks(df, df_months), rotation=90)

        #title = "{}\n{}".format("World", c)
        #plt.title(title, loc='left')
        plt.legend()

        plt.tight_layout()
        plt.savefig(path)
        print("wrote", path)
        plt.close()

def plot_lines_per_group_with_actuals(df, connectstring, directory):

    directory = directory + "/country_avg_w_actuals/"
    create_dirs([directory])

    groups = get_groups(df)
    columns = get_numeric_cols(df)

    df_actuals = dbutils.db_to_df(connectstring, "landed", "agg_cm_actuals")
    df_actuals.set_index(['month_id', 'country_id'], inplace=True)
    df_actuals = subset_times(df_actuals, *get_times_actuals(df))

    df_names = fetch_df_country_names(connectstring)
    df_months = fetch_df_months(connectstring)

    df = df.merge(df_actuals, left_index=True, right_index=True, how='outer')

    for g in groups:
        dg = df.xs(g, level=1)

        country_name = df_names.loc[g]['name']

        for c in columns:

            actual = maputils.match_plotvar_actual(c)
            actual = "pgm_" + actual


            path = directory + str(int(g)) + "_" + str(c) + ".png"
            plt.figure()

            # if max is below 1%, set that as the limit
            if dg[c].max()<0.01 and dg[actual].max()<0.01:
                plt.ylim([-0.0001, 0.01])
            # let the figure set its own limits
            else:
                pass

            plt.plot(dg[actual], label='History')
            plt.plot(dg[c], linestyle='--', label=c)

            plt.xticks(*make_ticks(df, df_months), rotation=90)

            title = "{}\n{}".format(country_name, c)
            title = country_name
            plt.title(title, loc='left')
            plt.legend()
            plt.tight_layout()
            plt.savefig(path)
            print("wrote", path)
            plt.close()




