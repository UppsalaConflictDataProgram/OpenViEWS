"""Load GED into the database from the API
Works perfectly but must be packaged to allow for options.
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

def _get_ged_slice(next_page_url, token=None):
    headers = {'x-ucdp-access-token': token}
    r = requests.get(next_page_url, headers=headers)
    output = r.json()
    next_page_url = output['NextPageUrl'] if output['NextPageUrl'] != '' else None
    ged = pd.DataFrame(output['Result'])
    page_count = output['TotalPages']
    return next_page_url, ged, page_count

def checkGED(db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
             version_number='5.9.99',
             month_start=400,
             imputation=True):

    print (month_start)

    if imputation:
        month_start=month_start-11

    engine = create_engine(db_engine_name)

    with engine.connect() as con:
        query = alchemy_text("SELECT month, year_id FROM staging.month WHERE id=:sd")
        go = False
        try:
            result = con.execute(query,sd=month_start).fetchone()
            iso_start_check = '{1:04d}-{0:02d}-01'.format(*result)
            iso_end_check = '{1:04d}-{0:02d}-25'.format(*result)
            next_page_url = 'http://ucdpapi.pcr.uu.se/api/gedevents/'+version_number+'?pagesize=1&StartDate='+iso_start_check+'&EndDate='+iso_end_check
            print(next_page_url)
            next_page_url, ged_slice, total_pages = _get_ged_slice(next_page_url=next_page_url,
                                                                   token='48dda3460c347f3b')
            # print(iso_start_check, iso_end_check, total_pages)
            if total_pages>0: go = True
        except: go = False
        return go

def getGED(version_number='5.9.99',
             db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
             schema_name='dataprep',
             table_name='ged'):

    print ("Getting GED...\n")
    cur_page = 1

    next_page_url = 'http://ucdpapi.pcr.uu.se/api/gedevents/'+version_number+'?pagesize=1000'

    ged = pd.DataFrame()

    while next_page_url:
        next_page_url, ged_slice, total_pages = _get_ged_slice(next_page_url=next_page_url,
                                                 token='48dda3460c347f3b')
        ged = ged.append(ged_slice, ignore_index=True)
        print(cur_page,'/',total_pages,'pages loaded')
        cur_page+=1

    print("Inserting into database now...")

    engine = create_engine(db_engine_name)
    ged.to_sql(name=table_name, schema=schema_name, con=engine, if_exists='replace')

    print("\nDone loading :" + str(ged.shape[0]) + " rows into table " + table_name + "\n")

def prepareGED(db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
               schema_name='dataprep',
               table_name='ged'):
    engine = create_engine(db_engine_name)

    print ("Dropping old attached GED...")

    with engine.connect() as con:
        con.execute("DROP TABLE IF EXISTS preflight.ged_attached_full")
        con.execute("DROP TABLE IF EXISTS preflight.ged_attached")

    print("Attaching new GED...")

    query = alchemy_text("""

CREATE TABLE preflight.ged_attached AS
  (
    WITH month_ged AS
    (
        SELECT
          *,
          EXTRACT(MONTH FROM date_start :: DATE) AS month_start,
          EXTRACT(MONTH FROM date_end :: DATE)   AS month_end
        FROM """+schema_name+'.'+table_name+"""
    ),
        month_ged_start AS
      (
          SELECT
            month_ged.*,
            staging.month.id AS month_id_start
          FROM month_ged, staging.month
          WHERE
            (month_ged.year :: INT = staging.month.year_id AND
             month_ged.month_start = staging.month.month)
      ),
        month_ged_full AS
      (
          SELECT
            month_ged_start.*,
            staging.month.id AS month_id_end
          FROM month_ged_start, staging.month
          WHERE
            (month_ged_start.year :: INT = staging.month.year_id AND
             month_ged_start.month_end = staging.month.month)
      )
    SELECT *
    FROM month_ged_full
  );

