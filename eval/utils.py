import sys
import pandas as pd
import numpy as np


from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
import matplotlib.pyplot as plt

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils

figsize = (12,12)
fontsize = 12

def get_predictions_eval_test():
    schema_pred = "landed"
    schema_actuals = "preflight"

    table_ds = "ds_pgm_eval_test"
    table_osa = "osa_pgm_eval_test"
    table_ebma = "ebma_pgm_eval_test"

    table_actuals = "flight_pgm"

    timevar = "month_id"
    groupvar = "pg_id"
    ids = [timevar, groupvar]

    outcomes = ["ged_dummy_sb", "ged_dummy_ns", "ged_dummy_os", "acled_dummy_pr"]

    df_ds = dbutils.db_to_df(connectstring, schema_pred, table_ds)
    df_osa = dbutils.db_to_df(connectstring, schema_pred, table_osa)
    df_ebma = dbutils.db_to_df(connectstring, schema_pred, table_ebma)
    df_ds.set_index(ids, inplace=True)
    df_osa.set_index(ids, inplace=True)
    df_ebma.set_index(ids, inplace=True)

    t_start_ds = df_ds.index.get_level_values(timevar).min()
    t_start_osa = df_osa.index.get_level_values(timevar).min()
    t_start_ebma = df_ebma.index.get_level_values(timevar).min()
    t_end_ds = df_ds.index.get_level_values(timevar).max()
    t_end_osa = df_osa.index.get_level_values(timevar).max()
    t_end_ebma = df_ebma.index.get_level_values(timevar).max()

    start_same = t_start_ds == t_start_osa == t_start_ebma
    end_same = t_end_ds == t_end_osa == t_end_ebma

    if not start_same and end_same:
        raise RuntimeError("The time indexes for ds, osa and ebma don't match")

    df = dbutils.db_to_df_limited(connectstring, 
        schema_actuals, table_actuals, columns=outcomes+ids, 
        timevar=timevar, groupvar=groupvar, tmin=t_start_ds, tmax=t_end_ds)

    df = df.merge(df_ds, left_index=True, right_index=True)
    df = df.merge(df_osa, left_index=True, right_index=True)
    df = df.merge(df_ebma, left_index=True, right_index=True)
    return df

def average_cols(df, name, cols):
    df[name] = np.average(df[cols], axis=1)
    return df

def calculate_prs(df, col_actual, cols_pred):
    prs = []
    y = df[col_actual]
    
    for col in cols_pred:
        score = df[col]
        precision, recall, _ = precision_recall_curve(y, score)
        average_precision = average_precision_score(y, score)
        this_auc = auc(precision, recall)
        
        pr = {
            'precision' : precision,
            'recall' : recall,
            'average_precision' : average_precision,
            'auc' : this_auc,
            'col' : col
        }
        prs.append(pr)
    return prs

def plot_performance(path, perflist, xvar, yvar, xlabel, ylabel):
    pass



def plot_prs(path, df, col_actual, cols_pred, title=None):
    #http://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html#sphx-glr-auto-examples-model-selection-plot-precision-recall-py
    
    prs = []
    y = df[col_actual]
    
    if title:
        title = "PR: " + title
    else:
        title = "PR"
    
    for col in cols_pred:
        score = df[col]
        precision, recall, _ = precision_recall_curve(y, score)
        average_precision = average_precision_score(y, score)
        
        pr = {
            'precision' : precision,
            'recall' : recall,
            'AP' : average_precision,
            'col' : col
        }
        prs.append(pr)

    plt.figure(figsize=figsize)

    for pr in prs:
        label = "{0} AP:{1:0.3f}".format(pr['col'], pr['AP'])
        plt.plot(pr['recall'], pr['precision'], label=label)
    plt.legend(fontsize=fontsize)
    plt.xlabel('Recall', fontsize=fontsize)
    plt.ylabel('Precision', fontsize=fontsize)
    
    plt.title(title)
    plt.savefig(path)
    print("wrote", path)

