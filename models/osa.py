import sys
import json
import utils

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils

dir_output_paramfiles = "./output/osa/paramfiles/"
dir_output_runfiles =  "./output/osa/runfiles/"


uname    = "VIEWSADMIN"
prefix   = "postgresql"
db       = "views"
port     = "5432"
hostname = "VIEWSHOST"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)


dir_models = "./output/models/"
dir_source = "./source/"
path_source_paramfile = dir_source + "paramfile_osa.py"
path_source_runfile = dir_source + "runfile_osa_uppmax.sh"

share_zeros_full = 1
share_ones_full = 1
share_zeros_tenth = 0.1
steps = [1, 6, 12, 24, 36]
steps_fcast_test = [1, 6, 12, 24, 36, 38]

table_input_pgm = {
    'connectstring' : connectstring,
    'schema'    : 'launched',
    'table'     : 'transforms_pgm_imp_1',
    'timevar'   : 'month_id',
    'groupvar'  : 'pg_id'}

table_input_cm = {
    'connectstring' : connectstring,
    'schema'    : 'launched',
    'table'     : 'transforms_cm_imp_1',
    'timevar'   : 'month_id',
    'groupvar'  : 'country_id'}

# Each of the models is entered, once for each of these estimators
estimators = [
    {
        'name'          : 'logit_fullsample',
        'estimator'     : "SMLogit()",
        'share_zeros_keep'   : share_zeros_full,
        'share_ones_keep'    : share_ones_full,
    },
    {
        'name'          : 'logit_downsampled',
        'estimator'     : "SMLogit()",
        'share_zeros_keep'   : share_zeros_tenth,
        'share_ones_keep'    : share_ones_full,
    },
    {
        'name'          : 'rf_downsampled',
        'estimator'     : "pipe_rf_500",
        'share_zeros_keep'   : share_zeros_tenth,
        'share_ones_keep'    : share_ones_full,
    }
]

# load what we need from each model
paths_models = utils.get_paths_from_dir(dir_models, ".json")
wanted_kws = ["name", "name_base", "lhs", "rhs",
              "train_start", "train_end", "sim_start", "sim_end",
              "loa", "runtype", "period", "outcome_extension"]



renames = [
    {'old' : 'lhs',         'new' : 'outcome'},
    {'old' : 'rhs',         'new' : 'features'},
    {'old' : 'sim_start',   'new' : 'forecast_start'},
    {'old' : 'sim_end',     'new' : 'forecast_end'},
    ]

# subset the info we need from each of the raw models
models = []
for path in paths_models:
    with open (path, 'r') as f:
        model_raw = json.load(f)
    model = utils.subset_dict(model_raw, wanted_kws)
    model = utils.rename_dict_keys(model, renames)
    model = utils.fix_means_period_osa(model)
    model['steps'] = steps
    model['share_ones'] = share_ones_full
    model['estimator'] = "$estimator"

    if model['loa']=="cm":
        model['table'] = table_input_cm
    elif model['loa']=="pgm":
        model['table'] = table_input_pgm
    else:
        raise ValueError("unrecognized loa " + model['loa'])



    models.append(model)

loas = ["pgm", "cm"]
runtypes = ["eval", "fcast"]
periods = ["calib", "test"]

# assign models to runs members
runs = []
for model in models:
    name = "osa_" + model['name']
    run = {
        'name' : name,
        'models' : [model],
        }
    runs.append(run.copy())




# add run each model (a set of features) for each estimator
model_kws_keep = ["name", "estimator", "outcome", "features", "steps",
    "share_zeros_keep", "share_ones_keep", "train_start", "train_end",
    "forecast_start", "forecast_end", "table"]

for run in runs:
    models_w_estimators = []
    for model in run['models']:
        for estimator in estimators:
            this_model = model.copy()
            this_model['estimator'] = estimator['estimator']
            this_model['share_zeros_keep'] = estimator['share_zeros_keep']
            this_model['share_ones_keep'] = estimator['share_ones_keep']
            name = "_".join([model['name_base'], model['runtype'], model['period']])
            name += "_" + "_".join([estimator['name'], model['outcome_extension']])
            this_model['name'] = name
            this_model = utils.subset_dict(this_model, model_kws_keep)
            #print(this_model.keys())
            models_w_estimators.append(this_model)
    run['models'] = models_w_estimators

for run in runs:
    for model in run['models']:
        if "fcast_test" in model['name']:
            model['steps'] = steps_fcast_test



# Add dir_pickles to each model
basedir_pickles = "$SNIC_TMP/osa/pickles"
for run in runs:
    name_run = run['name']
    print(run['name'])
    for model in run['models']:
        name_model = model['name']
        dir_pickles = "/".join([basedir_pickles, name_run, name_model])
        pickledict = {'dir_pickles' : dir_pickles}
        model.update(pickledict)


for run in runs:
    with open(path_source_paramfile, 'r')  as f:
        source = f.read()
    source = source.replace("$models", json.dumps(run['models'],
                                                  indent=2,
                                                  sort_keys=True))

    # json can't write strings without quotes around them
    # we want to pass an actual object into the model, not a string
    # therefore we strip the quotes from each occurenct of  the estimator quoted
    for estimator in estimators:
        to_replace = "\"" + estimator['estimator'] + "\""
        replace_with = estimator['estimator']
        source = source.replace(to_replace, replace_with)

    # Set the output table
    table_output = "\"" + run['name'] + "\""
    source = source.replace("$output_table", table_output)

    # Write the paramfile
    path_output = dir_output_paramfiles + run['name'] + ".py"
    with open(path_output, 'w') as f:
        f.write(source)
    print("Wrote",path_output)

    # Write the runfile
    with open(path_source_runfile, 'r') as f:
        source = f.read()
    source = source.replace("$run_id", run['name'])
    path_output = dir_output_runfiles + run['name'] + ".sh"
    with open(path_output, 'w') as f:
        f.write(source)
    print("Wrote", path_output)
