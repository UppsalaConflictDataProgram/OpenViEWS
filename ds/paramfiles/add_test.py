

import argparse
import json

run_id = "add_test" # same name as the paramfile!
timevar = "year"
groupvar = "gwno"

ts = [
    {"name" : "cw_conflict_0",       "var" : "conflict",      "cw": "==0", 
            "seed" : 999},
    {"name" : "l1_conflict",         "var" : "conflict",      "lag" : 1},
    {"name" : "l1_gdp",         "var" : "gdp",      "lag" : 1},
    {"name" : "ma3_delta_gdp",         "var" : "delta_gdp",      "ma" : 3},
    {"name" : "ma3_gdp",         "var" : "gdp",      "ma" : 3},
    {"name" : "l1_delta_gdp",   "var" : "delta_gdp",      "lag" : 1},    

    ] 

spatial = []

transforms = [
    {   'name' : 'decay_2_cw_conflict_0', 'f' : 'decay', 'halflife' : 2, 
            'var' : 'cw_conflict_0'},

    # {   'name' : 'delta_gdp', 
    #         'a' : 'gdp', 
    #         'b' : 'l1_gdp', 
    #         'f' : 'subtract' },

]

transforms_post = [
    {"name" : "gdp", 
        "a" : "l1_gdp", 
        "b" : "delta_gdp", 
        "f" : "add"}]

gdp_growth = {
    'name' : 'gdp_growth' ,
    'formula' : "delta_gdp ~ ma3_delta_gdp + decay_2_cw_conflict_0",
    'modtype' : 'SMIdentity'}

conflict = { 
    'name' : 'conflict', 
    'formula' : 'conflict ~ ma3_gdp + decay_2_cw_conflict_0',
    'modtype' : 'SMLogit'}

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

models = [gdp_growth, conflict]

vars_plots = []
vars_plots_outcomes = []

stats = [mean]

nsim = 10

train_start = 1980
train_end = 2020
sim_start = 2021
sim_end = 2050

################################################################################
######################## DON'T CHANGE BELOW HERE ###############################
################################################################################

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