""")

    print ("Geometrifying...")

    with engine.connect() as con:
        con.execute(query)
        con.execute('ALTER TABLE preflight.ged_attached ADD PRIMARY KEY (id)')
        con.execute('ALTER TABLE preflight.ged_attached ADD COLUMN country_month_id_end bigint')
        con.execute('ALTER TABLE preflight.ged_attached ADD COLUMN country_month_id_start bigint')
        con.execute('ALTER TABLE preflight.ged_attached DROP COLUMN IF EXISTS geom')
        con.execute('ALTER TABLE preflight.ged_attached ADD COLUMN geom geometry (point,4326)')
        con.execute("UPDATE preflight.ged_attached SET geom=st_setsrid(st_geometryfromtext(geom_wkt),4326) WHERE geom_wkt<>''")

    print ("Attaching country information...")


    with engine.connect() as con:
        trans = con.begin()
        con.execute('CREATE TABLE preflight.ged_attached_full AS SELECT * FROM preflight.ged_attached')
        trans.commit()


    print ("Indexing...")

    with engine.connect() as con:
        con.execute('DELETE FROM preflight.ged_attached WHERE where_prec IN (4,6,7)')
        con.execute('ALTER TABLE preflight.ged_attached_full ADD PRIMARY KEY (id)')
        con.execute('CREATE INDEX ged_attached_gidx ON preflight.ged_attached USING GIST(geom)')
        con.execute('CREATE INDEX ged_attached_idx ON preflight.ged_attached (priogrid_gid,month_id_end, type_of_violence)')
        con.execute('CREATE INDEX ged_attached_s_idx ON preflight.ged_attached (priogrid_gid,month_id_start, type_of_violence)')
        con.execute('CREATE INDEX ged_attached_full_gidx ON preflight.ged_attached_full USING GIST(geom)')
        con.execute('CREATE INDEX ged_attached_fullx_s_idx ON preflight.ged_attached_full (priogrid_gid,month_id_end, type_of_violence)')
        con.execute('CREATE INDEX ged_attached_fullx_gidx ON preflight.ged_attached_full (priogrid_gid,month_id_start, type_of_violence)')

    with engine.connect() as con:
        trans = con.begin()
        con.execute("""with a as
    (SELECT cm.*, c.gwcode FROM staging.country_month cm left join
          staging.country c on (cm.country_id=c.id))
    UPDATE preflight.ged_attached_full SET country_month_id_end=a.id
    FROM a
    WHERE (a.gwcode = ged_attached_full.country_id AND a.month_id = ged_attached_full.month_id_end);
    """)
        trans.commit()


    with engine.connect() as con:
        trans = con.begin()
        con.execute("""with a as
    (SELECT cm.*, c.gwcode FROM staging.country_month cm left join
          staging.country c on (cm.country_id=c.id))
    UPDATE preflight.ged_attached_full SET country_month_id_start=a.id
    FROM a
    WHERE (a.gwcode = ged_attached_full.country_id AND a.month_id = ged_attached_full.month_id_start);
    """)
        trans.commit()

def stageGED2CM(month_start=445,
               month_end=446,
               db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views'):

    if month_start > month_end:
        month_start, month_end = month_end, month_start

    engine = create_engine(db_engine_name)

    with engine.connect() as con:
        limits = con.execute("SELECT min(month_id_end) AS int, max(month_id_end) AS int FROM preflight.ged_attached").fetchone()
        if limits[0]>month_start : month_start = limits[0]
        if limits[1]<=month_end : month_end = limits[1]

    print ("start/end:",month_start,month_end)

    print ("Staging Country-Month with base GED variables and spatial lags...")

    query = alchemy_text ("""
    UPDATE staging.country_month SET
    ged_best_sb = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,0,1),
    ged_best_ns = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,0,2),
    ged_best_os = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,0,3),
    ged_count_sb = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,0,1),
    ged_count_ns = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,0,2),
    ged_count_os = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,0,3),
    ged_best_sb_lag1 = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,1,1),
    ged_best_ns_lag1 = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,1,2),
    ged_best_os_lag1 = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,1,3),
    ged_count_sb_lag1 = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,1,1),
    ged_count_ns_lag1 = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,1,2),
    ged_count_os_lag1 = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,1,3) WHERE
month_id BETWEEN :m1 AND :m2 """)

    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    print ("Staging Country-Month t-lags...")

    query = alchemy_text ("""
