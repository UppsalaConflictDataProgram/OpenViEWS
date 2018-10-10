import argparse
import json

run_id = "pgm_acled_protest_eval_test"
timevar = "month_id"
groupvar = "pg_id"

ts = [
  {
    "lag": 10,
    "name": "l10_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 9,
    "name": "l9_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 7,
    "name": "l7_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 8,
    "name": "l8_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 1,
    "name": "l1_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 12,
    "name": "l12_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 4,
    "name": "l4_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 3,
    "name": "l3_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 6,
    "name": "l6_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "cw": "==0",
    "name": "cw_acled_dummy_pr_0",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 2,
    "name": "l2_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 5,
    "name": "l5_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 11,
    "name": "l11_acled_dummy_pr",
    "var": "acled_dummy_pr"
  }
]

spatial = [
  {
    "first": 1,
    "last": 1,
    "name": "q_1_1_l2_acled_dummy_pr",
    "srule": "q",
    "var": "l2_acled_dummy_pr"
  },
  {
    "first": 1,
    "last": 1,
    "name": "q_1_1_l3_acled_dummy_pr",
    "srule": "q",
    "var": "l3_acled_dummy_pr"
  },
  {
    "first": 1,
    "last": 1,
    "name": "q_1_1_l1_acled_dummy_pr",
    "srule": "q",
    "var": "l1_acled_dummy_pr"
  }
]

transforms = [
  {
    "f": "decay",
    "halflife": 12,
    "name": "decay_12_cw_acled_dummy_pr_0",
    "var": "cw_acled_dummy_pr_0"
  }
]

models = [
  {
    "formula": "ged_dummy_ns ~ l2_acled_dummy_pr + l3_acled_dummy_pr + l4_acled_dummy_pr + l5_acled_dummy_pr + l6_acled_dummy_pr + l7_acled_dummy_pr + l8_acled_dummy_pr + l9_acled_dummy_pr + l10_acled_dummy_pr + l11_acled_dummy_pr + l12_acled_dummy_pr + q_1_1_l2_acled_dummy_pr + q_1_1_l3_acled_dummy_pr + l1_acled_dummy_pr + decay_12_cw_acled_dummy_pr_0 + q_1_1_l1_acled_dummy_pr",
    "modtype": "SMLogit",
    "name": "pgm_acled_protest_eval_test_ns"
  },
  {
    "formula": "ged_dummy_os ~ l2_acled_dummy_pr + l3_acled_dummy_pr + l4_acled_dummy_pr + l5_acled_dummy_pr + l6_acled_dummy_pr + l7_acled_dummy_pr + l8_acled_dummy_pr + l9_acled_dummy_pr + l10_acled_dummy_pr + l11_acled_dummy_pr + l12_acled_dummy_pr + q_1_1_l2_acled_dummy_pr + q_1_1_l3_acled_dummy_pr + l1_acled_dummy_pr + decay_12_cw_acled_dummy_pr_0 + q_1_1_l1_acled_dummy_pr",
    "modtype": "SMLogit",
    "name": "pgm_acled_protest_eval_test_os"
  },
  {
    "formula": "acled_dummy_pr ~ l2_acled_dummy_pr + l3_acled_dummy_pr + l4_acled_dummy_pr + l5_acled_dummy_pr + l6_acled_dummy_pr + l7_acled_dummy_pr + l8_acled_dummy_pr + l9_acled_dummy_pr + l10_acled_dummy_pr + l11_acled_dummy_pr + l12_acled_dummy_pr + q_1_1_l2_acled_dummy_pr + q_1_1_l3_acled_dummy_pr + l1_acled_dummy_pr + decay_12_cw_acled_dummy_pr_0 + q_1_1_l1_acled_dummy_pr",
    "modtype": "SMLogit",
    "name": "pgm_acled_protest_eval_test_pr"
  },
  {
    "formula": "ged_dummy_sb ~ l2_acled_dummy_pr + l3_acled_dummy_pr + l4_acled_dummy_pr + l5_acled_dummy_pr + l6_acled_dummy_pr + l7_acled_dummy_pr + l8_acled_dummy_pr + l9_acled_dummy_pr + l10_acled_dummy_pr + l11_acled_dummy_pr + l12_acled_dummy_pr + q_1_1_l2_acled_dummy_pr + q_1_1_l3_acled_dummy_pr + l1_acled_dummy_pr + decay_12_cw_acled_dummy_pr_0 + q_1_1_l1_acled_dummy_pr",
    "modtype": "SMLogit",
    "name": "pgm_acled_protest_eval_test_sb"
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
vars_plots_outcomes = ["ged_dummy_ns", "ged_dummy_os", "acled_dummy_pr", "ged_dummy_sb"]

stats = [mean]

nsim = 1000

train_start = 205
train_end = 420
sim_start = 421
sim_end = 456

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