def plot_rocs(df, col_actual, cols_predictions, title=None):
    #http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py
    rocs = []
    y = df[col_actual]

    if title:
        title = "ROC: " + title
    else:
        title = "ROC"
    
    
    for col_pred in cols_predictions:
        scores = df[col_pred]
        fpr, tpr, thresholds = roc_curve(y, scores)
        this_auc = auc(fpr, tpr)
        roc = {
            'fpr' : fpr,
            'tpr' : tpr,
            'thresholds' : thresholds,
            'col' : col_pred.split("_")[0].upper(),
            'auc' : this_auc
        }
        rocs.append(roc)
    
    plt.figure(figsize=figsize)
    for roc in rocs:
        label = "{0} AP:{1:0.3f}".format(roc['col'], roc['auc'])
        plt.plot(roc['fpr'], roc['tpr'], label=label)
    plt.legend(fontsize=fontsize)
    plt.xlabel('False Positive Rate', fontsize=fontsize)
    plt.ylabel('True Positive Rate', fontsize=fontsize)

    plt.title(title, fontsize=fontsize)

    plt.show()
    
def plot_rocs_times(df, steps, col_actual, cols_predictions, title=None):
    #http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py
    rocs = []
    
    t_start = int(df.index.get_level_values(0).min())
    times = [step+t_start-1 for step in steps]
    
    linestyles = ['-', '--', '-.', ':']
    colors = ["C0", "C1", "C2", "C3"]


    if title:
        title = "ROC: " + title
    else:
        title = "ROC"
    
    for step, linestyle in zip(steps, linestyles):
        t = t_start + step - 1
        for col_pred, color in zip(cols_predictions, colors):
            y = df.loc[t][col_actual]
            scores = df.loc[t][col_pred]
            fpr, tpr, thresholds = roc_curve(y, scores)
            this_auc = auc(fpr, tpr)
            roc = {
                'fpr' : fpr,
                'tpr' : tpr,
                'thresholds' : thresholds,
                'col' : col_pred.split("_")[0].upper(),
                'auc' : this_auc,
                'linestyle' : linestyle,
                't' : step,
                'color' : color
            }
            rocs.append(roc)
    

    plt.figure(figsize=(16,16))
    for roc in rocs:
        label = "t:{0}, {1} AUC:{2:0.3f}".format(roc['t'], roc['col'], roc['auc'])
        plt.plot(roc['fpr'], roc['tpr'], label=label, linestyle=roc['linestyle'], color=roc['color'])
    plt.legend(fontsize=fontsize)
    plt.xlabel('False Positive Rate', fontsize=fontsize)
    plt.ylabel('True Positive Rate', fontsize=fontsize)

    plt.title(title, fontsize=fontsize)

    plt.show()
    
def plot_prs_times(df, steps, col_actual, cols_predictions, title=None):
    #http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py

    prs = []
    
    t_start = int(df.index.get_level_values(0).min())
    times = [step+t_start-1 for step in steps]
    
    linestyles = ['-', '--', '-.', ':']
    
    #assert len(steps)<=len(linestyles)
    colors = ["C0", "C1", "C2", "C3"]


    if title:
        title = "PR: " + title
    else:
        title = "PR"
    
    for step, linestyle in zip(steps, itertools.cycle(linestyles)):
        t = t_start + step - 1
        for col_pred, color in zip(cols_predictions, colors):
            y = df.loc[t][col_actual]
            score = df.loc[t][col_pred]
            precision, recall, _ = precision_recall_curve(y, score)
            this_auc = auc(recall, precision)
            pr = {
                'prec' : precision,
                'rec' : recall,
                'col' : col_pred.split("_")[0].upper(),
                'auc' : this_auc,
                'linestyle' : linestyle,
                't' : step,
                'color' : color
            }
            prs.append(pr)
    

    plt.figure(figsize=(16,16))
    for pr in prs:
        label = "t:{0}, {1} AUC:{2:0.3f}".format(pr['t'], pr['col'], pr['auc'])
        plt.plot(pr['rec'], pr['prec'], label=label, linestyle=pr['linestyle'], color=pr['color'])

    plt.legend(fontsize=fontsize)
    plt.xlabel('Recall', fontsize=fontsize)
    plt.ylabel('Precision', fontsize=fontsize)

    plt.title(title, fontsize=fontsize)

    plt.show()

