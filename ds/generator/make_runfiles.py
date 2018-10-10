import os

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

paths_paramfiles = get_paths_from_dir(dir = "./output/paramfiles", extension=".py")

for path in paths_paramfiles:
    with open("source/runfiles/runfile_base_uppmax.sh", 'r') as f:
        source=f.read()

    run_id = path.split("/")[-1]
    run_id = run_id.split(".")[0]
    source = source.replace("$run_id", run_id)

    fname_output=run_id+".sh"
    path_output = "output/runfiles/"+fname_output
    with open(path_output,'w') as f:
        f.write(source)
    print("Wrote", path_output)