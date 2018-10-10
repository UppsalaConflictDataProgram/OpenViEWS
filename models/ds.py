import os
import json
import times as t
import utils
from config import nsim

def assert_list_values_all_equal(l):
    assert len(set(l))==1, "this list has non-equal elements"

def set_runs_transforms(runs):
    for run in runs:
        run = set_run_transforms(run)
    return runs

def assign_models_to_runs(runs, models):
    for run in runs:
        #print("#"*80)
        #print(run['name'])
        for model in models:
            if model['name'].startswith(run['name']):
                #print("  ", model['name'])
                run['models'].append(model)
    return runs

def set_nsim_runs(runs):
    for run in runs:
        run['nsim'] = nsim
    return runs

def get_ds_baseruns(models):
    runs_bases = []
    for model in models:
        runs_bases.append(model['name_base'])
    runs_bases = list(set(runs_bases))
    return runs_bases

def assert_equal_commons(models):
    ts = []
    te = []
    ss = []
    se = []
    loas = []
    for model in models:
        ts.append(model['train_start'])
        te.append(model['train_end'])
        ss.append(model['sim_start'])
        se.append(model['sim_start'])
        loas.append(model['loa'])

    assert len(set(ts))==1
    assert len(set(te))==1
    assert len(set(ss))==1
    assert len(set(se))==1
    assert len(set(loas))==1

def copy_model_attrs_to_runs(runs):
    for run in runs:
        assert_equal_commons(run['models'])
        for model in run['models']:
            run['train_start'] = model['train_start']
            run['train_end'] = model['train_end']
            run['sim_start'] = model['sim_start']
            run['sim_end'] = model['sim_end']
            run['groupvar'] = model['groupvar']
            run['timevar'] = model['timevar']
            run['runtype'] = model['runtype']
            run['period'] = model['period']
            run['loa'] = model['loa']
    return runs

def set_run_transforms(run):
    ts = []
    spatial = []
    transforms = []

    for model in run['models']:
        model['transforms_nested'] = {
            'ts' : [],
            'spatial' : [],
            'transform' : []
        }
        for transform in model['transforms']:
            model['transforms_nested'][transform['type']].append(transform)
        #print(json.dumps(model['transforms_nested'], indent=2))


    for model in run['models']:
        ts.append(model['transforms_nested']['ts'])
        spatial.append(model['transforms_nested']['spatial'])
        transforms.append(model['transforms_nested']['transform'])
    ts = utils.flatten_list(ts)
    spatial = utils.flatten_list(spatial)
    transforms = utils.flatten_list(transforms)
    ts = utils.drop_duplicates_from_list_of_dicts(ts)
    spatial = utils.drop_duplicates_from_list_of_dicts(spatial)
    transforms = utils.drop_duplicates_from_list_of_dicts(transforms)

    for transform in ts+spatial+transforms:
        del transform['type']

    run['transforms'] = {
        'ts' : ts,
        'spatial' : spatial,
        'transforms' : transforms
    }
    return run

def model_to_paramfile(model):
    model_paramfile = {
        'name' : model['name'],
        'formula' : model['formula']
    }

    binary_outcomes = ["ged_dummy_sb", "ged_dummy_ns", "ged_dummy_os",
                        "acled_dummy_pr"]
    if model['lhs'] in binary_outcomes:
        model_paramfile['modtype'] = 'SMLogit'
    else:
        model_paramfile['modtype'] = 'SMIdentity'

    return model_paramfile

def write_paramfile(run, dir_source, dir_output):
    path_source = dir_source + "paramfile_ds.py"
    with open(path_source, 'r') as f:
        source = f.read()
    paramfile = source

    # set times
    vals = ["train_start", "train_end",
            "sim_start", "sim_end", "timevar", "groupvar"]
    for val in vals:
        key = "$"+val
        paramfile = paramfile.replace(key, str(run[val]))

    paramfile = paramfile.replace("$runid", run['name'])

    for transformtype in ["ts", "spatial", "transforms"]:
        key="$"+transformtype
        paramfile = paramfile.replace(key,
            json.dumps(run['transforms'][transformtype],
                       indent=2,
                       sort_keys=True))

    models_paramfile = []
    for model in run['models']:
        models_paramfile.append(model_to_paramfile(model))

    paramfile = paramfile.replace("$models", json.dumps(models_paramfile,
                                                        indent=2,
                                                        sort_keys=True))

    outcomes = []
    for model in run['models']:
        outcomes.append(model['lhs'])

    paramfile = paramfile.replace("$vars_plots_outcomes", json.dumps(outcomes))
    paramfile = paramfile.replace("$nsim", str(run['nsim']))

    path_output = dir_output + run['name'] + ".py"
    with open(path_output, 'w') as f:
        f.write(paramfile)
    print("Wrote", path_output)

