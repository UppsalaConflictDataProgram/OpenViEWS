""""""

import sys
import json

import pandas as pd
import numpy as np

sys.path.append("..")
import views_utils.dbutils as dbutils

def get_data(connectstring, level, runtype):
    """"""

    schema = "landed"

    timevar = "month_id"
    if level == "cm":
        groupvar = "country_id"
    elif level == "pgm":
        groupvar = "pg_id"
    ids = [timevar, groupvar]

    table = "_".join(["calibrated", level, runtype, "test"])
    df = dbutils.db_to_df(connectstring, schema, table, ids=ids)
    df.sort_index(inplace=True)

    return df



def publish_results(connectstring, df, level, runtype):
    """"""
    schema = "landed"
    table = "ensemble_{level}_{runtype}_test".format(level=level,
                                                       runtype=runtype)

    dbutils.df_to_db(connectstring, df, schema, table, if_exists="replace",
                     write_index=True)

def compute_ensembles(df, templates, level, runtype, outcomes):
    """"""
    def fill_template_str(s, runtype, outcome):
        s = s.replace("RUNTYPE", runtype)
        s = s.replace("OUTCOME", outcome)
        return s

    df_ens = df[[]].copy()

    template = templates[level]

    for ens_name in template:
        name = ens_name
        cols = template[name].copy()

        for outcome in outcomes:
            this_name = fill_template_str(name, runtype, outcome)
            these_cols = [fill_template_str(col, runtype, outcome)
                          for col in cols]

            print("Computing ensemble", this_name)
            df_ens[this_name] = df[these_cols].mean(axis=1)

    return df_ens

def main():
    """ Ensemble main """
    uname = "VIEWSADMIN"
    prefix = "postgresql"
    db = "views"
    port = "5432"
    hostname = "VIEWSHOST"
    connectstring = dbutils.make_connectstring(prefix, db, uname,
                                               hostname, port)

    levels = ["cm", "pgm"]
    runtypes = ["eval", "fcast"]
    outcomes = ["sb", "ns", "os"]

    with open("ensembles_cm.json", 'r') as f:
        template_cm = json.load(f)
    with open("ensembles_pgm.json", 'r') as f:
        template_pgm = json.load(f)
    templates = {
        'pgm' : template_pgm,
        'cm' : template_cm
    }

    for level in levels:
        for runtype in runtypes:
            df = get_data(connectstring, level, runtype)
            df_ens = compute_ensembles(df, templates, level, runtype, outcomes)
            print(df_ens)
            publish_results(connectstring, df_ens, level, runtype)



if __name__ == "__main__":
    main()
