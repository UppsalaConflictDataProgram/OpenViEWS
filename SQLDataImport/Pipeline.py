from __future__ import print_function
from __future__ import division
from GetGED import *
from GetACLED import getACLED, stageACLED, prepareACLED
from RunPreflight import preflightRUN
from imputeGED import geoi_prepare, geoi_run, geoi_assemble, geoi_pgm_dummy_update
from validateLoad import validate
from config import *
from importTools import tools

def status_print(status):
    if status: print(' [OK] ')
    else: print (' [FAIL] ')


startmonth = tools.date_to_monthid(startmonth)
endmonth = tools.date_to_monthid(endmonth)

startiso = tools.monthid_to_ymd(startmonth)
endiso = tools.monthid_to_ymd(endmonth)

print ('Pipeline version 1.0')
print ('Now starting data import pipeline. Configuration in use:')
print ('Start Month:',startmonth)
print ('End Month:',endmonth)
print ('Version:',api_version)
print ('And working against:',db)
print ('***********************************************\n\n')

if do_ged:
    print('Now starting data import for GED:')
    print('***********************************************\n\n')

    go_ahead = checkGED(month_start=startmonth, version_number=api_version)
    if go_ahead:
        print('Checking if API contains correct data... [OK]')
    else:
        print('Checking if API contains correct data... [FAIL].\nExiting immediately')
        exit(99)

    getGED(version_number=api_version,
                 db_engine_name=db,
                 schema_name='dataprep',
                 table_name='ged')

    print ('***********************************************\n\n')
    print ('Preparing a load!\n')
    prepareGED(db_engine_name=db)
    print ('***********************************************\n\n')
    print ('Staging PGM\n')

    stageGED2PGM(month_start=startmonth, month_end=endmonth,db_engine_name=db)
    print ('***********************************************\n\n')
    print ('Staging CM\n')
    stageGED2CM(month_start=startmonth, month_end=endmonth,db_engine_name=db)
    print ('***********************************************\n\n')

    print ('Making imputations possible...\n')
    geoi_prepare(db_engine_name=db,lookup_schema='left_imputation',lookup_table='ged',
                      month_start=startmonth, month_end=endmonth)

    print ('Inputting Precision 4 (ADM1)...')
    geoi_run(15,db_engine_name=db,lookup_schema='left_imputation',lookup_table='ged',
            adm1=True)

    print ('\nInputting Precision 6 (Country)...')
    geoi_run(15,db_engine_name=db,lookup_schema='left_imputation',lookup_table='ged',
            adm1=False)


    print ('\nAssembling dataset...')
    geoi_assemble(db_engine_name=db,lookup_schema='left_imputation',lookup_table='ged',
                  month_start=startmonth, month_end=endmonth)

    print ('\nBuilding geoi_pgm_dummy dataset with 5 imputations')
    for i in range(1,6):
        print (i, sep=' ')
        geoi_pgm_dummy_update(i, db_engine_name=db,
                              lookup_schema='left_imputation',
                              month_start=startmonth,
                              month_end=endmonth)
    print ("\nDone with GED\n")

if do_acled:
    if startmonth<205:
        startmonth = 205
        startiso = '1997-01-01'
    print ('***********************************************'
           '\n***********************************************\n\n')
    print('Now starting data import for ACLED. Configuration in use:')
    print('Start Month:', startmonth)
    print('End Month:', endmonth)
    print('And working against:', db)
    print('***********************************************\n\n')
    print ('***********************************************\n\n')
    print ('Getting ACLED\n')
    getACLED(from_date=startiso, table_name='acled', db_engine_name=db)
    print ('Prepping ACLED\n')
    prepareACLED(table_name='acled', db_engine_name=db)
    print ('Staging ACLED\n')
    stageACLED(startmonth,endmonth,db_engine_name=db)

if preflight_when_done:
    print ("Running a preflight!\n*************************************\n")
    print ("PGM...")
    preflightRUN (db_engine_name=db,level='pgm')
    print("CM...")
    preflightRUN (db_engine_name=db,level='cm')

if validate_load and do_ged:
    print ("Checking GED load in staging/PGM...",end='')
    ok = validate(month_start=startmonth,month_end=endmonth,db_engine_name=db,schema='staging',table='priogrid_month')
    status_print(ok)
    print("Checking GED load in staging/CM...", end='')
    ok = validate(month_start=startmonth, month_end=endmonth, db_engine_name=db, schema='staging',table='country_month')
    status_print(ok)

if validate_load and preflight_when_done:
    print ("Checking GED load in preflight/PGM...",end='')
    ok = validate(month_start=startmonth,month_end=endmonth,db_engine_name=db,schema='preflight',table='flight_pgm')
    status_print(ok)
    print("Checking GED load in preflight/CM...", end='')
    ok = validate(month_start=startmonth, month_end=endmonth, db_engine_name=db, schema='preflight',table='flight_cm')
    status_print(ok)



print ("*************************************\n")
print ("Done. Happy forecasting! \n")
print ("*************************************\n")