times = t.times_nested

dir_source = "./source/"
dir_paramfiles = "./output/ds/paramfiles/"
dir_runfiles = "./output/ds/runfiles/"
dir_publishes = "./output/ds/publishes/"

loas = ["pgm", "cm"]
runtypes = ["eval", "fcast"]
periods = ["calib", "test"]

paths_models = utils.get_paths_from_dir(dir = "./output/models/", extension=".json")

# load all models
models = []
for path in paths_models:
    with open(path, 'r') as f:
        model = json.load(f)
        models.append(model)

# base ds runs, without time
runs_bases = get_ds_baseruns(models)

# make the runs with a name
runs = []
for run_base in runs_bases:
    for runtype in runtypes:
        for period in periods:
            name = "_".join([run_base, runtype, period])
            run = {
                'name' : name,
                'models' : []
            }
            runs.append(run)

# assign each model to a run
runs = assign_models_to_runs(runs, models)
runs = copy_model_attrs_to_runs(runs)
runs = set_runs_transforms(runs)
runs = set_nsim_runs(runs)

for run in runs:
    write_paramfile(run, dir_source, dir_paramfiles)


# Make the runfiles
paths_paramfiles = utils.get_paths_from_dir(dir_paramfiles, extension=".py")
for path in paths_paramfiles:
    with open("source/runfile_ds_uppmax.sh", 'r') as f:
        source=f.read()

    run_id = path.split("/")[-1]
    run_id = run_id.split(".")[0]
    source = source.replace("$run_id", run_id)

    fname_output=run_id+".sh"
    path_output = "./output/ds/runfiles/"+fname_output
    with open(path_output,'w') as f:
        f.write(source)
    print("Wrote", path_output)


# make empty tables
tables = []
for loa in loas:
    for runtype in runtypes:
        for period in periods:
            table_name = "_".join(["ds", loa, runtype, period])
            table = {
                'name' : table_name,
                'loa' : loa,
                'runtype' : runtype,
                'period' : period,
                'members' : [],
                'members_lhs' : []
            }
            tables.append(table)

# assign run to table
for table in tables:
    for run in runs:
        name_table_run = "_".join([run['loa'], run['runtype'], run['period']])
        name_table = "_".join([table['loa'], table['runtype'], table['period']])
        if name_table_run == name_table:
            table['members'].append(run['name'])

            lhss = []
            for model in run['models']:
                lhs = model['lhs']
                table['members_lhs'].append(lhs)
    table['members_lhs'] = sorted(list(set(table['members_lhs'])))

    #print(json.dumps(table, indent=2))

# make the publishfile
for table in tables:
    command =  "# This file was generated by models/ds.py \n"
    command += "python publish.py \\\n"
    command += "    --uname VIEWSADMIN \\\n"

    command += "    --dir_scratch /storage/runs/current/ds/results \\\n"
    command += "    --schema landed \\\n"
    command += "    --table " + table['name'] + "\\\n"

    for lhs in table['members_lhs']:
        print(lhs)
        command += "    --outcome " + lhs + "_mean" + "\\\n"

    command += "    --stripname ged_dummy_ \\\n"
    command += "    --stripname acled_dummy_ \\\n"
    command += "    --stripname _mean \\\n"

    for run_id in table['members']:
        command += "    --run_id " + run_id + "\\\n"

    command += "    --push \\\n"
    command += "    --printswitch \\\n"

    #print(command)

    path_output = dir_publishes + table['name'] + ".sh"
    with open(path_output, 'w') as f:
        f.write(command)
    print("Wrote", path_output)


