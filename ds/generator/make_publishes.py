import os
import json

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

# find all the generated runfiles
paths_runfiles = get_paths_from_dir(dir = "./output/runfiles/", extension=".sh")

# using the amazing naming convention, figure out which 
# level and time period this run is for
runs = []
for path in paths_runfiles:
    fname = path.split("/")[-1]
    fname = fname.split(".")[0]
    level = fname.split("_")[0]
    varset = fname.split("_")[1]
    runtype = fname.split("_")[-2]
    time = fname.split("_")[-1]
    run = {
        'name' : fname,
        'level' : level,
        'varset' : varset,
        'runtype' : runtype,
        'time' : time
    }
    runs.append(run)

levels = ["cm", "pgm"]
runtypes = ["eval", "fcast"]
periods = ["calib", "test"]

# construct 8 tables of the combinations of levels, runtypes and periods
tables = []
for level in levels:
    for runtype in runtypes:
        for period in periods:
            table = {
                'name' : "_".join([level, runtype, period]),
                'members' : []
            }
            tables.append(table)

# match these tables to runs that we found runfiles for
for table in tables:
    for run in runs:
        run_table_name = "_".join([run['level'], run['runtype'], run['time']])
        if run_table_name == table['name']:
            table['members'].append(run)
    table['name'] = "ds_" + table['name']

for table in tables:
    command =  "# This file was generated by ds/maker/make_publishes.py \n"
    command += "python publish.py \\\n"
    command += "    --uname VIEWSADMIN \\\n"

    command += "    --dir_scratch /storage/runs/current/ds/results \\\n"
    command += "    --schema landed \\\n"
    command += "    --table " + table['name'] + "\\\n"

    command += "    --outcome ged_dummy_sb_mean \\\n"
    command += "    --outcome ged_dummy_ns_mean \\\n"
    command += "    --outcome ged_dummy_os_mean \\\n"
    command += "    --outcome acled_dummy_pr_mean \\\n"

    command += "    --stripname ged_dummy_ \\\n"
    command += "    --stripname acled_dummy_ \\\n"
    command += "    --stripname _mean \\\n"

    for run in table['members']:
        command += "    --run_id " + run['name'] + "\\\n"

    command += "    --push \\\n"
    command += "    --printswitch \\\n"

    #print(command)

    path_output = "output/publishes/" + table['name'] + ".sh"
    with open(path_output, 'w') as f:
        f.write(command)
    print("Wrote", path_output)

