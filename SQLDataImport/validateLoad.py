from __future__ import print_function
from __future__ import division
from tabulate import tabulate
from sqlalchemy import create_engine
from sqlalchemy.sql import text as alchemy_text
import pandas as pd


def validate (month_start,
              month_end,
              db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
              schema='preflight',
              table='flight_pgm'):
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query = alchemy_text("""SELECT min(month_id) as min, max(month_id) as max FROM """+schema+"."+table+""" 
        WHERE ged_count_sb IS NOT NULL  AND ged_count_sb > 0 AND month_id BETWEEN :m1 and :m2 """)
        try:
            result = con.execute(query, m1=month_start, m2=month_end).fetchone()
        except:
            result = None, None
    if result[0] is None:
        return False
    if int(result[0]) == int(month_start) and int(result[1]) == int(month_end):
        return True
    return False


def report_pgm (
        month_start,
        month_end,
        include_previous_months=0,
        db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
):
    month_start -= include_previous_months
    query=alchemy_text("""
    with a as (
    SELECT
      year_id,
      sum(to_dummy(ged_count_sb)) AS sb_count_pg,
      sum(to_dummy(ged_count_ns)) AS ns_count_pg,
      sum(to_dummy(ged_count_os)) AS os_count_pg,
      sum(ged_count_sb)           AS sb_count_events,
      sum(ged_count_ns)           AS ns_count_events,
      sum(ged_count_os)           AS os_count_events,
      sum(ged_best_sb)            AS sb_sum_deaths,
      sum(ged_best_ns)            AS ns_sum_deaths,
      sum(ged_best_os)            AS os_sum_deaths,
      month_id
    FROM preflight.flight_pgm
    WHERE month_id BETWEEN :s AND :e
    GROUP BY month_id, year_id
)
  SELECT m.month, a.*
FROM a, staging.month as m
WHERE a.month_id=m.id;
    """)
    query = query.bindparams(s=month_start, e=month_end)
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        report = pd.read_sql(sql=query,con=con)
        return (report)

def print_report (df,type='grid',to_screen=True):
    a = tabulate(df,headers='keys', showindex=False, tablefmt=type)
    if to_screen:
        print (a)
    return (a)

if __name__ == "__main__":
    print(validate(455,456))
    print_report(report_pgm(455, 456))
    print_report(report_pgm(455, 456), type='latex')
    print_report(report_pgm(455, 456), type='html')

