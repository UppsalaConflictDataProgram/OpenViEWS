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
parser.add_argument("--groupvar", type=str,
    help="groupvar")
parser.add_argument("--timevar", type=str,
    help="timevar")
parser.add_argument("--crop", type=str,
    help="Allowed values are africa and world")
parser.add_argument("--run_id", type=str,
    help="Run ID to tag the maps with")
parser.add_argument("--scale", type=str,
    help="logodds, prob or interval")
parser.add_argument("--plotvar", type=str, action='append', required=True,
    help="Var to plot. Supply once for each.")

args_main = parser.parse_args()

schema = args_main.schema
table = args_main.table
groupvar = args_main.groupvar
timevar = args_main.timevar
crop = args_main.crop
run_id = args_main.run_id
plotvars = args_main.plotvar
variable_scale = args_main.scale

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
    port="5432", prefix="postgres",uname="VIEWSADMIN")

local_settings = {
    "connectstring" : connectstring,
    "dir_plots"     : "/storage/runs/current/maps/",
    "dir_spatial_pgm" : "/storage/runs/current/ds/input/pgm/spatial/",
    "dir_spatial_cm"  : "/storage/runs/current/ds/input/cm/spatial/",
}


n_plotvars = len(plotvars)
i = 1
print("You specified {} vars to plot".format(n_plotvars))
for plotvar in plotvars:
    print("Plotting var {i} of {n_plotvars}".format(i=i, n_plotvars=n_plotvars))
    plotjob = {
               'plotvar' : plotvar, 
               'varname_actual' : None, 
               'schema_plotvar' : 'launched', 
               'schema_actual' : None, 
               'table_plotvar' : table, 
               'table_actual' : None, 
               'timevar' : timevar, 
               'groupvar' : groupvar, 
               'variable_scale' : variable_scale, 
               'projection' : 'cyl', 
               'crop' : crop, 
               'run_id' : run_id
               }

    maputils.plot_map_worker(local_settings=local_settings, plotjob=plotjob)
