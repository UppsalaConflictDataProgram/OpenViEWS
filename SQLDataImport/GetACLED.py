"""
Loads ACLED into the database from the API and stage it.
It has two uses:
1. Completely restage ACLED into the database (so do a full upgrade of the data)
OR
2. Update the DB with one new month's release from ACLED
"""

from __future__ import print_function
from __future__ import division
import json
import requests
import pandas as pd
import time
from importTools.tools import backupOldTable
from sqlalchemy import create_engine
from sqlalchemy.sql import text as alchemy_text
from sqlalchemy.sql import select, column, func
from datetime import datetime, timedelta, date

__author__ = "Mihai Croicu"
__copyright__ = "(C) 2017 ViEWS, Uppsala University"
__credits__ = ["Mihai Croicu", "Haavard Hegre"]
__license__ = "All Rights Reserved"
__version__ = "0.2"
__maintainer__ = "Mihai Croicu"
__email__ = "VIEWSADMIN.croicu@pcr.uu.se"
__status__ = "Development"



def _getACLEDSlice(date_start, page_count):

    """
    Gets a slice of ACLED.
    Should NEVER be called by itself; it is a private method used by getACLED
    """

    url = 'http://api.acleddata.com/acled/read'
    #since ACLED only knows > and <, and we want >=, calculate yesterday's date
    event_date = datetime.strftime(datetime.strptime(date_start, '%Y-%m-%d') - timedelta(1),'%Y-%m-%d')
    payload = {'event_date':event_date,'event_date_where':'>','page':page_count}
    r = requests.get(url=url,params=payload)
    output = r.json()
    if output["count"] > 0:
        acled = pd.DataFrame(output['data'])
        count = output["count"]
    else:
        acled = None
        count = output["count"]
    return count, acled



def getACLED(from_date='1997-01-01',
             db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
             schema_name='dataprep',
             table_name='acled'):

    """Gets a copy of ACLED from (and including) the date supplied as a parameter and loads it
    into a temporary table of the ViEWS database
    :param from_date : grab events from this date and onwards. Script will always take all events up to the most recent
    :param db_engine_name : database engine URI in the standard URI formate (postgres://... or mysql://)
    :param schema_name : schema where the temporary table is to be put. Defaults to dataprep
    :param table_name : schema where the temporary table is to be put. Defaults to acled.
    """

    print ('Getting ACLED...')

    acled = pd.DataFrame()

    if schema_name.lower().strip() == 'staging':
        raise ValueError('Do you really think I am going to allow you to trash staging? No? Good.')

    cur_page = 1

    while True:
        count, acled_slice = _getACLEDSlice(from_date,cur_page)
        if count > 0:
            print (cur_page, " : ", count, " entries")
            acled = acled.append(acled_slice, ignore_index=True)
            cur_page+=1
        else:
            break

    print ("")
    print ("Inserting into database....")

    engine = create_engine(db_engine_name)
    acled.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='replace')

    print("Done loading :" + str(acled.shape[0]) + " rows")

