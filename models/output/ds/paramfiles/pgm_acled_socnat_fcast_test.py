import argparse
import json

run_id = "pgm_acled_socnat_fcast_test"
timevar = "month_id"
groupvar = "pg_id"

ts = []

spatial = []

transforms = [
  {
    "f": "log_natural",
    "name": "ln_dist_diamsec",
    "var": "dist_diamsec_s_wgs"
  },
  {
    "f": "log_natural",
    "name": "ln_ttime",
    "var": "ttime_mean"
  },
  {
    "f": "log_natural",
    "name": "ln_dist_petroleum",
    "var": "dist_petroleum_s_wgs"
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
    "name": "ln_pop",
    "var": "pop_li_gpw_sum"
  }
]

models = [
  {
    "formula": "ged_dummy_ns ~ ln_bdist3 + ln_ttime + ln_capdist + ln_pop + gcp_li_mer + imr_mean + excluded_dummy_li + ln_dist_diamsec + ln_dist_petroleum + agri_ih_li + barren_ih_li + forest_ih_li + mountains_mean + savanna_ih_li + shrub_ih_li + pasture_ih_li + urban_ih_li",
    "modtype": "SMLogit",
    "name": "pgm_acled_socnat_fcast_test_ns"
  },
  {
    "formula": "ged_dummy_os ~ ln_bdist3 + ln_ttime + ln_capdist + ln_pop + gcp_li_mer + imr_mean + excluded_dummy_li + ln_dist_diamsec + ln_dist_petroleum + agri_ih_li + barren_ih_li + forest_ih_li + mountains_mean + savanna_ih_li + shrub_ih_li + pasture_ih_li + urban_ih_li",
    "modtype": "SMLogit",
    "name": "pgm_acled_socnat_fcast_test_os"
  },
  {
    "formula": "acled_dummy_pr ~ ln_bdist3 + ln_ttime + ln_capdist + ln_pop + gcp_li_mer + imr_mean + excluded_dummy_li + ln_dist_diamsec + ln_dist_petroleum + agri_ih_li + barren_ih_li + forest_ih_li + mountains_mean + savanna_ih_li + shrub_ih_li + pasture_ih_li + urban_ih_li",
    "modtype": "SMLogit",
    "name": "pgm_acled_socnat_fcast_test_pr"
  },
  {
    "formula": "ged_dummy_sb ~ ln_bdist3 + ln_ttime + ln_capdist + ln_pop + gcp_li_mer + imr_mean + excluded_dummy_li + ln_dist_diamsec + ln_dist_petroleum + agri_ih_li + barren_ih_li + forest_ih_li + mountains_mean + savanna_ih_li + shrub_ih_li + pasture_ih_li + urban_ih_li",
    "modtype": "SMLogit",
    "name": "pgm_acled_socnat_fcast_test_sb"
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
