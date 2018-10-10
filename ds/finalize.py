import pandas as pd

import argparse

from utils import (
    split,
    load_params,
    get_paths_sims,
    create_dirs,
    get_model_vars,
    add_varsets_to_modeljobs,
    get_paths_from_dir,
    get_predictions_training
    )

def make_csv_aggregated(dir_agg, dir_output):
    print("Making aggregated.csv")
    path_agg = dir_agg + "aggregated.hdf5"
    df_agg = pd.read_hdf(path_agg)
    print("read", path_agg)
    path_results = dir_output + "aggregated.csv"
    df_agg.to_csv(path_results)
    print("wrote", path_results)

def make_csv_data(dir_data, dir_output):
    paths_data = get_paths_from_dir(dir_data)
    for path in paths_data:
        df = pd.read_hdf(path)
        print("read", path)
        print("read", path)
        filename = path.split("/")[0]
        filename_noext = filename.split(".hdf5")[0]

        filename_output = filename_noext + "_data.csv"
        path_output = dir_output + filename_output
        df.to_csv(path_output)
        print("wrote", path_output)
def make_csv_replicate(dir_data, dir_train, dir_sim, dir_output):
    paths_imputed = get_paths_from_dir(dir_data)
    names_imputed = []
    for p in paths_imputed:
        name = p.split("/")[-1].split(".hdf5")[0]
        names_imputed.append(name)

    print("Found", str(len(names_imputed)), "imputed datasets")

    for name in names_imputed:
        print("preping replicate.csv for", name)
        path_train = dir_train + name + "/workdata.hdf5"
        df_train = pd.read_hdf(path_train)
        print("read", path_train)
        cols_train = list(df_train.columns)
        path_sim = dir_sim + name + "/workdata.hdf5"
        df_sim = pd.read_hdf(path_sim)
        print("read", path_sim)
        df_sim = df_sim[cols_train]
        df = df_train.append(df_sim)
        path_output = dir_output + name + "_replicate.csv"
        df.to_csv(path_output)
        path_output = dir_output + name + "_replicate.hdf5"
        df.to_hdf(path_output, key='data')
        print("wrote", path_output)

def collect_predictions_train(dir_train, dir_output):
    
    def get_names_datasets(dir_train):
        paths = get_paths_from_dir(dir_train, extension=".hdf5")
        paths_  = [path for path in paths if "workdata.hdf5" in path]
        paths = [path.split("/")[-2] for path in paths]
        names = list(set(paths))
        return names

    def get_paths_models(dir_train_dataset):
        paths = get_paths_from_dir(dir_train_dataset, ".hdf5")
        paths = [path for path in paths if not "workdata.hdf5" in path]
        return paths

    names_datasets = get_names_datasets(dir_train)


    for dataset in names_datasets:
        print("Collecting training predictions for", dataset)
        dir_train_dataset = dir_train + dataset + "/"
        
        # Read the training data and keep only indices
        path_dataset = dir_train_dataset + "workdata.hdf5"
        df = pd.read_hdf(path_dataset)

        # rows with missingness won't have predictions
        df = df.dropna()
        print("read", path_dataset)
        df = df[[]]
        print(df)
        print(len(df))

        paths_models = get_paths_models(dir_train_dataset)
        for path in paths_models:
            name_model = path.split("/")[-1].split(".hdf5")[0]
            predictions = get_predictions_training(path)
            print(predictions.shape)
            df[name_model] = predictions

        path_output = dir_output + "predictions_train_" + dataset + ".hdf5"
        df.to_hdf(path_output, key='data')
        print("Wrote", path_output)

def main_final():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir_scratch", type=str,
        help="temp directory in which to save data")

    args = parser.parse_args()

    dir_scratch = args.dir_scratch

    path_params = dir_scratch + "params.json"

    dir_sim = dir_scratch + "sim/"
    dir_data = dir_scratch + "data/"
    dir_train = dir_scratch + "train/"
    dir_agg = dir_scratch + "aggregate/"
    dir_output = dir_scratch + "output/"

    params = load_params(path_params)


    make_csv_aggregated(dir_agg, dir_output)
    collect_predictions_train(dir_train, dir_output)
    #make_csv_replicate(dir_data, dir_train, dir_sim, dir_output)




if __name__ == "__main__":
    main_final()