import argparse
import json

run_id = "cy_growth"
timevar = "year_id"
groupvar = "country_id"

ts = [
  {
    "name": "l1_gdp",
    "var": "gdp",
    "lag": 1
  },
  {
    "name": "ma3_delta_gdp",
    "var": "delta_gdp",
    "ma": 3
  },
  {
    "name": "ma3_delta_gdp_exog",
    "var": "delta_gdp_exog",
    "ma": 3
  },
  {
    "name": "l1_conflict",
    "var": "conflict",
    "lag": 1
  },
  {
    "name": "l1_delta_gdp",
    "var": "delta_gdp",
    "lag": 7
  },
  {
    "name": "cw_conflict_0",
    "var": "conflict",
    "cw": "==0"
  },
] 

spatial = [
  {
    "name": "q_1_1_l1_conflict",
    "var": "conflict",
    "srule": "q",
    "first": 1,
    "last": 1
  }
]

transforms = [
  {
    "name": "decay_3_cw_conflict_0",
    "f": "decay",
    "halflife": 3,
    "var": "cw_conflict_0"
  }
]

transforms_post = [
  {
    "name" : "gdp",
    "a" : "l1_gdp",
    "b" : "delta_gdp",
    "f" : "add"
  }
]

models = [
  {
    "name": "delta_gdp",
    "formula": "delta_gdp ~ ma3_delta_gdp_exog + decay_3_cw_conflict_0",
    "modtype": "SMIdentity"
  },
  {
    "name": "conflict",
    "formula": "conflict ~ l1_delta_gdp + l1_gdp + l1_conflict + decay_3_cw_conflict_0",
    'modtype' : "SMLogit"
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
vars_plots_outcomes = ["conflict"]

stats = [mean]

nsim = 4

train_start = 1980
train_end = 2009
sim_start = 2010
sim_end = 2100

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
        'transforms_post' : transforms_post,
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