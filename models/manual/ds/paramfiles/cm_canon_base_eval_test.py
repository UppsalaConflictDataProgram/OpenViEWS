import argparse
import json

run_id = "cm_canon_base_eval_test"
timevar = "month_id"
groupvar = "country_id"

ts = [
  {
    "name": "l1_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 1
  },
  {
    "name": "l10_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 10
  },
  {
    "name": "l5_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 5
  },
  {
    "name": "l8_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 8
  },
  {
    "name": "l1_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 1
  },
  {
    "name": "l4_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 4
  },
  {
    "name": "l4_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 4
  },
  {
    "name": "l7_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 7
  },
  {
    "name": "l7_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 7
  },
  {
    "name": "l9_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 9
  },
  {
    "name": "cw_ged_dummy_os_0",
    "var": "ged_dummy_os",
    "cw": "==0"
  },
  {
    "name": "l11_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 11
  },
  {
    "name": "l12_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 12
  },
  {
    "name": "l3_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 3
  },
  {
    "name": "l7_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 7
  },
  {
    "name": "l6_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 6
  },
  {
    "name": "l9_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 9
  },
  {
    "name": "l12_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 12
  },
  {
    "name": "l10_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 10
  },
  {
    "name": "l5_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 5
  },
  {
    "name": "l5_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 5
  },
  {
    "name": "l1_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 1
  },
  {
    "name": "l11_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 11
  },
  {
    "name": "l8_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 8
  },
  {
    "name": "l2_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 2
  },
  {
    "name": "l10_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 10
  },
  {
    "name": "l3_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 3
  },
  {
    "name": "l6_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 6
  },
  {
    "name": "l6_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 6
  },
  {
    "name": "l4_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 4
  },
  {
    "name": "l11_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 11
  },
  {
    "name": "l9_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 9
  },
  {
    "name": "l8_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 8
  },
  {
    "name": "cw_ged_dummy_sb_0",
    "var": "ged_dummy_sb",
    "cw": "==0"
  },
  {
    "name": "l12_ged_dummy_sb",
    "var": "ged_dummy_sb",
    "lag": 12
  },
  {
    "name": "l2_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 2
  },
  {
    "name": "l3_ged_dummy_ns",
    "var": "ged_dummy_ns",
    "lag": 3
  },
  {
    "name": "cw_ged_dummy_ns_0",
    "var": "ged_dummy_ns",
    "cw": "==0"
  },
  {
    "name": "l2_ged_dummy_os",
    "var": "ged_dummy_os",
    "lag": 2
  }
] 

spatial = []

transforms = [
  {
    "name": "ln_fvp_population200",
    "f": "log_natural",
    "var": "fvp_population200"
  },
  {
    "name": "ln_fvp_timesincepreindepwar",
    "f": "log_natural",
    "var": "fvp_timesincepreindepwar"
  },
  {
    "name": "ln_fvp_timeindep",
    "f": "log_natural",
    "var": "fvp_timeindep"
  },
  {
    "name": "decay_12_cw_ged_dummy_ns_0",
    "f": "decay",
    "halflife": 12,
    "var": "cw_ged_dummy_ns_0"
  },
  {
    "name": "decay_12_cw_ged_dummy_os_0",
    "f": "decay",
    "halflife": 12,
    "var": "cw_ged_dummy_os_0"
  },
  {
    "name": "ln_fvp_timesinceregimechange",
    "f": "log_natural",
    "var": "fvp_timesinceregimechange"
  },
  {
    "name": "decay_12_cw_ged_dummy_sb_0",
    "f": "decay",
    "halflife": 12,
    "var": "cw_ged_dummy_sb_0"
  }
]

models = [
  {
    "name": "cm_canon_base_eval_test_ns",
    "formula": "ged_dummy_ns ~ l2_ged_dummy_ns + l3_ged_dummy_ns + l4_ged_dummy_ns + l5_ged_dummy_ns + l6_ged_dummy_ns + l7_ged_dummy_ns + l8_ged_dummy_ns + l9_ged_dummy_ns + l10_ged_dummy_ns + l11_ged_dummy_ns + l12_ged_dummy_ns + l1_ged_dummy_sb + l1_ged_dummy_ns + l1_ged_dummy_os + decay_12_cw_ged_dummy_sb_0 + decay_12_cw_ged_dummy_ns_0 + decay_12_cw_ged_dummy_os_0 + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + ln_fvp_population200 + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + ssp2_edu_sec_15_24_prop + fvp_prop_excluded + ssp2_urban_share_iiasa",
    "modtype": "SMLogit"
  },
  {
    "name": "cm_canon_base_eval_test_os",
    "formula": "ged_dummy_os ~ l2_ged_dummy_os + l3_ged_dummy_os + l4_ged_dummy_os + l5_ged_dummy_os + l6_ged_dummy_os + l7_ged_dummy_os + l8_ged_dummy_os + l9_ged_dummy_os + l10_ged_dummy_os + l11_ged_dummy_os + l12_ged_dummy_os + l1_ged_dummy_sb + l1_ged_dummy_ns + l1_ged_dummy_os + decay_12_cw_ged_dummy_sb_0 + decay_12_cw_ged_dummy_ns_0 + decay_12_cw_ged_dummy_os_0 + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + ln_fvp_population200 + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + ssp2_edu_sec_15_24_prop + fvp_prop_excluded + ssp2_urban_share_iiasa",
    "modtype": "SMLogit"
  },
  {
    "name": "cm_canon_base_eval_test_sb",
    "formula": "ged_dummy_sb ~ l2_ged_dummy_sb + l3_ged_dummy_sb + l4_ged_dummy_sb + l5_ged_dummy_sb + l6_ged_dummy_sb + l7_ged_dummy_sb + l8_ged_dummy_sb + l9_ged_dummy_sb + l10_ged_dummy_sb + l11_ged_dummy_sb + l12_ged_dummy_sb + l1_ged_dummy_sb + l1_ged_dummy_ns + l1_ged_dummy_os + decay_12_cw_ged_dummy_sb_0 + decay_12_cw_ged_dummy_ns_0 + decay_12_cw_ged_dummy_os_0 + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + ln_fvp_population200 + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + ssp2_edu_sec_15_24_prop + fvp_prop_excluded + ssp2_urban_share_iiasa",
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
vars_plots_outcomes = ["ged_dummy_ns", "ged_dummy_os", "ged_dummy_sb"]

stats = [mean]

nsim = 1000

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