SELECT public.make_country_month_temporal_lags(1,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(2,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(3,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(4,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(5,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(6,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(7,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(8,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(9,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(10,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(11,FALSE,109,:m2);
SELECT public.make_country_month_temporal_lags(12,FALSE,109,:m2);
    """)

    with engine.connect() as con:
        con.execute(query,m2=month_end)

    print ("Staging Country-Month distances to nearest event...")

    query = alchemy_text ("""
    UPDATE staging.country_month SET
ged_months_since_last_sb = public.cm_months_since_last_event('ged_count_sb', country_id, month_id),
ged_months_since_last_ns = public.cm_months_since_last_event('ged_count_ns', country_id, month_id),
ged_months_since_last_os = public.cm_months_since_last_event('ged_count_os', country_id, month_id),
ged_months_since_last_sb_lag1 = public.cm_months_since_last_event('ged_count_sb_lag1', country_id, month_id),
ged_months_since_last_ns_lag1 = public.cm_months_since_last_event('ged_count_ns_lag1', country_id, month_id),
ged_months_since_last_os_lag1 = public.cm_months_since_last_event('ged_count_os_lag1', country_id, month_id)
WHERE month_id BETWEEN :m1 AND :m2""")

    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    with engine.connect() as con:
        print("Updating base onset variables for CM...")
        trans = con.begin()
        query = alchemy_text("""with a as (SELECT * FROM onset_months_table('staging','country_month','ged_best_sb','country_id'))
          UPDATE staging.country_month SET onset_months_sb = a.onset_distance
          FROM a
          WHERE a.id=staging.country_month.id;

        with a as (SELECT * FROM onset_months_table('staging','country_month','ged_best_ns','country_id'))
          UPDATE staging.country_month SET onset_months_ns = a.onset_distance
          FROM a
          WHERE a.id=staging.country_month.id;

        with a as (SELECT * FROM onset_months_table('staging','country_month','ged_best_os','country_id'))
          UPDATE staging.country_month SET onset_months_os = a.onset_distance
          FROM a
          WHERE a.id=staging.country_month.id;""")
        con.execute(query)
        trans.commit()


def stageGED2PGM(month_start=445,
               month_end=446,
               db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views'):

    if month_start > month_end:
        month_start, month_end = month_end, month_start

    engine = create_engine(db_engine_name)

    with engine.connect() as con:
        limits = con.execute("SELECT min(month_id_end) AS int, max(month_id_end) AS int FROM preflight.ged_attached").fetchone()
        if limits[0]>month_start : month_start = limits[0]
        if limits[1]<=month_end : month_end = limits[1]

    print (month_start, month_end)

    print ("Updating sums...")

    query = alchemy_text ("""UPDATE staging.priogrid_month SET
  ged_best_sb = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 0, 1),
  ged_best_ns = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 0, 2),
  ged_best_os = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 0, 3),
  ged_count_sb = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 0, 1),
  ged_count_ns = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 0, 2),
  ged_count_os = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 0, 3),
   ged_best_sb_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, FALSE, FALSE, 0, 1),
   ged_best_ns_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, FALSE, FALSE, 0, 2),
   ged_best_os_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, FALSE, FALSE, 0, 3),
   ged_count_sb_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, TRUE, FALSE, 0, 1),
   ged_count_ns_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, TRUE, FALSE, 0, 2),
   ged_count_os_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, TRUE, FALSE, 0, 3),
    ged_best_sb_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 1, 1),
 ged_best_ns_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 1, 2),
 ged_best_os_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 1, 3),
 ged_count_sb_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 1, 1),
 ged_count_ns_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 1, 2),
 ged_count_os_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 1, 3),
  ged_best_sb_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 2, 1),
 ged_best_ns_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 2, 2),
 ged_best_os_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 2, 3),
 ged_count_sb_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 2, 1),
 ged_count_ns_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 2, 2),
 ged_count_os_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 2, 3)