def prepareACLED(db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
               schema_name='dataprep',
               table_name='acled'):
    engine = create_engine(db_engine_name)

    print ("Dropping old attached ACLED...")

    with engine.connect() as con:
        trans = con.begin()
        con.execute("DROP TABLE IF EXISTS preflight.acled_full")
        con.execute("DROP TABLE IF EXISTS preflight.acled")
        trans.commit()

    print ("Reattaching ACLED...")

    with engine.connect() as con:
        trans = con.begin()
        con.execute(
            """
    CREATE TABLE preflight.acled_full AS 
    WITH month_acled AS
    (
        SELECT
          *,
          EXTRACT(MONTH FROM event_date :: DATE) AS month,
          public.priogrid(latitude::float4,longitude::float4) AS priogrid_gid
        FROM """+schema_name+'.'+table_name+""" 
        WHERE latitude::float BETWEEN -180 AND 180 AND longitude::float BETWEEN -90 AND 90
    ),
        month_acled2 AS
      (
          SELECT
            month_acled.*,
            staging.month.id AS month_id
          FROM month_acled, staging.month
          WHERE
            (month_acled.year :: INT = staging.month.year_id AND
             month_acled.month = staging.month.month)
      )
    SELECT *
    FROM month_acled2;
            """
        )
        trans.commit()
        trans = con.begin()
        con.execute("ALTER TABLE preflight.acled_full ADD COLUMN type_of_violence INT")
        con.execute("ALTER TABLE preflight.acled_full ADD COLUMN type_of_protest VARCHAR(10)")
        trans.commit()
        trans = con.begin()

        print ('Attaching ViEWS categories to attached ACLED... State-based...',end='')

        #1. We are emulating UCDP/ViEWS StateBased category using ACLED data.
        #i.e. Military Forces vs. others/other Military Forces, only "battles" and "remote violence"
        #no civilians involved.
        #TODO: shelling and remote violence may need to be treated differently

        con.execute('''
        UPDATE preflight.acled_full SET type_of_violence = 1 WHERE 
        (event_type ilike '%%battle%%' OR event_type ilike '%%remote%%') 
        AND actor1||actor2 ilike '%%military forces%%'
        AND actor1||actor2 NOT ilike '%%civilians%%'
        ''')


        #2. We are emulating UCDP/ViEWS StateBased category using ACLED data.
        #i.e. no military forces, no civilians, only "battles" and "remote violence"
        #UCDP's artificial organizational criteria are not included and cannot for now be included

        print ('Non-state...',end='')

        con.execute('''
        UPDATE preflight.acled_full SET type_of_violence = 2 WHERE 
        (event_type ilike '%%battle%%' OR event_type ilike '%%remote%%')
        AND actor1||actor2 not ilike '%%military forces%%'
        AND actor1||actor2 NOT ilike '%%civilians%%'
        ''')

        print ('One-Sided...',end='')

        #3: Emulate UCDP/Views OneSided category.
        # Remote violence, battle and violence against civilians
        # TODO: This may be improved using a better division of "Remote Violence"

        con.execute('''
        UPDATE preflight.acled_full SET type_of_violence = 3 WHERE 
        (event_type ilike '%%battle%%' OR event_type ilike '%%remote%%' OR event_type ilike '%%civi%%')
        AND actor1||actor2 ilike '%%civilians%%'
        ''')

        print ('Protest')

        #4: Protests
        #The entire protest category, as is

        con.execute('''
        UPDATE preflight.acled_full SET type_of_violence = 4 WHERE
        event_type ilike '%%protest%%'        
        ''')
        trans.commit()
        trans = con.begin()
        query = alchemy_text("""
        UPDATE preflight.acled_full SET type_of_protest = 'p' 
        WHERE 
        type_of_violence=4 AND (inter1::int=6 OR inter2::int=6);
        """)
        con.execute(query)
        query = alchemy_text("""
        UPDATE preflight.acled_full SET type_of_protest = coalesce(type_of_protest,'') || 'r' 
        WHERE 
        type_of_violence=4 AND (inter1::int=5 OR inter2::int=5);
        """)
        con.execute(query)
        query = alchemy_text("""
        UPDATE preflight.acled_full SET type_of_protest = COALESCE(type_of_protest,'') || 'x' 
        WHERE 
        event_type ilike '%violence against civi%' AND interaction::int IN (15,16,25,26,35,36,45,46);
        """)
        con.execute(query)
        query = alchemy_text("""
        UPDATE preflight.acled_full SET type_of_protest = COALESCE(type_of_protest,'') || 'y' 
        WHERE
        event_type ilike '%violence against civi%' AND interaction::int IN (15,16);
        """)
        con.execute(query)
        trans.commit()

        # We are only using events precise enough to have locations within PGM cells
        # Thus, we exclude geo_precision 3 which indicates "larger area"
        # (unclear what that means but during testing, it was nearly always ADM1 or higher.

        trans = con.begin()
        print("Espen's categroies...")
        con.execute('DROP TABLE IF EXISTS preflight.acled')
        trans.commit()
        trans = con.begin()
        con.execute('CREATE TABLE preflight.acled AS SELECT * FROM preflight.acled_full WHERE geo_precision::int<3')
        trans.commit()
        trans = con.begin()
        print ("Indexing...")
        con.execute('''
        ALTER TABLE preflight.acled ADD PRIMARY KEY(index);
        ALTER TABLE preflight.acled_full ADD  PRIMARY KEY (index);
        CREATE INDEX acled_idx ON preflight.acled(priogrid_gid, month_id, type_of_violence);
        CREATE INDEX acled_full_idx ON preflight.acled_full(priogrid_gid, month_id, type_of_violence);
        CREATE INDEX acled2_idx ON preflight.acled(priogrid_gid, month_id, type_of_violence,type_of_protest);
        CREATE INDEX acled2_full_idx ON preflight.acled_full(priogrid_gid, month_id, type_of_violence,type_of_protest)
        ''')
        trans.commit()

