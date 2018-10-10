"""
Gets VDEM data and monthifies it with regimechange variables.
Pushes to dataprep.

RBJ 16-08-2018
"""

# @TODO
# 1. gross regime change direction? Also: dummy or category variable?
# 2. do we need backwards fill too for the first rows?

import argparse
import urllib
import sys
sys.path.append("../..")
from datetime import datetime
import pandas as pd
import numpy as np
import random
from views_utils import dbutils

# set seed
random.seed(1992)

# set connectstring
connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
                port="5432", prefix="postgresql",uname="VIEWSADMIN")

# valid date function
def valid_date(s):
    """converts string provided in argparse to datetime"""
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

# fetch monthid
def fetch_df_months(connectstring):
    q_months = """
    SELECT id, month, year_id
    FROM staging.month;
    """
    df_months = dbutils.query_to_df(connectstring, q_months)
    df_months.rename(columns={'id': 'month_id', 'year_id': 'year'}, inplace=True)
    #df_months['month_id'] = df_months['id']
    df_months.set_index(['year', 'month'], inplace=True)
    return df_months

#add arguments to add in bash
parser = argparse.ArgumentParser()
parser.add_argument("--ucdp_update", 
                    help="Latest UCDP update - format YYYY-MM-DD", 
                    required=True, 
                    type=valid_date)
parser.add_argument("--fcast_end", 
                    help="End of forecasting window - format YYYY-MM-DD", 
                    required=True, 
                    type=valid_date)
parser.add_argument("--path", 
                    help="Path to VDEM file", 
                    required=True)

args_main = parser.parse_args()
ucdp_update = args_main.ucdp_update
fcast_end = args_main.fcast_end
path = args_main.path

def diff_month(d1, d2):
    """compute number of months between two datetime objects"""
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def getVDEM(path):
    """Reads VDEM data and selects only core variables. Returns the csv """
    df = pd.read_csv(path)

    #remove subvariables
    df.drop(list(df.filter(regex = '_codehigh')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '_codelow')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '_ord')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '_osp')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '_rec')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '_ex')), axis = 1, inplace = True)
    df.drop(list(df.filter(regex = '_leg')), axis = 1, inplace = True)

    #remove numbered categoricals
    for i in range(0, 22):
        df.drop(list(df.filter(regex = '_{}'.format(i))), axis = 1, inplace = True)

    return df

def getVDEM_m():
    """Reads VDEM data and computes regime change variables""" 
    #fetch
    #"/storage/db/V-Dem-CY-v8.csv"
    vdem = pd.read_csv(path)

    #subset only the relevant columns
    #set to ccode
    vdem = vdem[['country_id', 'year', 'v2x_libdem']]
    vdem['month'] = 1

    #compute regimetype variables
    vdem['auto'] = np.where(vdem['v2x_libdem'] < .15, 1, 0)
    vdem['semi'] = np.where((vdem['v2x_libdem'] >= .15) & (vdem['v2x_libdem'] <= .5), 1, 0)
    vdem['demo'] = np.where(vdem['v2x_libdem'] > .5, 1, 0)

    #do the same for v2x_libdem squared
    vdem['v2x_libdem_sq'] = vdem['v2x_libdem'] ** 2
    vdem['auto_sq'] = np.where(vdem['v2x_libdem_sq'] < .15, 1, 0)
    vdem['semi_sq'] = np.where((vdem['v2x_libdem_sq'] >= .15) & (vdem['v2x_libdem_sq'] <= .5), 1, 0)
    vdem['demo_sq'] = np.where(vdem['v2x_libdem_sq'] > .5, 1, 0)

    #dummies
    vdem['libdem_lb'] = np.where(vdem['v2x_libdem'] > .7, 1, 0)
    vdem['libdem_ub'] = np.where(vdem['v2x_libdem'] < .82, 1, 0)

    #shift variables to compare differences
    vdem['prev_regimescore'] = vdem.groupby(['country_id'])['v2x_libdem'].shift()
    vdem['prev_auto'] = vdem.groupby(['country_id'])['auto'].shift(1)
    vdem['prev_semi'] = vdem.groupby(['country_id'])['semi'].shift(1)
    vdem['prev_demo'] = vdem.groupby(['country_id'])['demo'].shift(1)

    #compute gross regime change category 
    conditions = [
    (abs(vdem['v2x_libdem'] - vdem['prev_regimescore']) <= .02),
    ((abs(vdem['v2x_libdem'] - vdem['prev_regimescore']) > .02) & 
     (abs(vdem['v2x_libdem'] - vdem['prev_regimescore']) <= .05)),
    ((abs(vdem['v2x_libdem'] - vdem['prev_regimescore']) > .05) & 
     (abs(vdem['v2x_libdem'] - vdem['prev_regimescore']) <= .10)),
    (abs(vdem['v2x_libdem'] - vdem['prev_regimescore']) > .10)]
    choices = [0, 1, 2, 3]
    vdem['gross_regimechange'] = np.select(conditions, choices)

    #compute typified regime change category
    vdem['auto_to_semi'] = np.where((vdem.semi == 1) & (vdem.prev_auto == 1), 1, 0)
    vdem['auto_to_demo'] = np.where((vdem.demo == 1) & (vdem.prev_auto == 1), 1, 0)
    vdem['semi_to_auto'] = np.where((vdem.auto == 1) & (vdem.prev_semi == 1), 1, 0)
    vdem['semi_to_demo'] = np.where((vdem.demo == 1) & (vdem.prev_semi == 1), 1, 0)
    vdem['demo_to_auto'] = np.where((vdem.auto == 1) & (vdem.prev_demo == 1), 1, 0)
    vdem['demo_to_semi'] = np.where((vdem.semi == 1) & (vdem.prev_demo == 1), 1, 0)
    #return Libya and 125 as test
    # testcase = vdem[(vdem.country_id == 124) | (vdem.country_id == 125)]
    # testcase.to_csv("testcase.csv")
    return(vdem)

