# possible values are 
# "logodds", "prob", "interval",
# "ortho", "cyl"

import argparse
import sys
import utils

sys.path.append("../..")
import views_utils.dbutils as dbutils


parser = argparse.ArgumentParser()
parser.add_argument("--schema", 
    type=str,
    help="schema to read table from", 
    required=True)
parser.add_argument("--table", 
    type=str,
    help="table to plot", 
    required=True)
parser.add_argument("--groupvar", 
    type=str,
    help="groupvar", 
    required=True)
parser.add_argument("--timevar", 
    type=str,
    help="timevar", 
    required=True)

parser.add_argument("--spaghetti", 
    action='store_true',
    help="Plot spaghetti")
parser.add_argument("--histogram", 
    action='store_true',
    help="Plot histograms")
parser.add_argument("--lpg", 
    action='store_true',
    help="Plot lines per group")
parser.add_argument("--abt", 
    action='store_true',
    help="Plot aggregates by time")
parser.add_argument("--pgcm", 
    action='store_true',
    help="Plot pg predictions at cm level")
parser.add_argument("--lpgwa",
    action='store_true',
    help="Plot lines per group with actuals")
parser.add_argument("--wawa",
    action='store_true',
    help="Plot world average with actuals")


args_main = parser.parse_args()

schema = args_main.schema
table = args_main.table
groupvar = args_main.groupvar
timevar = args_main.timevar

plot_spaghetti = args_main.spaghetti
plot_hist = args_main.histogram
plot_lpg = args_main.lpg
plot_abt = args_main.abt
plot_pgcm = args_main.pgcm
plot_lpgwa = args_main.lpgwa
plot_wawa = args_main.wawa


all_plot_bools = [plot_spaghetti, plot_hist, plot_lpg, plot_abt, 
                  plot_pgcm, plot_lpgwa, plot_wawa]

if not True in all_plot_bools:
    print("You didn't specify any plot types, exiting")
    sys.exit(1)

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
    port="5432", prefix="postgres",uname="VIEWSADMIN")

dir_descriptive = "/storage/runs/current/descriptive"
dir_table = "/".join([dir_descriptive, schema, table])

df = dbutils.db_to_df(connectstring, schema, table, ids=[timevar, groupvar])
df.sort_index(inplace=True)

if plot_wawa:
    utils.plot_world_average_with_actuals(df, connectstring, dir_table, 
                                          timevar, groupvar)
if plot_spaghetti:
    utils.plot_spaghetties(df, connectstring, dir_table)
if plot_hist:
    utils.plot_histograms(df, dir_table)
if plot_lpg:
    utils.plot_lines_per_group(df, dir_table)
if plot_abt:
    utils.plot_stats_by_time(df, dir_table)
if plot_pgcm:
    utils.plot_pgcm(df, connectstring, dir_table)
if plot_lpgwa:
    utils.plot_lines_per_group_with_actuals(df, connectstring, dir_table)

