tables_to_plot = [
    "ensemble_cm_eval_test",
    "ensemble_cm_fcast_test",
    "ensemble_pgm_eval_test",
    "ensemble_pgm_fcast_test",
    "agg_cm_eval_calib",
    "agg_cm_eval_test",
    "agg_cm_fcast_calib",
    "agg_cm_fcast_test",
    "ds_cm_eval_calib",
    "ds_cm_eval_test",
    "ds_cm_fcast_calib",
    "ds_cm_fcast_test",
    "ds_pgm_eval_calib",
    "ds_pgm_eval_test",
    "ds_pgm_fcast_calib",
    "ds_pgm_fcast_test",
    "osa_cm_eval_calib",
    "osa_cm_eval_test",
    "osa_cm_fcast_calib",
    "osa_cm_fcast_test",
    "osa_pgm_eval_calib",
    "osa_pgm_eval_test",
    "osa_pgm_fcast_calib",
    "osa_pgm_fcast_test"]

tables_cm = [table for table in tables_to_plot if "_cm" in table]
tables_pgm = [table for table in tables_to_plot if "_pgm" in table]

def make_runfile_maps(tables, groupvar):
    
    with open("template_runfile_map_header.sh", 'r') as f:
        header = f.read()

    with open("template_runfile_map_body.sh", 'r') as f:
        body = f.read()

    waitline = "\n wait \n"

    runfile = header

    i = 1
    for table in tables:
        this_body = body.replace("TABLENAME", table)
        this_body = this_body.replace("GROUPVAR", groupvar)
        if groupvar=="pg_id":
            this_body = this_body.replace("TABLE_ACTUAL", "flight_pgm")
        elif groupvar=="country_id":
            this_body = this_body.replace("TABLE_ACTUAL", "flight_cm")
        runfile = runfile + this_body

        if i%4==0:
            runfile = runfile + waitline
        i+=1

    return runfile

def make_runfile_descriptives(tables, groupvar):
    with open("template_runfile_descriptive_header.sh", 'r') as f:
        header = f.read()

    if groupvar == "pg_id":
        path_body = "template_runfiles_descriptive_body_pgm.sh"
    elif groupvar == "country_id":
        path_body = "template_runfiles_descriptive_body_cm.sh"

    with open(path_body, 'r') as f:
        body = f.read()

    waitline = "\n wait \n"

    runfile = header

    i = 1
    for table in tables:
        this_body = body.replace("TABLENAME", table)
        this_body = this_body.replace("GROUPVAR", groupvar)
        runfile = runfile + this_body

        if i%4==0:
            runfile = runfile + waitline
        i+=1

    return runfile


runfiles_maps_cm = make_runfile_maps(tables_cm, "country_id")
runfiles_maps_pgm = make_runfile_maps(tables_pgm, "pg_id")
runfiles_desc_cm = make_runfile_descriptives(tables_cm, "country_id")
runfiles_desc_pgm = make_runfile_descriptives(tables_pgm, "pg_id")



with open("plot_maps_cm.sh", 'w') as f:
    f.write(runfiles_maps_cm)
with open("plot_maps_pgm.sh", 'w') as f:
    f.write(runfiles_maps_pgm)
with open("plot_desc_cm.sh", 'w') as f:
    f.write(runfiles_desc_cm)
with open("plot_desc_pgm.sh", 'w') as f:
    f.write(runfiles_desc_pgm)