def stageACLED(month_start=448,
               month_end=449,
               db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views'):

    # swap if month start > month end
    if month_start>month_end:
        month_start, month_end = month_end, month_start

    engine = create_engine(db_engine_name)

    with engine.connect() as con:

        # Check we don't want to update some column that doesn't exist in the downloaded ACLED
        # Last month in ACLED is always incomplete, thus use month-1 for end limit.

        limits = con.execute("SELECT min(month_id) AS int, max(month_id)-1 AS int FROM preflight.acled").fetchone()
        if limits[0]>month_start : month_start = limits[0]
        if limits[1]<=month_end : month_end = limits[1]

    print ("Updating PGM for months between ", month_start, " and ", month_end, "with sum/counts and geographic lags...")

    #This will compute event counts for priogrid-month observations as well as for 1st and 2nd order lags

    query = alchemy_text ('''
    UPDATE staging.priogrid_month SET
  acled_count_sb = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,1),
  acled_count_ns = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,2),
  acled_count_os = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,3),
  acled_count_pr = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,4),
  acled_count_prp= public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,'p'),
  acled_count_prr= public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,'r'),
  acled_count_prx= public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,'x'),
  acled_count_pry= public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,0,'y'),
  acled_fat_sb = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,1),
  acled_fat_ns = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,2),
  acled_fat_os = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,3),
  acled_fat_pr = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,4),
  acled_fat_prp= public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,'p'),
  acled_fat_prr= public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,'r'),
  acled_fat_prx= public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,'x'),
  acled_fat_pry= public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,0,'y'),
  acled_count_sb_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,1),
  acled_count_ns_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,2),
  acled_count_os_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,3),
  acled_count_pr_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,4),
  acled_count_prp_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,'p'),
  acled_count_prr_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,'r'),
  acled_count_prx_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,'x'),
  acled_count_pry_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,1,'y'),
  acled_fat_sb_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,1),
  acled_fat_ns_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,2),
  acled_fat_os_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,3),
  acled_fat_pr_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,4),
  acled_fat_prp_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,'p'),
  acled_fat_prr_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,'r'),
  acled_fat_prx_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,'x'),
  acled_fat_pry_lag1 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,1,'y'),
  acled_count_sb_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,1),
  acled_count_ns_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,2),
  acled_count_os_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,3),
  acled_count_pr_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,4),
  acled_count_prp_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,'p'),
  acled_count_prr_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,'r'),
  acled_count_prx_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,'x'),
  acled_count_pry_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,TRUE,2,'y'),
  acled_fat_sb_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,1),
  acled_fat_ns_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,2),
  acled_fat_os_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,3),
  acled_fat_pr_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,4),
  acled_fat_prp_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,'p'),
  acled_fat_prr_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,'r'),
  acled_fat_prx_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,'x'),
  acled_fat_pry_lag2 = public.aggregate_acled_pgm (priogrid_gid,month_id,FALSE,2,'y')
  WHERE month_id BETWEEN :m1 AND :m2
        AND
  priogrid_gid IN (SELECT gid FROM staging.priogrid WHERE in_africa)
  ''')
    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    print ("Creating temporal lags...")

    #This will compute temporal lags.
    #This must be run AFTER the above query has commited

    query = alchemy_text('''
SELECT public.make_priogrid_month_acled_temporal_lags(1,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(2,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(3,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(4,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(5,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(6,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(7,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(8,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_acled_temporal_lags(9,FALSE,:m1,:m2);
''')
    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    print ("Computing time since last event...")

    #This will compute time since last event.
    #This must be run AFTER the above query has commited

    query = alchemy_text('''
    UPDATE staging.priogrid_month SET
acled_months_since_last_sb = public.months_since_last_event('acled_count_sb', priogrid_gid, month_id),
acled_months_since_last_ns = public.months_since_last_event('acled_count_ns', priogrid_gid, month_id),
acled_months_since_last_os = public.months_since_last_event('acled_count_os', priogrid_gid, month_id),
acled_months_since_last_pr = public.months_since_last_event('acled_count_pr', priogrid_gid, month_id),
acled_months_since_last_prp = public.months_since_last_event('acled_count_prp', priogrid_gid, month_id),
acled_months_since_last_prr = public.months_since_last_event('acled_count_prr', priogrid_gid, month_id),
acled_months_since_last_prx = public.months_since_last_event('acled_count_prx', priogrid_gid, month_id),
acled_months_since_last_pry = public.months_since_last_event('acled_count_pry', priogrid_gid, month_id),
acled_months_since_last_sb_lag1 = public.months_since_last_event('acled_count_sb_lag1', priogrid_gid, month_id),
acled_months_since_last_ns_lag1 = public.months_since_last_event('acled_count_ns_lag1', priogrid_gid, month_id),
acled_months_since_last_os_lag1 = public.months_since_last_event('acled_count_os_lag1', priogrid_gid, month_id),
acled_months_since_last_pr_lag1 = public.months_since_last_event('acled_count_pr_lag1', priogrid_gid, month_id),
acled_months_since_last_prp_lag1 = public.months_since_last_event('acled_count_prp_lag1', priogrid_gid, month_id),
acled_months_since_last_prr_lag1 = public.months_since_last_event('acled_count_prr_lag1', priogrid_gid, month_id),
acled_months_since_last_prx_lag1 = public.months_since_last_event('acled_count_prx_lag1', priogrid_gid, month_id),
acled_months_since_last_pry_lag1 = public.months_since_last_event('acled_count_pry_lag1', priogrid_gid, month_id),
acled_months_since_last_sb_lag2 = public.months_since_last_event('acled_count_sb_lag2', priogrid_gid, month_id),
acled_months_since_last_ns_lag2 = public.months_since_last_event('acled_count_ns_lag2', priogrid_gid, month_id),
acled_months_since_last_os_lag2 = public.months_since_last_event('acled_count_os_lag2', priogrid_gid, month_id),
acled_months_since_last_pr_lag2 = public.months_since_last_event('acled_count_pr_lag2', priogrid_gid, month_id),
acled_months_since_last_prp_lag2 = public.months_since_last_event('acled_count_prp_lag2', priogrid_gid, month_id),
acled_months_since_last_prr_lag2 = public.months_since_last_event('acled_count_prr_lag2', priogrid_gid, month_id),
acled_months_since_last_prx_lag2 = public.months_since_last_event('acled_count_prx_lag2', priogrid_gid, month_id),
acled_months_since_last_pry_lag2 = public.months_since_last_event('acled_count_pry_lag2', priogrid_gid, month_id)
WHERE month_id BETWEEN :m1 AND :m2;
    ''')

    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)


    print("Preparing ACLED for CM...")

    with engine.connect() as con:

        trans = con.begin()
        query = "ALTER TABLE preflight.acled_full ADD COLUMN gwno INT"
        con.execute(query)
        trans.commit()

        trans = con.begin()
        query = "UPDATE preflight.acled_full SET gwno=isonum_to_gwcode(iso::int)"
        con.execute(query)
        trans.commit()

        trans = con.begin()
        try:
            con.execute("ALTER TABLE preflight.acled_full ADD COLUMN country_month_id INT")
        except:
            pass
        trans.commit()

        trans = con.begin()
        query = alchemy_text("""
        with a as
(SELECT cm.*, c.gwcode FROM staging.country_month cm left join
      staging.country c on (cm.country_id=c.id))
UPDATE preflight.acled_full SET country_month_id=a.id
FROM a
WHERE (a.gwcode::int = acled_full.gwno::int AND a.month_id = acled_full.month_id);
        """)
        con.execute(query)
        con.execute("CREATE INDEX acled_full_cm_idx ON preflight.acled_full(country_month_id, type_of_violence)")
        trans.commit()

        print("Updating CM aggregates for ACLED...")

        trans = con.begin()
        query = alchemy_text("""UPDATE staging.country_month SET
  acled_count_sb = public.aggregate_cm_acled(id,TRUE,0,1),
  acled_count_ns = public.aggregate_cm_acled(id,TRUE,0,2),
  acled_count_os = public.aggregate_cm_acled(id,TRUE,0,3),
  acled_count_pr = public.aggregate_cm_acled(id,TRUE,0,4),
  acled_count_sb_lag1 = public.aggregate_cm_acled(id,TRUE,1,1),
  acled_count_ns_lag1 = public.aggregate_cm_acled(id,TRUE,1,2),
  acled_count_os_lag1 = public.aggregate_cm_acled(id,TRUE,1,3),
  acled_count_pr_lag1 = public.aggregate_cm_acled(id,TRUE,1,4)
WHERE month_id BETWEEN :m1 AND :m2""")
        con.execute(query,m1=month_start,m2=month_end)
        trans.commit()
        print("Updating CM months since...")
        trans = con.begin()
        query = alchemy_text("""UPDATE staging.country_month SET
acled_months_since_last_sb = public.cm_months_since_last_event('acled_count_sb', country_id, month_id),
acled_months_since_last_ns = public.cm_months_since_last_event('acled_count_ns', country_id, month_id),
acled_months_since_last_os = public.cm_months_since_last_event('acled_count_os', country_id, month_id),
acled_months_since_last_pr = public.cm_months_since_last_event('acled_count_pr', country_id, month_id),
acled_months_since_last_sb_lag1 = public.cm_months_since_last_event('acled_count_sb_lag1', country_id, month_id),
acled_months_since_last_ns_lag1 = public.cm_months_since_last_event('acled_count_ns_lag1', country_id, month_id),
acled_months_since_last_os_lag1 = public.cm_months_since_last_event('acled_count_os_lag1', country_id, month_id),
acled_months_since_last_pr_lag1 = public.cm_months_since_last_event('acled_count_pr_lag1', country_id, month_id)
WHERE month_id BETWEEN :m1 AND :m2""")
        con.execute(query, m1=month_start - 12, m2=month_end + 12)
        trans.commit()
        print("Updating CM temporal lags...")
        trans = con.begin()
        query = alchemy_text("""
        SELECT make_country_month_acled_temporal_lags(1, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(2, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(3, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(4, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(5, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(6, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(7, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(8, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(9, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(10, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(11, FALSE, :m1, :m2);
SELECT make_country_month_acled_temporal_lags(12, FALSE, :m1, :m2);
""")
        con.execute(query, m1=month_start, m2=month_end)
        trans.commit()
    print ("Update complete!")

