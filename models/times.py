# This file defines all time periods for ViEWS, each paramfile imports
# it's time limits from here to make monthly updates smoother
# There are 4 periods
# eval
#   calib
#   test
# fcast
#   calib
#   test
# Where eval done on the final yearly updated UCDP data and fcast is
# aligned so fcast_test starts on the first month for which we have no
# data.
# The training

# last month of final UCDP data, released yearly
last_month_final = 456 # 2017-12
# last month of rollingly released data from UCDP, updated monthly
last_month_rolling = 464 #2018-8


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
sim_end_fcast_test = sim_start_fcast_test + 37

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
    'sim_end_fcast_calib'   : str(sim_end_fcast_calib),
    'sim_end_fcast_test'    : str(sim_end_fcast_test),
}

times_nested = {
    'eval' : {
        'calib' : {
            'train_end' : train_end_eval_calib,
            'sim_start' : sim_start_eval_calib,
            'sim_end' : sim_end_eval_calib
        },
        'test' : {
            'train_end' : train_end_eval_test,
            'sim_start' : sim_start_eval_test,
            'sim_end' : sim_end_eval_test
        }
    },
    'fcast' : {
        'calib' : {
            'train_end' : train_end_fcast_calib,
            'sim_start' : sim_start_fcast_calib,
            'sim_end' : sim_end_fcast_calib
        },
        'test' : {
            'train_end' : train_end_fcast_test,
            'sim_start' : sim_start_fcast_test,
            'sim_end' : sim_end_fcast_test
        }
    },
    'train_start_acled' : train_start_acled,
    'train_start_canon' : train_start_canon
}

















