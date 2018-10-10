""" Calibration module

This module calibrates test period probabilities based on calibration period
predicted probabilities and calibration period actual outcomes."""

import sys

import pandas as pd
import numpy as np

import statsmodels.api as sm
import patsy

sys.path.append("..")
import views_utils.dbutils as dbutils




def assert_equal_times(df1, df2, timevar):
    """ Assert that two dataframes have the same time limits """
    t_start_1 = df1.index.get_level_values(timevar).min()
    t_end_1 = df1.index.get_level_values(timevar).max()

    t_start_2 = df2.index.get_level_values(timevar).min()
    t_end_2 = df2.index.get_level_values(timevar).max()

    assert t_start_1 == t_start_2
    assert t_end_1 == t_end_2

def get_data(connectstring, level="cm", runtype="fcast"):
    """ Get actuals and calibration period and testing period predictions

    Args:
        connectstring:
        level: cm or pgm
        runtype: fcast or eval
    """

    schema_actuals = "preflight"
    schema_predictions = "landed"

    table_actuals = "flight_" + level
    cols_actual = ["ged_dummy_" + t for t in ["sb", "ns", "os"]]
    cols_actual.append("acled_dummy_pr")

    timevar = "month_id"
    if level == "cm":
        groupvar = "country_id"
    elif level == "pgm":
        groupvar = "pg_id"
    ids = [timevar, groupvar]

    table_osa_calib = "_".join(["osa", level, runtype, "calib"])
    table_osa_test = "_".join(["osa", level, runtype, "test"])
    table_ds_calib = "_".join(["ds", level, runtype, "calib"])
    table_ds_test = "_".join(["ds", level, runtype, "test"])
    table_cl_calib = "_".join(["cl", level, runtype, "calib"])
    table_cl_test = "_".join(["cl", level, runtype, "test"])



    df_osa_calib = dbutils.db_to_df(connectstring, schema_predictions,
                                    table_osa_calib, ids=ids)
    df_osa_test = dbutils.db_to_df(connectstring, schema_predictions,
                                   table_osa_test, ids=ids)

    df_ds_calib = dbutils.db_to_df(connectstring, schema_predictions,
                                   table_ds_calib, ids=ids)
    df_ds_test = dbutils.db_to_df(connectstring, schema_predictions,
                                  table_ds_test, ids=ids)

    # only include cl for pgm level
    if level=="pgm":
        df_cl_calib = dbutils.db_to_df(connectstring, schema_predictions,
                                       table_cl_calib, ids=ids)
        df_cl_test = dbutils.db_to_df(connectstring, schema_predictions,
                                      table_cl_test, ids=ids)


    assert_equal_times(df_osa_calib, df_ds_calib, timevar)
    assert_equal_times(df_osa_test, df_ds_test, timevar)

    t_start_calib = df_osa_calib.index.get_level_values(timevar).min()
    t_end_calib = df_osa_calib.index.get_level_values(timevar).max()

    df_pred_calib = df_osa_calib.merge(df_ds_calib,
                                       left_index=True, right_index=True)

    df_pred_test = df_osa_test.merge(df_ds_test,
                                     left_index=True, right_index=True)

    # only include cl for pgm level
    if level == "pgm":
        df_pred_calib = df_pred_calib.merge(df_cl_calib,
                                            left_index=True, right_index=True)
        df_pred_test = df_pred_test.merge(df_cl_test,
                                            left_index=True, right_index=True)

    df_actuals = dbutils.db_to_df_limited(connectstring,
                                          schema_actuals, table_actuals,
                                          columns=cols_actual,
                                          timevar=timevar,
                                          groupvar=groupvar,
                                          tmin=t_start_calib,
                                          tmax=t_end_calib)

    for df in [df_actuals, df_pred_calib, df_pred_test]:
        df.sort_index(inplace=True)


    return df_actuals, df_pred_calib, df_pred_test


