""" Utils for one step ahead forecasts"""
import sys

import traceback

import pandas as pd
import numpy as np
import functools
import pickle
import os

sys.path.insert(0, "..")
import views_utils.dbutils as dbutils

def create_dirs(dirs):
    """Create a folder in locations supplied by each of the arguments"""
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)
            print("Created directory", d)


def get_y_X_step(df, step, outcome, features,
    share_zeros_keep=1, share_ones_keep=1):
    """ Get arrays y_t, X_(t-step) from df

    The goal of OSA forecasting is to predict the future using the present.
    We want to train models that predict y_(t+36) based on X_t.
    To train models like these we have to align the future outcome to the
    present predictors, or analogously align the present outcome to the past
    predictors.

    There are two ways of achieving this:

        * We could lead our outcome: y_(t+36) ~ f(X_t)
        * We could lag our predictors: y_t ~ f(X_(t-36))

    We choose lagging our predictors.
    By lagging X instead of leading y we move the lead/lag induced
    missingness in the training data from the latest observations
    (leading y) to the most distant training data (lagging X).

    Args:
        df: Training data
        step: Time periods to lag features by
        outcome: outcome variable
        features: list of features to lag,
        share_zeros_keep: share of outcome==0 rows to keep
        share_ones_keep: share of outcome==1 rows to keep
    Returns:
        y: array of outcome
        X: matrix of lagged features

    """
    def downsample(df, outcomes, share_zeros_keep, share_ones_keep):
        """ Downsamples a dataframe to balance it in terms of outcomes.

        Returns a subset of a dataframe where the supplied shares of ones
        and zeros are kept.
        Ones are considered as rows where the outcome columns are greater
        than zero.

        Args:
          df:
          outcomes: list of strings, variables to consider,
          share_zeros_keep:
          share_ones_keep:

        Returns:
            df, a downsampled dataframe
        """

        # if outcomes is given as a single string
        if isinstance(outcomes, str):
            df_ones  = df[df[[outcomes]].sum(axis=1)>0]
            df_zeros = df[df[[outcomes]].sum(axis=1)==0]
        # if outcomes is a list of columns
        else:
            df_ones  = df[df[outcomes].sum(axis=1)>0]
            df_zeros = df[df[outcomes].sum(axis=1)==0]

        n_ones  = len(df_ones)
        n_zeros = len(df_zeros)

        n_ones_want  = int(n_ones  * share_ones_keep)
        n_zeros_want = int(n_zeros * share_zeros_keep)


        df_sampled  = pd.concat(
            [df_ones.sample( n = n_ones_want),
             df_zeros.sample(n = n_zeros_want)])

        return df_sampled

    # Lag the features by step, level 1 is groupvar
    df_step = df[features].groupby(level=1).shift(step)
    # Don't lag outcomes/labels
    df_step[outcome] = df[outcome]

    # lagging the features introduces missingness at furthest past, drop that
    df_step.dropna(inplace=True)

    df_step = downsample(df_step, outcome,
        share_zeros_keep, share_ones_keep)

    y = np.asarray(df_step[outcome])
    X = np.asarray(df_step[features])

    return y, X

def get_X_forecast(df, forecast_start, features):
    """ Get matrix X_(t_forecast_start-1)

    For predicting Y between t_forecast_start and t_forecast_end we use
    X_(t_forecast_start - 1), the last seen data before forecast.

    Args:
        df: Pre-forecast data
        forecast_start: integer time-id of forecast start
        features: list of features
    Returns:
        X: Matrix of features from t_(forecast_start-1)
    """

    t_forecast_X = forecast_start - 1
    df.sort_index(inplace=True)
    df = df.loc[t_forecast_X]
    df = df[features]

    # Make sure we're not missing any data
    for col in df.columns:
        message = "Missing values for {}".format(col)
        assert df[col].isnull().sum()==0, message

    X = np.asarray(df)
    return X

def add_li(df, cols, overwrite=True):
    """Add interpolated versions of cols to df"""
    df.sort_index(inplace=True)
    if overwrite:
        df[cols] = df[cols].groupby(level=1).apply(
            lambda group: group.interpolate())
    else:
        df_ipol = df[cols].groupby(level=1).apply(
            lambda group: group.interpolate())
        df_ipol = df_ipol.add_suffix("_li")
        df = df.merge(df_ipol, left_index=True, right_index=True)
    return df

def fetch_data(model):
    """ Reads df_train and df_forecast from db

    df_train contains ids, outcomes and features for the training period.
    df_forecast contains only ids for the forecasting period.
    """

    def get_columns_train(model, ids):
        columns = []
        columns += ids
        columns.append(model['outcome'])
        columns += model['features']
        return columns

    def get_columns_forecast(model, ids):
        columns = ids
        return columns

    connectstring = model['table']['connectstring']
    schema   = model['table']['schema']
    table    = model['table']['table']
    timevar  = model['table']['timevar']
    groupvar = model['table']['groupvar']
    ids = [timevar, groupvar]

    df_train = dbutils.db_to_df_limited(
        connectstring = connectstring,
        schema   = schema,
        table    = table,
        columns  = get_columns_train(model, ids),
        timevar  = timevar,
        groupvar = groupvar,
        tmin     = model['train_start'],
        tmax     = model['train_end']
        )

    df_forecast = dbutils.db_to_df_limited(
        connectstring = connectstring,
        schema   = schema,
        table    = table,
        columns  = get_columns_forecast(model, ids),
        timevar  = timevar,
        groupvar = groupvar,
        tmin     = model['forecast_start'],
        tmax     = model['forecast_end']
        )

    return df_train, df_forecast

