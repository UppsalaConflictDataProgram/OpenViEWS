import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
pd.set_option('float_format', '{:f}'.format)

def columnid2columnname (lookup_tables, column_id_list, db='postgresql://VIEWSADMIN@VIEWSHOST:5432/views'):
    '''
    Take 1 indexed column rows and all the tables where they reside, and return a tuple column of the predictions_pgm
    format
    :return: a list of predictions_pgm format. This is fugly. This works for now.
    '''
    x=[]
    engine = create_engine(db)
    with engine.connect() as con:
        for tname in lookup_tables:
            rowname = pd.read_sql("SELECT * FROM " + tname + " LIMIT 1", con)
            rowname = list(rowname.columns.values)
            rowname = [rowname[i - 1] for i in column_id_list]
            rowname = [(i, tname) for i in rowname]
            x.extend(rowname)
        return(x)


engine = create_engine("postgresql://VIEWSADMIN@VIEWSHOST:5432/views")

#These are for the input data.
start_date_data = 109
end_date_data = 461

#Below are the columns and tables to be used for extracting the prediction files
#They extract the predicted model columns from the model tables (see below for examples) and push it to file.
#You can specify either named columns (SQL style) in the format below. Set variable below to False.
#Or column positional ids (1-indexed) (R style). Set variable below to True.


use_numeric_columns = True

#If false, these will be used

predictions_cm = [
    ('average_sb', 'landed.sb_ensemble_fcast_cm'),
    ('average_ns', 'landed.ns_ensemble_fcast_cm'),
    ('average_os', 'landed.os_ensemble_fcast_cm')
]

predictions_pgm = [
    ('average_select_sb', 'landed.sb_ensemble_fcast_pgm'),
    ('average_select_ns', 'landed.ns_ensemble_fcast_pgm'),
    ('average_select_os', 'landed.os_ensemble_fcast_pgm')
]

#If you want to use numeric column indices, spec them here.
#
#

prediction_pgm_columns = [3,4,6,8,10,11,12,14,21,22,23,26,31]
prediction_pgm_tables =  ['landed.sb_ensemble_fcast_pgm','landed.ns_ensemble_fcast_pgm','landed.os_ensemble_fcast_pgm']
prediction_cm_columns = list(range(3,10))
prediction_cm_tables =  ['landed.sb_ensemble_fcast_cm','landed.ns_ensemble_fcast_cm','landed.os_ensemble_fcast_cm']

if use_numeric_columns:
    predictions_pgm = columnid2columnname(prediction_pgm_tables,prediction_pgm_columns)
    predictions_cm = columnid2columnname(prediction_cm_tables, prediction_cm_columns)


# ***********************************************
#### DO NOT CHANGE ANYTHING BEYOND THIS POINT! **
#### DO NOT CHANGE ANYTHING BEYOND THIS POINT! **
#************************************************


queries_data = {
'ucdp_month_country':'''
SELECT 
id,
gwcode,
month_id,
year_id as year,
month,
ged_dummy_sb,
ged_count_sb,
ged_best_sb,
ged_dummy_ns,
ged_count_ns,
ged_best_ns,
ged_dummy_os,
ged_count_os,
ged_best_os,
ged_count_sb_lag1,
ged_count_ns_lag1,
ged_count_os_lag1,
ged_best_sb_lag1,
ged_best_ns_lag1,
ged_best_os_lag1
FROM preflight.flight_cm WHERE month_id BETWEEN :s AND :e AND 
(gwcode BETWEEN 400 and 627 OR gwcode=651) 
''',
'ucdp_month_priogrid':'''SELECT
  id,
  pg_id,
  month_id,
  year_id as year,
  CASE WHEN month_id%12=0 THEN 12 ELSE month_id%12 END as month,
  gwcode,
  ged_dummy_sb,
  ged_count_sb,
  ged_best_sb,
  ged_dummy_ns,
  ged_count_ns,
  ged_best_ns,
  ged_dummy_os,
  ged_count_os,
  ged_best_os
FROM preflight.flight_pgm WHERE month_id BETWEEN :s AND :e ORDER BY month_id,pg_id''',
  'imputted_priogrid':''' SELECT
*
FROM left_imputation.pgm WHERE month_id BETWEEN :s AND :e
'''}

print ("Now exporting data...")
print ("*"*24)

with engine.connect() as con:
    for key in queries_data:
        print (key)
        print ("*"*24)
        query = text(queries_data[key])
        query = query.bindparams(s=start_date_data, e=end_date_data)
        df = pd.read_sql(query,con)
        df.to_csv(key+'.csv.gz', compression='gzip', index=False)

df = None


print ("Now exporting predictions...")
print ("*"*24)
print ("PGM...")
print ("*"*24)
print ("*"*24)


with engine.connect() as con:
    out = None
    for column, table in predictions_pgm:
        print("Doing:",column,table)
        query = text('SELECT pg_id, month_id, "'+column+'" FROM '+table)
        df = pd.read_sql(query, con)
        try:
            out = out.merge(df, on=['pg_id','month_id'], how='inner')
        except:
            out = df
    #print(out.head(100))
    out['pg_id'] = out['pg_id'].astype(int)
    out['month_id'] = out['month_id'].astype(int)
    out['month'] = (out['month_id']%12).astype(int)
    out.loc[out.month == 0, 'month'] = 12
    out['year'] = (np.floor(out['month_id'] / 12) + 1980).astype(int)
    out.to_csv('predictions_pgm.csv.gz', compression='gzip', index=False)

print ("CM...")
print ("*"*24)
print ("*"*24)

with engine.connect() as con:
    out = None
    for column, table in predictions_cm:
        print("Doing:",column,table)
        query = text('SELECT country_id_to_gwcode(country_id::int) as country_id, month_id, "'+column+'" FROM '+table)
        df = pd.read_sql(query, con)
        try:
            out = out.merge(df, on=['country_id','month_id'], how='inner')
        except:
            out = df
    #print(out.head(100))
    out['month_id'] = out['month_id'].astype(int)
    out['month'] = (out['month_id']%12).astype(int)
    #out['month'][out['month_id'] == 0] = 12
    out.loc[out.month == 0, 'month'] = 12

    out['year'] = (np.floor(out['month_id'] / 12) + 1980).astype(int)
    out.to_csv('predictions_cm.csv.gz', compression='gzip', index=False)


