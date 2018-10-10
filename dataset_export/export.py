import libexport2 as ex
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from libdataqueries import data_queries
from export_config import run_id, db

pd.set_option('float_format', '{:f}'.format)



engine = create_engine(db)

print ("*"*24)
print ("Directory is: ", run_id)
print( "Database is:", db)
print (" ")
print ("*"*24)
print ("Exporting predictions...")
print ("*"*24)


levels = ('sb','ns','os')

for level in levels:
    print ('\nLevel: ',level)
    print("*" * 24)
    print ('PGM level predictions....')
    directory = run_id+'/predictions_'+level
    dataset = ex.Predictions (level='pgm', level_var='pg_id', run='fcast', outcome=level, db_engine=db)
    dataset.save_bulk (directory=directory+'_pgm')
    print ('CM level predictions....')
    dataset_cm = ex.Predictions (level='cm', level_var='country_id', run='fcast', outcome=level, db_engine=db)
    dataset_cm.save_bulk(directory=directory + '_cm')
    print ('Metadata....')
    with open(directory+'_pgm/metadata.json','w') as f:
        f.write(dataset.metadata())
    with open(directory+'_cm/metadata.json','w') as f:
        f.write(dataset_cm.metadata())

print ("Identifying date ranges...")

start_date_data = 109
end_date_data = 600
try:
    end_date_data,_ = dataset.temporal_extent()
    end_date_data -=1
except:
    pass

print ("Exporting evaluation dataset (including actuals)...")

for level in levels:
    print ('\nLevel: ',level)
    print("*" * 24)
    print ('PGM level predictions....')
    directory = run_id+'/eval_'+level
    dataset = ex.Predictions (level='pgm', level_var='pg_id', run='eval', outcome=level, db_engine=db)
    dataset.hook_actuals (schema = 'launched', table = 'transforms_pgm_imp_1', column_name = 'ged_dummy_OUTCOME')
    dataset.save_bulk (directory=directory+'_pgm')
    print ('CM level predictions....')
    dataset_cm = ex.Predictions (level='cm', level_var='country_id', run='eval', outcome=level, db_engine=db)
    dataset_cm.hook_actuals(schema='preflight', table='flight_cm', column_name='ged_dummy_OUTCOME')
    dataset_cm.save_bulk(directory=directory + '_cm')
    print ('Metadata....')
    with open(directory+'_pgm/metadata.json','w') as f:
        f.write(dataset.metadata())
    with open(directory+'_cm/metadata.json','w') as f:
        f.write(dataset_cm.metadata())


print ("*"*24)
print ("Exporting underlying data...")
print ("*"*24)
print (" ")

#Get temporal extent of the training data. This is always the first predicted month minus 1.
#Take this from the last dataset processed above so that we don't bother the user.

print ("Training data between:", start_date_data, end_date_data)

with engine.connect() as con:
    for key in data_queries:
        print (key)
        print ("*"*24)
        query = text(data_queries[key])
        query = query.bindparams(s=start_date_data, e=end_date_data)
        dataset_d = ex.Dataset(query, db_engine_name = db)
        dataset_d.save(directory=run_id+'/data',filename=key+'.csv')