def forecast(model):
    """ Main forecasting function

    Args:
        model: dictionary containing the following fields:
            'name' : descriptive name that goes into the column name of results
            'outcome'   : Name of outcome variable
            'estimator' : A scikit-like object with .fit() and .predict() method
            'features'  : List of features or predictors
            'steps'     : The time-steps to train and forecast for
            'share_zeros_keep'  : Share of outcome=0 observations to use
            'share_ones_keep'   : Share of outcome=1 observations to use
            'train_start'   :
            'train_end'     :
            'forecast_start':
            'forecast_end'  :
            'table' : dictionary containing:
                'connectstring' : connectstring,
                'schema'    : schema to read data from
                'table'     : table to read data from
                'timevar'   : time variable, used for subsetting and indexing
                'groupvar'  : group variable, such as pg_id or country_id

    Returns:
        df_forecast: a df containing the forecast results

    Example:
        >>> from sklearn.neural_network import MLPClassifier
        >>> connectstring = "postgresql://VIEWSADMIN@VIEWSHOST:5432/views"
        >>> table_input = {
        ...     'connectstring' : connectstring,
        ...     'schema'    : 'launched',
        ...     'table'     : 'imp_imp_1',
        ...     'timevar'   : 'month_id',
        ...     'groupvar'  : 'pg_id'
        ...     }
        >>> model = model_hist = {
        ...     'name'      : 'mlp_sb_hist',
        ...     'outcome'   : 'ged_dummy_sb',
        ...     'estimator' : MLPClassifier(),
        ...     'features'  : ["ged_dummy_sb", "ged_dummy_ns", "ged_dummy_os"],
        ...     'steps'     : [1,36],
        ...     'share_zeros_keep'  : 0.1,
        ...     'share_ones_keep'   : 0.1,
        ...     'train_start'   : 370,
        ...     'train_end'     : 408,
        ...     'forecast_start': 409,
        ...     'forecast_end'  : 444,
        ...     'table' : table_input
        ...    }
        >>> df = forecast(model)
        """

    # colname for predicted probability
    name = model['name']
    p_name = "osa_" + name

    # Unpack the dictionary, because using kwargs makes too much sense
    steps = model['steps']
    outcome  = model['outcome']
    features = model['features']
    share_zeros_keep = model['share_zeros_keep']
    share_ones_keep  = model['share_ones_keep']

    print("Starting forecast {}".format(name))
    print("Fetching data")
    df_train, df_forecast = fetch_data(model)

    # Initalise empty columns in df_forecast to hold predictions
    df_forecast[p_name] = np.nan

    # Check we got the times righr
    forecast_start = df_forecast.index.get_level_values(0).min()
    assert forecast_start==model['forecast_start']

    # X_forecast is the last month of known data, used to make the predictions
    X_forecast = get_X_forecast(df_train, forecast_start, model['features'])

    for step in steps:
        print("Training {} step {}".format(name, str(step)))

        y_train, X_train = get_y_X_step(
            df = df_train, step=step,
            outcome=outcome, features=features,
            share_zeros_keep=share_zeros_keep, share_ones_keep=share_ones_keep)

        model['estimator'].fit(X_train, y_train)
        print(model['estimator'])

        path_pickle = "{d}/{n}_{s}.pickle".format(d=model['dir_pickles'],
                                                  n=model['name'],
                                                  s=step)
        path_pickle = os.path.expandvars(path_pickle)
        with open(path_pickle, 'wb') as f:
            pickle.dump(model, f)
        print("wrote", path_pickle)

        y_pred = model['estimator'].predict(X_forecast)
        # [:,1] gets the probs for label y=1
        y_p_pred = model['estimator'].predict_proba(X_forecast)[:,1]

        t = forecast_start + step - 1

        # assign the predicitions to the result dataframe
        df_forecast.loc[t, p_name] = y_p_pred

    names = [p_name]
    df_forecast = add_li(df_forecast, names)

    print("Finished forecasting {}".format(name))
    return df_forecast

def forecast_many(models):
    """Wrapper for forecast()

    Forecasts for a list of models and returns the merged results.

    Args:
        models: A list of dictionaries compatible with forecast()
    Returns:
        df: Outer-joined dataframe of forecasted predictions
    """
    dfs = []
    # for model in models:
    #     create_dirs([model['dir_pickles']])
    #     # Do the forecasting
    #     try:
    #         dfs.append(forecast(model))
    #     # Respect KeyboardInterrupt
    #     except KeyboardInterrupt:
    #         raise
    #     # If the forecast fails for some reason just print the failed model and continue
    #     except:
    #         print("#"*80)
    #         print("failed to forecast", model['name'])
    #         traceback.print_exc()
    #         print("#"*80)
    #         pass

    for model in models:
        dir_pickles = model['dir_pickles']
        dir_pickles = os.path.expandvars(dir_pickles)
        create_dirs([dir_pickles])

        dfs.append(forecast(model))

    # Merge the results
    df = functools.reduce(
        lambda x, y: pd.merge(x, y,
            left_index=True, right_index=True, how='outer'), dfs)
    return df


