# possible values are
# "logodds", "prob", "interval",
# "ortho", "cyl"

import argparse
import sys
import maputils

sys.path.append("../..")
import views_utils.dbutils as dbutils


parser = argparse.ArgumentParser()
parser.add_argument("--schema", type=str,
    help="schema to read table from")
parser.add_argument("--table", type=str,
    help="table to plot")
parser.add_argument("--table_actual", type=str,
    help="table in preflight containing actual outcomes")
parser.add_argument("--groupvar", type=str,
    help="groupvar")
parser.add_argument("--timevar", type=str,
    help="timevar")
parser.add_argument("--crop", type=str,
    help="Allowed values are africa and world")
parser.add_argument("--scale", type=str,
    help="logodds, prob or interval")
parser.add_argument("--run_id", type=str,
    help="Run ID to tag the maps with")

args_main = parser.parse_args()

schema = args_main.schema
table = args_main.table
table_actual = args_main.table_actual
groupvar = args_main.groupvar
timevar = args_main.timevar
crop = args_main.crop
run_id = args_main.run_id
variable_scale = args_main.scale

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST",
    port="5432", prefix="postgres",uname="VIEWSADMIN")

local_settings = {
    "connectstring" : connectstring,
    "dir_plots"     : "/proj/snic2018-3-380/runs/current/maps/",
    "dir_spatial_pgm" : "/proj/snic2018-3-380/runs/current/ds/input/pgm/spatial/",
    "dir_spatial_cm"  : "/proj/snic2018-3-380/runs/current/ds/input/cm/spatial/",
}

plotjobs = maputils.make_plotjobs_table(
    connectstring = connectstring,
    schema = schema,
    table = table,
    schema_actual = "preflight",
    table_actual = table_actual,
    variable_scale = variable_scale,
    projection = "cyl",
    groupvar = groupvar,
    timevar = timevar,
    crop=crop,
    run_id=run_id,
    )

for plotjob in plotjobs:
    maputils.plot_map_worker(local_settings, plotjob)
