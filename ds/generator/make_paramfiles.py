import os


from times import times

def get_paths_from_dir(dir, extension=None):
    paths = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root,file)
            paths.append(path)
    if extension:
        print("Selecting paths containing", extension, "from", dir)
        paths = [path for path in paths if extension in path.split("/")[-1]]
    paths = sorted(paths)
    return paths 

def cook_source(path, runtype, period, times):
    with open(path, 'r') as f:
        source_clean = f.read()

    fname_source = os.path.basename(path)
    fname_source = fname_source.split(".")[0]
    newname = "_".join([fname_source, runtype, period])
    #print(newname)

    source = source_clean

    runid_formated = "\"" + newname + "\""
    source = source.replace("$run_id", runid_formated)

    # train start varies between canon and acled models
    if "acled" in newname:
        key = "train_start_acled"
        source = source.replace("$train_start", times[key])
        #print(times[key])
    elif "canon" in newname:
        key = "train_start_canon"
        source = source.replace("$train_start", times[key])
        #print(times[key])

    timekey_stems = ["train_end", "sim_start", "sim_end"]
    for stem in timekey_stems:
        key = "_".join([stem, runtype, period])
        #print(key)
        to_replace = "$"+stem
        replace_with = times[key]
        source = source.replace(to_replace, replace_with)
        #print(key, times[key])

    path_output = "output/paramfiles/" + newname + ".py"
    #print(path_output)
    with open(path_output,'w') as f:
        f.write(source)
    print("Wrote", path_output)


paths_source = get_paths_from_dir(dir = "./source/", extension=".py")

runtypes = ["eval", "fcast"]

periods = ["calib", "test"]



for path in paths_source:
    for runtype in runtypes:
        for period in periods:
            cook_source(path, runtype, period, times)
