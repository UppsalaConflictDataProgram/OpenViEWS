import argparse
import json

run_id = "cm_transforms"
timevar = "month_id"
groupvar = "country_id"

ts = [
  {
    "lag": 7,
    "name": "l7_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 12,
    "name": "l12_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 10,
    "name": "l10_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 6,
    "name": "l6_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 12,
    "name": "l12_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 5,
    "name": "l5_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 4,
    "name": "l4_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 9,
    "name": "l9_ged_dummy_sb",
    "var": "ged_dummy_sb"
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
    "lag": 3,
    "name": "l3_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 5,
    "name": "l5_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 11,
    "name": "l11_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 2,
    "name": "l2_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 3,
    "name": "l3_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 11,
    "name": "l11_ged_dummy_os",
    "var": "ged_dummy_os"
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
    "lag": 8,
    "name": "l8_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 7,
    "name": "l7_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 7,
    "name": "l7_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 9,
    "name": "l9_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 6,
    "name": "l6_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 10,
    "name": "l10_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 12,
    "name": "l12_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 2,
    "name": "l2_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 12,
    "name": "l12_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 8,
    "name": "l8_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 4,
    "name": "l4_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 8,
    "name": "l8_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 5,
    "name": "l5_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 11,
    "name": "l11_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 10,
    "name": "l10_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 6,
    "name": "l6_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 11,
    "name": "l11_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 4,
    "name": "l4_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 10,
    "name": "l10_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 8,
    "name": "l8_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "lag": 2,
    "name": "l2_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "lag": 3,
    "name": "l3_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 4,
    "name": "l4_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 9,
    "name": "l9_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "lag": 9,
    "name": "l9_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "lag": 7,
    "name": "l7_ged_dummy_os",
    "var": "ged_dummy_os"
  }
]

spatial = []

transforms = [
  {
    "f": "mean",
    "name": "mean_ged_dummy_sb",
    "var": "ged_dummy_sb"
  },
  {
    "f": "mean",
    "name": "mean_ged_dummy_os",
    "var": "ged_dummy_os"
  },
  {
    "f": "mean",
    "name": "mean_ged_dummy_ns",
    "var": "ged_dummy_ns"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_population200",
    "var": "fvp_population200"
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
  },
  {
    "f": "mean",
    "name": "mean_acled_dummy_pr",
    "var": "acled_dummy_pr"
  },
  {
    "f": "log_natural",
    "name": "ln_fvp_timesinceregimechange",
    "var": "fvp_timesinceregimechange"
  }
]

models = [
  {
    "formula": "ged_dummy_ns ~ l2_ged_dummy_ns + l3_ged_dummy_ns + l4_ged_dummy_ns + l5_ged_dummy_ns + l6_ged_dummy_ns + l7_ged_dummy_ns + l8_ged_dummy_ns + l9_ged_dummy_ns + l10_ged_dummy_ns + l11_ged_dummy_ns + l12_ged_dummy_ns + mean_ged_dummy_ns + ln_fvp_population200 + ssp2_edu_sec_15_24_prop + ssp2_urban_share_iiasa + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_transforms_ns"
  },
  {
    "formula": "ged_dummy_os ~ l2_ged_dummy_os + l3_ged_dummy_os + l4_ged_dummy_os + l5_ged_dummy_os + l6_ged_dummy_os + l7_ged_dummy_os + l8_ged_dummy_os + l9_ged_dummy_os + l10_ged_dummy_os + l11_ged_dummy_os + l12_ged_dummy_os + mean_ged_dummy_os + ln_fvp_population200 + ssp2_edu_sec_15_24_prop + ssp2_urban_share_iiasa + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_transforms_os"
  },
  {
    "formula": "acled_dummy_pr ~ l2_acled_dummy_pr + l3_acled_dummy_pr + l4_acled_dummy_pr + l5_acled_dummy_pr + l6_acled_dummy_pr + l7_acled_dummy_pr + l8_acled_dummy_pr + l9_acled_dummy_pr + l10_acled_dummy_pr + l11_acled_dummy_pr + l12_acled_dummy_pr + mean_acled_dummy_pr + ln_fvp_population200 + ssp2_edu_sec_15_24_prop + ssp2_urban_share_iiasa + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_transforms_pr"
  },
  {
    "formula": "ged_dummy_sb ~ l2_ged_dummy_sb + l3_ged_dummy_sb + l4_ged_dummy_sb + l5_ged_dummy_sb + l6_ged_dummy_sb + l7_ged_dummy_sb + l8_ged_dummy_sb + l9_ged_dummy_sb + l10_ged_dummy_sb + l11_ged_dummy_sb + l12_ged_dummy_sb + mean_ged_dummy_sb + ln_fvp_population200 + ssp2_edu_sec_15_24_prop + ssp2_urban_share_iiasa + fvp_lngdpcap_nonoilrent + fvp_lngdpcap_oilrent + fvp_grgdpcap_oilrent + fvp_grgdpcap_nonoilrent + ln_fvp_timeindep + ln_fvp_timesincepreindepwar + ln_fvp_timesinceregimechange + fvp_demo + fvp_semi + fvp_prop_excluded",
    "modtype": "SMLogit",
    "name": "cm_transforms_sb"
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

nsim = 4

train_start = 205
train_end = 464
sim_start = 465
sim_end = 502

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
