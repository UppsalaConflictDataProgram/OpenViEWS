# This file defines all time periods for dynasim, each paramfile imports
# it's time limits from here to make monthly updates smoother
# There are 6 periods
# eval
#   penultimate
#   last
#   next
# fcast
#   penultimate
#   last
#   next
# Where eval done on the final yearly updated UCDP data and fcast is
# aligned so fcast_next starts on the first month for which we have no 
# data. 

# last month of final UCDP data, released yearly
last_month_final = 456
# last month of rollingly released data from UCDP, updated monthly
last_month_rolling = 456


# First month with ACLED data
train_start_acled = 205
# First month with GED data
train_start_canon = 121

train_end_eval_calib  = last_month_final - 72
train_end_eval_test = last_month_final - 36
sim_start_eval_calib  = train_end_eval_calib  + 1
sim_start_eval_test = train_end_eval_test + 1
sim_end_eval_calib = sim_start_eval_calib + 35
sim_end_eval_test = sim_start_eval_test + 35

train_end_fcast_calib = last_month_rolling - 36
train_end_fcast_test = last_month_rolling
sim_start_fcast_calib = train_end_fcast_calib + 1
sim_start_fcast_test = train_end_fcast_test + 1
sim_end_fcast_calib = sim_start_fcast_calib + 35
sim_end_fcast_test = sim_start_fcast_test + 35

times = {
    'train_start_acled'     : str(train_start_acled),
    'train_start_canon'     : str(train_start_canon),
    'train_end_eval_calib'  : str(train_end_eval_calib),
    'train_end_eval_test'   : str(train_end_eval_test),
    'sim_start_eval_calib'  : str(sim_start_eval_calib),
    'sim_start_eval_test'   : str(sim_start_eval_test),
    'sim_end_eval_calib'    : str(sim_end_eval_calib),
    'sim_end_eval_test'     : str(sim_end_eval_test),
    'train_end_fcast_calib' : str(train_end_fcast_calib),
    'train_end_fcast_test'  : str(train_end_fcast_test),
    'sim_start_fcast_calib' : str(sim_start_fcast_calib),
    'sim_start_fcast_test'  : str(sim_start_fcast_test),
    'sim_end_fcast_calib'  : str(sim_end_fcast_calib),
    'sim_end_fcast_test'    : str(sim_end_fcast_test),
}