def calibrate_models(df_actuals, df_pred_calib, df_pred_test):
    """ Calibrate test-period predicted probs using calib-period predictions

    Args:
        df_actuals: Actual outcomes for calib period
        df_pred_calib: Predictions for calib period
        df_pred_test: Preditions for test period
    Returns:
        df_pred_test_calibrated: Calibrated predictions for test period
        """

    def prob_to_logodds(p, clip=True):
        """ Convert probabilities to logodds
        Args:
            p: Probability
            clip: clip p=0 and p=1 to """
        if clip:
            #assert not (np.max(p) > 1), "probs greater than 1"
            #assert not (np.min(p) < 0), "probs smaller than 0"
            p = np.clip(p, 0.000000001, 0.999999999)
        logodds = np.log(p/(1-p))

        return logodds

    def match_pred_to_actual(col):
        """ Match prediction column name to its corresponding actual outcome """

        matches = {
            'sb' : 'ged_dummy_sb',
            'ns' : 'ged_dummy_ns',
            'os' : 'ged_dummy_os',
            'pr' : 'acled_dummy_pr',
        }

        for key in matches:
            if col.endswith(key):
                match = matches[key]
                break

        return match

    def match_test_to_calib(col_test, df_calib):
        """Get the corresponding calib colname for a given test col.

        Args:
            col_test: name of test column
            df_calib: a df of calibration period predictions
        Returns:
            col_calib: name of the corresponding calibration col
        """
        col_calib = col_test.replace("_test_", "_calib_")
        message = "No matching calib col found for {}".format(col_test)
        assert col_calib in df_calib.columns, message
        return col_calib

    def get_scaling_params(df_actual, df_calib, col_actual, col_calib):
        """ Gets scaling params based on regression actual ~ probs_calib
        Args:
            df_actual: df with actual outcomes for calib period
            df_calib: df with predicted logodds for calib period
            col_actual: colname for actual outcome
            col_calib: colname for calibration prediction
        Returns:
            intercept:
            beta:
        """

        df = df_actual.merge(df_calib, left_index=True, right_index=True)

        formula = "{} ~ {}".format(col_actual, col_calib)
        y, X = patsy.dmatrices(formula, df)
        model = sm.Logit(y, X).fit(disp=0)
        intercept = model.params[0]
        beta = model.params[1]

        return intercept, beta

    def apply_scaling_params(df, col_test, intercept, beta):
        """ Scale logodds in df[col_test] using intercept and beta"""
        numerator = np.exp(intercept + (beta*df[[col_test]]))
        denominator = (np.exp(intercept + (beta*df[[col_test]]))+1)
        scaled_probs = numerator / denominator

        return scaled_probs


    # Skeleton df for storing calibrated probs
    df_pred_test_calibrated = df_pred_test[[]].copy()

    df_pred_calib = prob_to_logodds(df_pred_calib)
    df_pred_test = prob_to_logodds(df_pred_test)

    for col_test in df_pred_test:


        col_calib = match_test_to_calib(col_test, df_pred_calib)
        col_actual = match_pred_to_actual(col_test)

        print("Calibrating", col_test, "to", col_calib)

        df_this_actual = df_actuals[[col_actual]]
        df_this_calib = df_pred_calib[[col_calib]]
        df_this_test = df_pred_test[[col_test]]

        intercept, beta = get_scaling_params(df_this_actual, df_this_calib,
                                             col_actual, col_calib)

        scaled_probs = apply_scaling_params(df_this_test, col_test,
                                            intercept, beta)

        df_pred_test_calibrated[[col_test]] = scaled_probs

    return df_pred_test_calibrated



def publish_results(connectstring, df, level, runtype):
    schema = "landed"
    table = "calibrated_{level}_{runtype}_test".format(level=level,
                                                       runtype=runtype)

    dbutils.df_to_db(connectstring, df, schema, table, if_exists="replace",
                     write_index=True)


def main():
    """ Run calibration """
    uname = "VIEWSADMIN"
    prefix = "postgresql"
    db = "views"
    port = "5432"
    hostname = "VIEWSHOST"
    connectstring = dbutils.make_connectstring(prefix, db, uname,
                                               hostname, port)

    levels = ["cm", "pgm"]
    runtypes = ["eval", "fcast"]

    for level in levels:
        for runtype in runtypes:
            df_actuals, df_calib, df_test = get_data(connectstring,
                                                     level,
                                                     runtype)
            df_test_calibrated = calibrate_models(df_actuals, df_calib, df_test)

            publish_results(connectstring, df_test_calibrated, level, runtype)



if __name__ == "__main__":
    main()
