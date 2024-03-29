import argparse
import json

run_id = "pgm_pronly_wcm_fcast_calib"
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
    "f": "log_natural",
    "name": "ln_dist_diamsec",
    "var": "dist_diamsec_s_wgs"
  },
  {
    "f": "decay",
    "halflife": 12,
    "name": "decay_12_cw_acled_dummy_pr_0",
    "var": "cw_acled_dummy_pr_0"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_population200",
    "var": "fvp_population200"
  },
  {
    "f": "log_natural",
    "name": "ln_dist_petroleum",
    "var": "dist_petroleum_s_wgs"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_timesincepreindepwar",
    "var": "fvp_timesincepreindepwar"
  },
  {
    "f": "log_natural",
    "name": "ln_ttime",
    "var": "ttime_mean"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_timeindep",
    "var": "fvp_timeindep"
  },
  {
    "f": "log_natural",
    "name": "ln_capdist",
    "var": "capdist_li"
  },
  {
    "f": "log_natural",
    "name": "ln_bdist3",
    "var": "bdist3"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_timesinceregimechange",
    "var": "fvp_timesinceregimechange"
  },
  {
    "f": "log_natural",
    "name": "ln_pop",
    "var": "pop_li_gpw_sum"
  }
]

models = [
  {
    "formula": "acled_dummy_pr ~ l2_acled_dummy_pr + l3_acled_dummy_pr + l4_acled_dummy_pr + l5_acled_dummy_pr + l6_acled_dummy_pr + l7_acled_dummy_pr + l8_acled_dummy_pr + l9_acled_dummy_pr + l10_acled_dummy_pr + l11_acled_dummy_pr + l12_acled_dummy_pr + q_1_1_l2_acled_dummy_pr + q_1_1_l3_acled_dummy_pr + l1_acled_dummy_pr + decay_12_cw_acled_dummy_pr_0 + q_1_1_l1_acled_dummy_pr + ln_dist_diamsec + ln_dist_petroleum + agri_ih_li + barren_ih_li + forest_ih_li + mountains_mean + savanna_ih_li + shrub_ih_li + pasture_ih_li + urban_ih_li + ln_bdist3 + ln_ttime + ln_capdist + ln_pop + gcp_li_mer + imr_mean + excluded_dummy_li + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded + ln_fvp_population200 + ssp2_edu_sec_15_24_prop + ssp2_urban_share_iiasa",
    "modtype": "SMLogit",
    "name": "pgm_pronly_wcm_fcast_calib_pr"
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
vars_plots_outcomes = ["acled_dummy_pr"]

stats = [mean]

nsim = 1000

train_start = 121
train_end = 428
sim_start = 429
sim_end = 464

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
