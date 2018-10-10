import json
import os
from loa import loas


def subset_dict(d, keys):
    """Get a subset of key-value pairs from a dict"""
    return dict((k, d[k]) for k in keys if k in d)


def rename_dict_keys(d, renames):
    for rename in renames:
        d[rename['new']] = d.pop(rename['old'])
    return d


def flatten_list(l):
    flat_list = [item for sublist in l for item in sublist]
    return flat_list


def drop_duplicates_from_list_of_dicts(l):
    l = [dict(t) for t in set([tuple(d.items()) for d in l])]
    return l


def add_outcome_extension_to_name(model):
    outcome_extension = model['lhs'].strip("ged_dummy")
    outcome_extension = outcome_extension.strip("acled_dummy")
    model['name'] = model['name'] + "_" + outcome_extension
    model['outcome_extension'] = outcome_extension
    return model


def add_time_extension_to_name(model, runtype, period):
    extension_time = "_".join(["", runtype, period])
    model['name'] = model['name'] + extension_time
    return model


def add_times_to_model(model, runtype, period, times):
    def assign_train_start(model):
        if "acled" in model['name']:
            model['train_start'] = times['train_start_acled']
        else:
            model['train_start'] = times['train_start_canon']
        return model

    model = assign_train_start(model)
    model['train_end'] = times[runtype][period]['train_end']
    model['sim_start'] = times[runtype][period]['sim_start']
    model['sim_end'] = times[runtype][period]['sim_end']
    model['runtype'] = runtype
    model['period'] = period
    return model


def add_model_formula(model):
    formula = model['lhs']
    formula += " ~ "
    formula += " + ".join(model['rhs'])
    model['formula'] = formula
    return model


def add_transforms_to_model(model, transforms):
    model_transforms = []
    for var in model['rhs']:
        if var in transforms.keys():
            # we found a transform matching the rhs-var
            model_transforms.append(transforms[var])

    # some transforms depend on other transforms, add these deps too
    # do it 3 times to get all three possible levels of dependency
    for i in range(3):
        for transform in model_transforms:
            if transform['var'] in transforms.keys():
                model_transforms.append(transforms[transform['var']])

    model_transforms = drop_duplicates_from_list_of_dicts(model_transforms)
    model['transforms'] = model_transforms

    return model


def print_model(model):
    print("#"*80)
    print("name: ", model['name'])
    print("loa:  ", model['loa'])
    print("lhs:  ", model['lhs'])
    print("rhs:  ")
    for v in model['rhs']:
        print("      ", v)
    print("formula: ")
    print(model['formula'])


def store_model(model, dir_output):
    fname_output = model['name'] + ".json"
    path_output = os.path.join(dir_output, fname_output)
    with open(path_output, 'w') as f:
        json.dump(model, f, indent=4)
    print("Wrote", path_output)


def add_timevar_groupvar(model):
    model['groupvar'] = loas[model['loa']]['groupvar']
    model['timevar'] = loas[model['loa']]['timevar']
    return model


def make_models(name, loa, vars_lhs, vars_rhs_specifics, rhs_common, stage,
                transforms):
    """ Returns a list of model dictionaries, one for each outcome"""
    models = []
    for lhs, rhs_specifics in zip(vars_lhs, vars_rhs_specifics):
        model = {
            'name': name,
            'name_base': name,
            'loa': loa,
            'lhs': lhs,
            'rhs': rhs_specifics + rhs_common,
            'stage': stage
        }

        model = add_model_formula(model)
        model = add_transforms_to_model(model, transforms)
        model = add_timevar_groupvar(model)
        models.append(model)

    return models


def demux_times(model, runtypes, periods, times):
    models = []
    for runtype in runtypes:
        for period in periods:
            model_time = add_time_extension_to_name(
                model.copy(), runtype, period)
            model_time = add_outcome_extension_to_name(model_time)
            model_time = add_times_to_model(model_time, runtype, period, times)
            models.append(model_time)
    return models


def get_paths_from_dir(dir, extension=None):
    paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            paths.append(path)
    if extension:
        #print("Selecting paths containing", extension, "from", dir)
        paths = [path for path in paths if extension in path.split("/")[-1]]
    paths = sorted(paths)
    return paths


def fix_means_period_osa(model):

    runperiod = f"_{model['runtype']}_{model['period']}"
    features = model['features']

    vars_mean = ['mean_ged_dummy_sb',
                 'mean_ged_dummy_ns',
                 'mean_ged_dummy_os',
                 'mean_acled_dummy_pr']

    for var in vars_mean:
        if var in features:
            var_replacement = var + runperiod
            features.remove(var)
            features.append(var_replacement)

    return model

