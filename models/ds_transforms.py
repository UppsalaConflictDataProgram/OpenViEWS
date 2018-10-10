
# the IDs of two runs that contain all the transforms
runs = [
    {
        'name_old' : "pgm_acled_meansocnathistcm_fcast_test",
        'name_new' : "pgm_transforms"
    },
    {
        'name_old' : "cm_acled_mndmgecohstnst_fcast_test",
        'name_new' : "cm_transforms"}
    ]


for run in runs:
    path_paramfile_old = "./output/ds/paramfiles/" + run['name_old'] + ".py"
    path_paramfile_new = "./output/ds/paramfiles/" + run['name_new'] + ".py"
    path_runfile_old =   "./output/ds/runfiles/" + run['name_old'] + ".sh"
    path_runfile_new =   "./output/ds/runfiles/" + run['name_new'] + ".sh"


    with open(path_paramfile_old, 'r') as f:
        paramfile = f.read()
    with open(path_runfile_old, 'r') as f:
        runfile = f.read()

    paramfile = paramfile.replace(run['name_old'], run['name_new'])
    paramfile = paramfile.replace("nsim = 1000", "nsim = 4")

    runfile = runfile.replace(run['name_old'], run['name_new'])
    runfile = runfile.replace("48:00:00", "4:00:00")
    runfile = runfile.replace("echo 'finished'", "")

    dir_transforms = "/proj/snic2018-3-380/runs/current/ds/transforms/"
    dir_output = dir_transforms + run['name_new']

    mkdir_p = "mkdir -p " + dir_output

    rsync = "\nrsync -av $SNIC_TMP/ds/" + run['name_new'] + \
            "/data " + dir_output + "\n"

    runfile += mkdir_p
    runfile += rsync
    runfile += "echo 'finished'"
    with open(path_paramfile_new, 'w') as f:
        f.write(paramfile)
    print("Wrote", path_paramfile_new)
    with open(path_runfile_new, 'w') as f:
        f.write(runfile)
    print("Wrote", path_runfile_new)