def getMonthID(year, month, db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views'):
    """
    converts a year and month into a Views MonthID
    :param year: Year as YYYY
    :param month:
    :param db_engine_name: Location of the VIEWS urI
    :return:
    """
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query=alchemy_text("""
        SELECT id FROM staging.month WHERE year_id=:y AND month=:m""")
        try:
            month_id = con.execute(query,y=year, m=month).fetchone()[0]
        except TypeError:
            raise ValueError("Supplied year and month do not fit the 1980-2030 range for values:",year,month)
        return month_id

if __name__ == "__main__":
    """If called from the terminal, takes four different optional params:
    -s --start: start-date
    -e --end: end-date
    -db --database: database URI
    -k --keepold: flag to keep old version of dataprep data
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", help="start date for update in ISO format (YYYY-MM-XX). "
                                          "Note that XX will always be converted to 01 automatically."
                                          "Must be above 1997-01-01."
                                          "Defaults to last month.")
    parser.add_argument("-e","--end", help="end date for update in ISO format (YYYY-MM-XX."
                                         "Note that XX will always be converted to last day of month."
                                         "Must be less than current month."
                                         "Defaults to previous month.")
    parser.add_argument("-k","--keep", help="preserve the old dataprep table", action="store_true")
    parser.add_argument("-db","--database",help="A valid database URI, eg: postgres://...; mysql:// etc.")
    args = parser.parse_args()

    #Get the last full month of available ACLED data.
    #If today's date is before the 8th, previous month is not available
    #(since it releases on the 7th), so use 2 months delay

    today_date = datetime.today()


    if today_date.day < 8:
        delta = 35
        #35 days from 1/MONTH should put us in the proper month no matter how long month is.
    else:
        delta = 1

    first_available_date = datetime(1997,1,1)
    last_available_date = datetime(today_date.year, today_date.month,1) - timedelta(delta)
    print ("ACLED is available up to (including): ", datetime.strftime(last_available_date,'%b-%Y'))

    """
    If no command line args are given, then only run on the last month of data availability.
    Since we only care about Y and M, we can use 01 for day throughout, even for the "end".
    """

    start_date = last_available_date
    end_date = last_available_date

    if args.start:
        try:
            start_date = datetime.strptime(args.start[:-3]+'-01', '%Y-%m-%d')
        except ValueError:
            start_date = last_available_date
            raise ValueError('Date MUST be supplied in YYYY-MM-DD format')

    if args.end:
        try:
            end_date = datetime.strptime(args.end[:-3] + '-01', '%Y-%m-%d')
        except ValueError:
            end_date = last_available_date
            raise ValueError('Date MUST be supplied in YYYY-MM-DD format')

    if start_date > end_date:
        print ("Start Date is later than end date. Switching them around!")
        end_date, start_date = start_date, end_date

    if start_date < first_available_date:
        print ("Start date is earlier than first ACLED availability. Will run from: ",
               datetime.strftime(last_available_date, '%b-%Y'))
        start_date = first_available_date

    if end_date > last_available_date:
        print ("End date is earlier than last ACLED availability. Will run up to: ",
               datetime.strftime(first_available_date,'%b-%Y'))

    if args.database:
        db_uri = args.database
    else:
        db_uri = 'postgresql://VIEWSADMIN@VIEWSHOST:5432/views'

    if args.keep:
        print ("Backing up old table...")
        backupOldTable(table_name='acled', db_engine_name=db_uri)
        backupOldTable(table_name='acled', db_engine_name=db_uri)

    print ("Run will update ACLED between: ",
           datetime.strftime(start_date, '%b-%Y'),"and",
           datetime.strftime(end_date, '%b-%Y'))

    start_at = getMonthID(start_date.year,start_date.month,db_engine_name=db_uri)
    stop_at = getMonthID(end_date.year,end_date.month,db_engine_name=db_uri)
    print ("Which is in ViEWS monthIDs: ", start_at ,"and", stop_at)

    getACLED(from_date=datetime.strftime(start_date,'%Y-%m-01'),table_name='acled',db_engine_name=db_uri)
    prepareACLED(table_name='acled',db_engine_name=db_uri)
   # stageACLED(start_at,stop_at,db_engine_name=db_uri)