def monthifyVDEM():
    """Function applying the following transformations to VDEM:
    1. Duplicates all rows into 12 and adds month counter per country-year
    2. Calculates number of months between current month and last month in data
    3. Gets values for each country ending in 2017, and extends those to current
    4. For all months until end of dataset -1 year, draws random integer 1:12 to assign 
        months of regime change
    5. For all months after end of dataset -1 year, draws random integer 
    6. Copies forward last grouped row until the specified end of forecasting period
    """
    vdem_base = getVDEM_m()
    vdem = pd.DataFrame()

    #repeat rows over 12 months and add month-numbers
    for i in range(1, 13):
        vdem_base['month'] = i
        vdem = pd.concat([vdem, vdem_base])

    #get current year and enddate, and the number of months in between
    currentyear = ucdp_update.year
    endyear = vdem.year.max()
    enddate = datetime(endyear,12,1)
    monthdifference = diff_month(ucdp_update, enddate)

    #group and get endvalues of the data and extend to end of fcast window
    endvalues_base = vdem.sort_values(['year', 'month']).groupby('country_id').tail(1)
    endvalues_base = endvalues_base[endvalues_base['year'] == endyear]
    endvalues = pd.DataFrame()
    for i in range(1, (monthdifference + 1)):
        endvalues_base['year'] = currentyear
        endvalues_base['month'] = i
        endvalues = pd.concat([endvalues, endvalues_base])

    #add to overall dataset and reset index
    vdem = pd.concat([vdem, endvalues])
    vdem.reset_index(inplace=True, drop=True)

    #random draw of change-month in 10 iterations (hacky way)
    #I'm splitting the data in two now; until endyear -1 i.e. 2016 at this point:
    vdem_split1 = vdem.loc[vdem['year'] < (endyear)]

    def get_random_month(group):
        group[changecol] = np.random.randint(1,(13 + monthdifference))
        return group

    for i in range(1, 11):
        changecol = "changemonth_{}".format(i)
        vdem_split1 = vdem_split1.groupby(['country_id', 'year']).apply(get_random_month)
        index_changemonths = vdem_split1['month']==vdem_split1['changemonth_{}'.format(i)]
        vdem_split1['regimechange_{}'.format(i)] = 0
        vdem_split1.loc[index_changemonths, 'regimechange_{}'.format(i)] = 1

    #after 2016:
    vdem_split2 = vdem.loc[vdem['year'] >= (endyear)]

    def get_random_month_ext(group):
        group[changecol] = np.random.randint(1,(13 + monthdifference))
        return group

    for i in range(1, 11):
        changecol = "changemonth_{}".format(i)
        vdem_split2 = vdem_split2.groupby(['country_id']).apply(get_random_month_ext) #only group by country here
        #get locations of 2018 to change (-12 to only get the ones >12 to apply to 2018)
        reduced = vdem_split2.loc[vdem_split2.year==currentyear, 'changemonth_{}'.format(i)] - 12
        vdem_split2.loc[vdem_split2.year==currentyear, 'changemonth_{}'.format(i)] = reduced
        index_changemonths = vdem_split2['month']==vdem_split2['changemonth_{}'.format(i)]
        vdem_split2['regimechange_{}'.format(i)] = 0
        vdem_split2.loc[index_changemonths, 'regimechange_{}'.format(i)] = 1

    #and concatenate again
    vdem = pd.concat([vdem_split1, vdem_split2])

    #assign regime changes to changemonths only
    regimechange_vars = ['gross_regimechange', 'auto_to_semi', 'auto_to_demo',
                         'semi_to_auto', 'semi_to_demo', 'demo_to_auto',
                         'demo_to_semi']
    for var in regimechange_vars:
        for i in range(1, 11):
            index_changemonths = vdem['regimechange_{}'.format(i)]==1
            vdem['{}_{}'.format(var, i)] = 0
            vdem.loc[index_changemonths, '{}_{}'.format(var, i)] = vdem.loc[index_changemonths, var]

    #replace v2x_libdem with values from previous year until changemonth
    #monthid and reindexing first NOTE!!! SETS MINIMUM YEAR TO 1980
    #vdem['month_id'] = (vdem['year']*12) + (vdem['month'])
    vdem.set_index(['year', 'month'], inplace=True)
    ## actual month_id
    df_m = fetch_df_months(connectstring)
    vdem = vdem.merge(df_m, left_index=True, right_index=True)

    # index reset 
    vdem.reset_index(inplace=True)
    vdem.set_index(['month_id', 'country_id'], inplace=True)
    vdem.sort_index(inplace=True)

    for i in range(1, 11):
        x = vdem.loc[vdem['regimechange_{}'.format(i)]==1, 'v2x_libdem']
        vdem.loc[vdem['regimechange_{}'.format(i)]==1, 'v2x_libdem_new_{}'.format(i)] = x
        vars_to_fill = ['v2x_libdem_new_{}'.format(i)]
        vars_filled = ['v2x_monthlylibdem_{}'.format(i)]
        vdem[vars_filled] = vdem[vars_to_fill].groupby(level=1).fillna(method='ffill')
        
    vdem.reset_index(inplace=True)
    df_m.reset_index(inplace=True)
    #extend data to end of forecasting window (optional?)
    #add months to latest ucdp update month until end of year
    endvalues_base = vdem.sort_values(['year', 'month']).groupby('country_id').tail(1)
    endvalues_base = endvalues_base[endvalues_base['year'] == ucdp_update.year]
    endvalues = pd.DataFrame()
    for month in range((ucdp_update.month + 1), 13):
        endvalues_base['year'] = currentyear
        endvalues_base['month'] = month
        endvalues_base['month_id'] = endvalues_base['month_id'] + 1
        # concatenate
        endvalues = pd.concat([endvalues, endvalues_base])
    #and for years until the end of the forecasting window
    for year in range((ucdp_update.year + 1), (fcast_end.year + 1)):
        for month in range(1, 13):
            endvalues_base['year'] = year
            endvalues_base['month'] = month
            endvalues_base['month_id'] = endvalues_base['month_id'] + 1
            # concatenate
            endvalues = pd.concat([endvalues, endvalues_base])
    #concatenate that business
    vdem = pd.concat([vdem, endvalues])
    print(endvalues.month_id.values)
    #testfile to inspect
    testcase = vdem[(vdem.country_id == 124) | (vdem.country_id == 125)]
    testcase.to_csv("testcase_long.csv")

    #cleanup and return the values for changemonths only
    return(vdem)

# single
new_vdem = monthifyVDEM()
new_vdem.set_index(['country_id', 'month_id'], inplace=True)
new_vdem.to_csv("vdem_monthly.csv")

#push to DB
connectstring = dbutils.make_connectstring(prefix="postgresql", db="views",
                                           uname="VIEWSADMIN", hostname="VIEWSHOST",
                                           port="5432")
schema = "dataprep"
if_exists = "replace"
table = "vdem_regimechange"
dbutils.df_to_db(connectstring, new_vdem, schema, table, if_exists, write_index=True)
