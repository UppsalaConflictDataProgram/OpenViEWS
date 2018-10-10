import json

run = {
    'name' : name,
    'jobs' : jobs,
    'table_h' : "landed.collected_pgm_fcast_test",
    'table_l' : "landed.collected_cm_fcast_test",
    'groupvar_h' : "pg_id",
    'groupvar_l' : "country_id",
    'timevar' : "month_id"
}