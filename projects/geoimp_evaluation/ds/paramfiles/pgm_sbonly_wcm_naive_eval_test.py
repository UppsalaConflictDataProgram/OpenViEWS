import argparse
import json

run_id = "pgm_sbonly_wcm_naive_eval_test"
timevar = "month_id"
groupvar = "pg_id"

ts = [
  {
    "name": "l5_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 5
  },
  {
    "name": "l12_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 12
  },
  {
    "name": "l2_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 2
  },
  {
    "name": "l10_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 10
  },
  {
    "name": "l8_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 8
  },
  {
    "name": "l7_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 7
  },
  {
    "name": "l3_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 3
  },
  {
    "name": "l9_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 9
  },
  {
    "name": "l4_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 4
  },
  {
    "name": "l6_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 6
  },
  {
    "name": "l1_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 1
  },
  {
    "name": "cw_ged_dummy_sb_0",
    "var": "ged_dummy_sb",
    "cw": "==0"
  },
  {
    "name": "l11_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 11
  }
] 

spatial = [
  {
    "name": "q_1_1_l2_ged_dummy_sb",
    "var": "l2_ged_dummy_sb",
    "srule": "q",
    "first": 1,
    "last": 1
  },
  {
    "name": "q_1_1_l3_ged_dummy_sb",
    "var": "l3_ged_dummy_sb",
    "srule": "q",
    "first": 1,
    "last": 1
  },
  {
    "name": "q_1_1_l1_ged_dummy_sb",
    "var": "l1_ged_dummy_sb",
    "srule": "q",
    "first": 1,
    "last": 1
  }
]

transforms = [
  {
    "name": "ln_dist_petroleum",
    "f": "log_natural",
    "var": "dist_petroleum_s_wgs"
  },
  {
    "name": "ln_ttime",
    "f": "log_natural",
    "var": "ttime_mean"
  },
  {
    "name": "ln_fvp_timesincepreindepwar",
    "f": "log_natural",
    "var": "fvp_timesincepreindepwar"
  },
  {
    "name": "ln_dist_diamsec",
    "f": "log_natural",
    "var": "dist_diamsec_s_wgs"
  },
  {
    "name": "ln_bdist3",
    "f": "log_natural",
    "var": "bdist3"
  },
  {
    "name": "ln_fvp_population200",
    "f": "log_natural",
    "var": "fvp_population200"
  },
  {
    "name": "decay_12_cw_ged_dummy_sb_0",
    "f": "decay",
    "halflife": 12,
    "var": "cw_ged_dummy_sb_0"
  },
  {
    "name": "ln_fvp_timeindep",
    "f": "log_natural",
    "var": "fvp_timeindep"
  },
  {
    "name": "ln_pop",
    "f": "log_natural",
    "var": "pop_li_gpw_sum"
  },
  {
    "name": "ln_capdist",
    "f": "log_natural",
    "var": "capdist_li"
  },
  {
    "name": "ln_fvp_timesinceregimechange",
    "f": "log_natural",
    "var": "fvp_timesinceregimechange"
  }
]

models = [
  {
    "name": "pgm_sbonly_wcm_eval_test_sb",
    "formula": "ged_dummy_sb ~ l2_ged_dummy_sb + l3_ged_dummy_sb + l4_ged_dummy_sb + l5_ged_dummy_sb + l6_ged_dummy_sb + l7_ged_dummy_sb + l8_ged_dummy_sb + l9_ged_dummy_sb + l10_ged_dummy_sb + l11_ged_dummy_sb + l12_ged_dummy_sb + q_1_1_l2_ged_dummy_sb + q_1_1_l3_ged_dummy_sb + l1_ged_dummy_sb + decay_12_cw_ged_dummy_sb_0 + q_1_1_l1_ged_dummy_sb + ln_bdist3 + ln_ttime + ln_capdist + ln_pop + ln_dist_diamsec + ln_dist_petroleum + gcp_li_mer + imr_mean + mountains_mean + urban_ih_li + excluded_dummy_li + agri_ih_li + barren_ih_li + forest_ih_li + savanna_ih_li + shrub_ih_li + pasture_ih_li + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + ln_fvp_population200 + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + ssp2_edu_sec_15_24_prop + fvp_prop_excluded + ssp2_urban_share_iiasa",
    "modtype": "SMLogit"
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
vars_plots_outcomes = ["ged_dummy_sb"]

stats = [mean]

nsim = 5000

train_start = 121
train_end = 408
sim_start = 409
sim_end = 444

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