WHERE
  month_id >= :m1 AND month_id <= :m2 """)

    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    print ("Creating temporal lags...")

    #This will compute temporal lags.
    #This must be run AFTER the above query has commited

    query = alchemy_text('''
SELECT public.make_priogrid_month_temporal_lags(1,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(2,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(3,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(4,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(5,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(6,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(7,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(8,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(9,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(10,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(11,FALSE,:m1,:m2);
SELECT public.make_priogrid_month_temporal_lags(12,FALSE,:m1,:m2);
''')
    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    print ("Updating count variables...")

    query = alchemy_text('''
    UPDATE staging.priogrid_month SET
ged_months_since_last_sb = public.months_since_last_event('ged_count_sb', priogrid_gid, month_id),
ged_months_since_last_ns = public.months_since_last_event('ged_count_ns', priogrid_gid, month_id),
ged_months_since_last_os = public.months_since_last_event('ged_count_os', priogrid_gid, month_id),
ged_months_since_last_sb_lag1 = public.months_since_last_event('ged_count_sb_lag1', priogrid_gid, month_id),
ged_months_since_last_ns_lag1 = public.months_since_last_event('ged_count_ns_lag1', priogrid_gid, month_id),
ged_months_since_last_os_lag1 = public.months_since_last_event('ged_count_os_lag1', priogrid_gid, month_id),
ged_months_since_last_sb_lag2 = public.months_since_last_event('ged_count_sb_lag2', priogrid_gid, month_id),
ged_months_since_last_ns_lag2 = public.months_since_last_event('ged_count_ns_lag2', priogrid_gid, month_id),
ged_months_since_last_os_lag2 = public.months_since_last_event('ged_count_os_lag2', priogrid_gid, month_id)
WHERE month_id BETWEEN :m1 AND :m2''')
    with engine.connect() as con:
        con.execute(query,m1=month_start,m2=month_end)

    print("Computing Spatial Distances...")

    with engine.connect() as con:
        query = alchemy_text("""
UPDATE staging.priogrid_month SET
dist_ged_sb_event=public.distance_to_nearest_ged('preflight','ged_attached',priogrid_gid,month_id,1),
dist_ged_ns_event=public.distance_to_nearest_ged('preflight','ged_attached',priogrid_gid,month_id,2),
dist_ged_os_event=public.distance_to_nearest_ged('preflight','ged_attached',priogrid_gid,month_id,3)
WHERE month_id BETWEEN :m1 AND :m2
""")
        con.execute(query,m1=month_start,m2=month_end)

    print("Updating base onset variables for PGM...")

    with engine.connect() as con:
        trans = con.begin()
        query = alchemy_text("""
        with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_sb'))
  UPDATE staging.priogrid_month SET onset_months_sb = a.onset_distance
  FROM a
  WHERE a.id=staging.priogrid_month.id;


with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_ns'))
  UPDATE staging.priogrid_month SET onset_months_ns = a.onset_distance
  FROM a
  WHERE a.id=staging.priogrid_month.id;


with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_os'))
  UPDATE staging.priogrid_month SET onset_months_os = a.onset_distance
  FROM a
  WHERE a.id=staging.priogrid_month.id;
        """)
        con.execute(query)
        trans.commit()

    print ("Updating onsets based on spatial lags at PGM...")

    with engine.connect() as con:
        trans = con.begin()
        query = alchemy_text("""UPDATE staging.priogrid_month SET
  onset_month_sb_lag1 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 1,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_sb'::varchar),

  onset_month_sb_lag2 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 2,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_sb'::varchar)
WHERE onset_months_sb > 0 AND month_id BETWEEN :m1 AND :m2;


UPDATE staging.priogrid_month SET
  onset_month_ns_lag1 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 1,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_ns'::varchar),

  onset_month_ns_lag2 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 2,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_ns'::varchar)
WHERE onset_months_ns > 0 AND month_id BETWEEN :m1 AND :m2;

UPDATE staging.priogrid_month SET
  onset_month_os_lag1 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 1,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_os'::varchar),

  onset_month_os_lag2 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 2,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_os'::varchar)
WHERE onset_months_os > 0 AND month_id BETWEEN :m1 AND :m2;
""")
        con.execute(query, m1=month_start, m2=month_end)
        trans.commit()


    print("Update complete!")


if __name__ == "__main__":
    #backupOldTable()
    getGED(version_number='18.1',
             db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/ucdp',
             schema_name='public',
             table_name='ged_cand')
    #prepareGED()
    #stageGED2PGM(month_start=445, month_end=454)
    #stageGED2CM(month_start=445, month_end=454)

