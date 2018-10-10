import argparse
import json

run_id = "cm_canon_inst_eval_calib"
timevar = "month_id"
groupvar = "country_id"

ts = []

spatial = []

transforms = [
  {
    "f": "log_natural",
    "name": "ln_fvp_timesinceregimechange",
    "var": "fvp_timesinceregimechange"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_timeindep",
    "var": "fvp_timeindep"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_timesincepreindepwar",
    "var": "fvp_timesincepreindepwar"
  }
]

models = [
  {
    "formula": "ged_dummy_ns ~ ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_canon_inst_eval_calib_ns"
  },
  {
    "formula": "ged_dummy_os ~ ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_canon_inst_eval_calib_os"
  },
  {
    "formula": "ged_dummy_sb ~ ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_canon_inst_eval_calib_sb"
  }
]

mean          = {"stat" : "mean"}
var           = {"stat" : "var"}
skew          = {"stat" : "skew"}
kurtosis      = {"stat" : "kurtosis"}
pct1          = {"stat" : "pctile", "q" : 1}
pct5          = {"stat" : "pctile", "q" : 5}
pct10         = {"stat" : "pctile", "q" : 10}
pct25         = {"stat" : "pctile", "q" : 25}
pct50         = {"stat" : "pctile", "q" : 50}
pct75         = {"stat" : "pctile", "q" : 75}
pct90         = {"stat" : "pctile", "q" : 90}
pct95         = {"stat" : "pctile", "q" : 95}
pct99         = {"stat" : "pctile", "q" : 99}

vars_plots = ["col", "row", "longitude", "latitude", "gwcode"]
vars_plots_outcomes = ["ged_dummy_ns", "ged_dummy_os", "ged_dummy_sb"]

stats = [mean]

nsim = 1000

train_start = 121
train_end = 384
sim_start = 385
sim_end = 420

############################################################################################
################################## DON'T CHANGE BELOW HERE #################################
############################################################################################


data = {'timevar'   : timevar,
        'groupvar'  : groupvar}

times = {   'train_start' : train_start,
            'train_end' : train_end,
            'sim_start' : sim_start,
            'sim_end' : sim_end,
            'full_start' : min(train_start, sim_start),
            'full_end' : max(train_end, sim_end)}

p = {   'run_id' : run_id,
        'data' : data,
        'ts' : ts,
        'spatial': spatial,
        'transforms' : transforms,
        'models' : models,
        'times' : times,
        'nsim' : nsim,
        'stats' : stats,
        'vars_plots' : vars_plots,
        'vars_plots_outcomes' : vars_plots_outcomes}



parser = argparse.ArgumentParser()
parser.add_argument("--dir_scratch", type=str,
    help="directory in which to save data")
args = parser.parse_args()

dir_scratch = args.dir_scratch

path_params =  dir_scratch + "params.json"

with open (path_params, 'w') as j:
        json.dump(p, j)
        print("Wrote", path_params)
