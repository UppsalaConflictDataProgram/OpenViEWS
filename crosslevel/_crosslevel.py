""" Calibration module

This module calibrates test period probabilities based on calibration period
predicted probabilities and calibration period actual outcomes."""

import sys
import json

import pandas as pd
import numpy as np

sys.path.append("..")
import views_utils.dbutils as dbutils

def get_data(connectstring, runtype="fcast", period="calib"):
    """ Get actuals and calibration period and testing period predictions

    Args:
        connectstring:
        level: cm or pgm
        runtype: fcast or eval
    """

    def assert_equal_times(df1, df2, timevar):
        # Rewrite for list of dfs
        pass


    schema_link_ids = "staging_test"
    schema_predictions = "landed"

    timevar = "month_id"
    groupvar_c = "country_id"
    groupvar_pg = "pg_id"
    ids_c = [timevar, groupvar_c]
    ids_pg = [timevar, groupvar_pg]



    table_osa_pgm = "_".join(["osa", "pgm", runtype, period])
    table_ds_pgm = "_".join(["ds", "pgm", runtype, period])
    table_osa_cm = "_".join(["osa", "cm", runtype, period])
    table_ds_cm = "_".join(["ds", "cm", runtype, period])
    table_link_ids = "cpgm"

    df_osa_pgm = dbutils.db_to_df(connectstring, schema_predictions,
                                  table_osa_pgm, ids=ids_pg)
    df_ds_pgm = dbutils.db_to_df(connectstring, schema_predictions,
                                 table_ds_pgm, ids=ids_pg)
    df_osa_cm = dbutils.db_to_df(connectstring, schema_predictions,
                                 table_osa_cm, ids=ids_c)
    df_ds_cm = dbutils.db_to_df(connectstring, schema_predictions,
                                table_ds_cm, ids=ids_c)
    df_link_ids = dbutils.db_to_df(connectstring, schema_link_ids,
                                   table_link_ids, ids=ids_pg)

    for df in [df_osa_pgm, df_ds_pgm, df_osa_cm, df_ds_cm]:
        df.sort_index(inplace=True)

    df_pgm = df_osa_pgm.merge(df_ds_pgm, left_index=True, right_index=True)
    df_pgm = df_pgm.merge(df_link_ids, left_index=True, right_index=True)

    df_cm = df_osa_cm.merge(df_ds_cm, left_index=True, right_index=True)

    df_cm.reset_index(inplace=True)
    df_pgm.reset_index(inplace=True)

    df_pgm = df_pgm.merge(df_cm, on=[timevar, groupvar_c])
    df_pgm.set_index(ids_pg, inplace=True)
    df_pgm.drop(columns=[groupvar_c], inplace=True)
    return df_pgm


def publish_results(connectstring, df, runtype, period):
    schema = "landed"
    table = "cl_pgm_{runtype}_{period}".format(runtype=runtype, period=period)

    dbutils.df_to_db(connectstring, df, schema, table, if_exists="replace",
                     write_index=True)

def compute_crosslevels(df, template, runtype, period, outcomes):

    def fill_template_str(s, runtype, period, outcome):
        s = s.replace("RUNTYPE", runtype)
        s = s.replace("PERIOD", period)
        s = s.replace("OUTCOME", outcome)
        return s

    # Get the index only
    df_cl = df[[]].copy()

    for cl_name in template:
        name = cl_name
        cols = template[name].copy()

        for outcome in outcomes:
            this_name = fill_template_str(name, runtype, period, outcome)
            these_cols = [fill_template_str(col, runtype, period, outcome)
                          for col in cols]

            df_cl[this_name] = df[these_cols].product(axis=1)

    return df_cl



def main():
    """ crosslevel main """
    uname = "VIEWSADMIN"
    prefix = "postgresql"
    db = "views"
    port = "5432"
    hostname = "VIEWSHOST"
    connectstring = dbutils.make_connectstring(prefix, db, uname,
                                               hostname, port)

    runtypes = ["eval", "fcast"]
    periods = ["calib", "test"]
    outcomes = ["sb", "ns", "os"]

    with open("crosslevels.json", 'r') as f:
                template=json.load(f)

    for runtype in runtypes:
        for period in periods:
            df = get_data(connectstring, runtype, period)
            df_cl = compute_crosslevels(df, template, runtype, period, outcomes)
            publish_results(connectstring, df_cl, runtype, period)



if __name__ == "__main__":
    main()