'''
Recursively loop over *featimp.csv and create feature importance plots
'''

#TODO VIEWSADMIN 2018-07-18:
# Make runid an argument with argparse
# Save plots in /storage/runs/current/plots/featimp/
# Create dirs if they don't exist
# Read the schema and table to plot from argparse
# Read from the database with dbutils.db_to_df()
# See Views/plot/maps/plot_cols.py for example



# RBJ 16-07-2018
import argparse
import os
import json
from os import listdir
from os.path import isfile, join
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

# add runid argument via argparse
parser = argparse.ArgumentParser()
parser.add_argument("--run_id", type=str,
                    help="Run ID")
args = parser.parse_args()
run_id = args.run_id

# move wd
path = "/storage/runs/current/osa/results/"
os.chdir(path)

# directory walk getting the paths to csv files
filelist = []
for (dirpath, dirnames, filenames) in os.walk(path):
    for files in filenames:
        directory = (dirpath + "/" + files)
        filelist.append(directory)

csvfiles = []
for file in filelist:
    #@TODO: "is True" isn't necessary, endswith returns a bool by default
    if file.endswith("featimp.csv"):
        csvfiles.append(file)

levels = ["cm", "pgm"]
periods = ["eval_calib", "eval_test", "fcast_calib", "fcast_test"]

runs = []
# Create 8 empty runs
for level in levels:
    for period in periods:
        run = {
            'level' : level,
            'period' : period,
            'jobs' : []
        }
        runs.append(run)

# Distribute the csv files between the runs
for run in runs:
    level = run['level']
    period = run['period']
    dir_output = "/storage/runs/current/plot/featimps/{level}_{period}/".format(level=level, period=period)
    run['dir_output'] = dir_output

    for path in csvfiles:
        name = path.replace('_featimp.csv', '')
        name = name.split("/")[-1]

        level_period = path.split("/")[6]


        if (level in level_period) and (period in level_period):
            job = {
            'name' : name,
            'path_input' : path
            }
            run['jobs'].append(job.copy())

for run in runs:
    for job in run['jobs']:
        path_output = run['dir_output'] + job['name'] + "_featimp.pdf"
        job['path_output'] = path_output

def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)

# plot function
def plot_featimp(path_input, path_output, modelname):
    '''transposes, sorts data and plots featimp figure.'''
    df = pd.read_csv(path_input)
    df = df.transpose()

    # correct first row after transposing, reset index and give colnames
    df = df.iloc[1:]
    df.reset_index(inplace=True)
    df.columns = ['variable', 'value']
    df.sort_values('value', ascending=False, inplace=True)

    # initialize and plot figure
    f, ax = plt.subplots(figsize=(14, 10))
    fimps = sns.barplot(x="value", y="variable", data=df, palette="RdYlBu")
    sns.despine(left=True, bottom=True)
    ax.set(xlim=(0, (max(df.value) + 0.15*max(df.value))), ylabel="",
           xlabel="")

    plt.title('Feature importance \nModelname: {} \nRun: {}'.format(modelname, run_id),
              loc='left')
    for i, v in enumerate(df.value):
        # Make the string first then pass it to plt.text()
        plt.text(v, i + .1, " " + str(round(v, 3)), va='center', size=10)

    # get and save to file
    fig_featp = fimps.get_figure()
    fig_featp.savefig(path_output, bbox_inches='tight', pad_inches=1)
    print("Wrote", path_output)

    plt.close(f)

def plot_featimp_worker(job):

    path_input = job['path_input']
    path_output = job['path_output']
    modelname = job['name']

    plot_featimp(path_input, path_output, modelname)

for run in runs:
    create_dirs([run['dir_output']])
    for job in run['jobs']:
        plot_featimp_worker(job)
