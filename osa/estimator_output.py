from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import os
import sys
sys.path.append("..")
import views_utils.dbutils as dbutils
import pickle
import json
import re

from osa.wrapper_sm import SMLogit


models = []
dir_osa_results = os.path.expandvars("$SNIC_TMP/osa/pickles/")
for root, dirs, files in os.walk(dir_osa_results):
    for file in files:
        path=os.path.join(root, file)
        if path.endswith(".pickle"):
            run= path.split("/")[-3]
            model = path.split("/")[-2]
            stepname = path.split("/")[-1]
            step = re.findall(string=stepname, pattern="(\d+)")[0]


            this_model = {
                'path_pickle' : path,
                'run' : run,
                'modelname' : model,
                'name' : stepname.split(".pickle")[0],
                'step' : step
            }
            models.append(this_model)



for model in models:
    with open(model['path_pickle'], 'rb') as f:
        this_pickle = pickle.load(f)
    print("read", model['path_pickle'])

    estimator = this_pickle['estimator']
    if isinstance(estimator, Pipeline):
        this_rf_fi = this_pickle['estimator'].named_steps.rf.feature_importances_
        cols_features = this_pickle['features']
        df_feature_importances = pd.DataFrame(this_rf_fi.reshape(-1, len(this_rf_fi)),
                                              columns=cols_features)
        model['feature_importances'] = df_feature_importances

        model['estimator_type'] = "rf"

        print("rf")

        path_csv = model['path_pickle'].replace(".pickle", "_featimp.csv")
        model['feature_importances'].to_csv(path_csv)
        print("wrote", path_csv)

    elif isinstance(estimator, SMLogit):
        features = this_pickle['features'] + ["Intercept"]
        outcome = this_pickle['outcome']
        estimator.model.model.data.xnames = features
        estimator.model.model.data.ynames = outcome
        model['summary_csv'] = estimator.model.summary().as_csv()

        summary_tex = estimator.model.summary().as_latex()
        summary_tex = summary_tex.replace("\_", "_")
        summary_tex = summary_tex.replace("_", "\_")
        model['summary_tex'] = summary_tex

        model['estimator_type'] = "logit"

        print("logit")

        path_csv = model['path_pickle'].replace(".pickle", "_regtab.csv")
        path_tex = model['path_pickle'].replace(".pickle", "_regtab.tex")

        with open(path_csv, 'w') as f:
            f.write(model['summary_csv'])
        print("wrote", path_csv)
        with open(path_tex, 'w') as f:
            f.write(model['summary_tex'])
        print("wrote", path_tex)


    else:
        print(model)


