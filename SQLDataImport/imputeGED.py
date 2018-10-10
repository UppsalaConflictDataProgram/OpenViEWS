from __future__ import print_function
from __future__ import division
from sqlalchemy import create_engine
from sqlalchemy.sql import select, column, func, text as alchemy_text
from importTools import tools
import pandas as pd
from numpy import log1p

def fpoint2pgm(
             point,
             db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
             polygon_schema_name='geoimputation',
             polygon_table_name='gadm1'):
    """
    :param db_engine_name: The location of the ADM
    :param polygon_schema_name:
    :param polygon_table_name:
    :return: a dataframe containing all the GIDs and the AREAS.

    What this does is that it un-fuzzies the fpoint by associating it with all the PGMs that the point may represent.
    A polygon dataset that represents the extent that each point represents (e.g. an ADM dataset for points representing
    administrative divisions or a country dataset for points representing countries) is needed.
    """

    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query = select([column('gid'),column('area')]).\
            select_from(func.geoi_fpoint2poly2pg(
            point,
            polygon_schema_name,
            polygon_table_name
        )
        )
        result = pd.read_sql(query,con)
        if result.empty: result[0]=[0,0]
        return result

def geteventdensity (
        priogrids_df,
        month,
        conflict_id,
        db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
        schema='geoimputation',
        table='ged'):
    """
    :param priogrids_df:
    :param month:
    :param db_engine_name:
    :param db_table_name:
    :return:
    """
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query = alchemy_text("SELECT priogrid_gid, count(*)*100 as density FROM "+schema+"."+table+
                             " WHERE conflict_new_id = :conflict AND month_id_end=:date GROUP BY priogrid_gid")
        query = query.bindparams(conflict=conflict_id, date=month)
        density_df = pd.read_sql(query,con)
        #print(density_df)
    df_merge = priogrids_df.merge(density_df, left_on='gid', right_on='priogrid_gid', how='left')
    df_merge = df_merge.drop('priogrid_gid',axis=1)
    df_merge = df_merge.fillna(1)
    #print (df_merge)
    #print ("**************************")
    return df_merge


#density = fpoint2pgm('POINT(66 32.12)')

def geom_inputation (
        db_engine_name,
        lookup_schema,
        lookup_table,
        adm_table,
        number_imputations,
        point_id,
        point_geom,
        month_start,
        conflict_id
):
    density = fpoint2pgm(point_geom,
                         db_engine_name=db_engine_name,
                         polygon_schema_name=lookup_schema,
                         polygon_table_name=adm_table)
    #print ("!*!*!*!*!*!*!*!*!*!*!*!*!*!*")
    #print (density)
    for past_months in range(0, 13):
        decay = 2 ** ((past_months * -1.0) / 12.0)
        #print(past_months, decay)
        density = geteventdensity(density, month=month_start - past_months, conflict_id=conflict_id,
                                  db_engine_name=db_engine_name, schema=lookup_schema,table=lookup_table)
        #print (density)
        if 'density_old' in density:
            density['density_old'] = density['density_old'] + density['density'] * decay
        else:
            density['density_old'] = density['density']
        density = density.drop('density', axis=1)
        #density.density_old = log1p(density.density_old)
    #print(density)
    #print("************************")
    sampled_point = density.sample(n=number_imputations, replace=True, axis=0, weights='density_old')
    point_id=[point_id]
    point_id.extend(sampled_point['gid'].tolist())
    return pd.DataFrame([point_id])

def geoi_prepare (
        db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
        lookup_schema = 'geoimputation',
        lookup_table = 'ged',
        month_start = 400,
        month_end = 400
):
    """Copies the current attached GED for the lookup to work"""
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        con.execute('DROP TABLE IF EXISTS '+lookup_schema+'.'+lookup_table)
        con.execute('DROP TABLE IF EXISTS '+lookup_schema+'.gedfull')
        con.execute('DROP TABLE IF EXISTS ' + lookup_schema + '.toimp4')
        con.execute('DROP TABLE IF EXISTS ' + lookup_schema + '.toimp6')
        trans = con.begin()
        con.execute('CREATE TABLE  '+lookup_schema+'.'+lookup_table+' AS SELECT id,priogrid_gid,conflict_new_id,month_id_end,'
                                                                    'month_id_start,type_of_violence, geom, best '
                                                                 'FROM preflight.ged_attached')
        con.execute('CREATE TABLE  ' + lookup_schema + '.gedfull AS SELECT id,priogrid_gid,conflict_new_id,month_id_end,'
                                                                    'month_id_start,type_of_violence, geom, best '
                                                                    'FROM preflight.ged_attached_full')
        con.execute('CREATE INDEX lookup_idx ON '+lookup_schema+'.'+lookup_table+' (conflict_new_id,month_id_end)')
        con.execute('CREATE INDEX lookup2_idx ON '+lookup_schema+'.'+lookup_table+' (priogrid_gid)')
        con.execute(alchemy_text('CREATE TABLE  '+lookup_schema+'.toimp4 AS SELECT * FROM preflight.ged_attached_full where where_prec=4'
                                                   ' AND month_id_end between :m1 and :m2'),m1=month_start,m2=month_end)
        con.execute(alchemy_text('CREATE TABLE  '+lookup_schema+'.toimp6 AS SELECT * FROM preflight.ged_attached_full where where_prec=6'
                                                   ' AND month_id_end between :m1 and :m2 AND geom IS NOT NULL'),m1=month_start,m2=month_end)
        trans.commit()


def geoi_run(
        count = 15,
        db_engine_name = 'postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
        lookup_schema = 'geoimputation',
        lookup_table = 'ged',
        adm1 = True
    ):

    engine = create_engine(db_engine_name)
    out_df = pd.DataFrame()
    if adm1:
        poly_table='gadm1'
        table_id='4'
    else:
        poly_table='country'
        table_id='6'
    with engine.connect() as con:
        query = alchemy_text("SELECT count(*) FROM "+lookup_schema+'.toimp'+table_id)
        row_count=con.execute(query).fetchone()
        i=0
        tools.printProgressBar(0,row_count[0],prefix='Progress:',suffix='Complete',bar_length=50)

        query = alchemy_text("SELECT id,geom_wkt,month_id_end as month_id,conflict_new_id as conflict_id "
                             "FROM "+lookup_schema+'.toimp'+table_id)
        for row in con.execute(query):
            #print(row)
            i+=1
            tools.printProgressBar(i, row_count[0], prefix='Progress:', suffix='Complete', bar_length=50)
            out_df = out_df.append(geom_inputation(db_engine_name,
                                                   lookup_schema,
                                                   lookup_table,
                                                   poly_table,
                                                   count,
                                                   *row))
        out_df = out_df.rename(columns={0: 'id'})
        out_df.to_sql(con=con, name='geoi_out_'+table_id, schema=lookup_schema, if_exists='replace', index=False)


def geoi_assemble(
        db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
        lookup_schema='geoimputation',
        lookup_table='ged',
        month_start=400,
        month_end=400
):

    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        trans = con.begin()
        query = alchemy_text("DROP TABLE IF EXISTS "+lookup_schema+".geoi_out_all;")
        trans.commit()
        con.execute(query)
        query = alchemy_text('''
        CREATE TABLE '''+lookup_schema+'''.geoi_out_all AS
SELECT * FROM '''+lookup_schema+'''.geoi_out_4 WHERE "1"<>1 UNION
SELECT * FROM '''+lookup_schema+'''.geoi_out_6 WHERE "1"<>1 UNION
SELECT id,
  priogrid_gid as "1",
  priogrid_gid as "2",
  priogrid_gid as "3",
  priogrid_gid as "4",
  priogrid_gid as "5",
  priogrid_gid as "6",
  priogrid_gid as "7",
  priogrid_gid as "8",
  priogrid_gid as "9",
    priogrid_gid as "10",
    priogrid_gid as "11",
    priogrid_gid as "12",
    priogrid_gid as "13",
    priogrid_gid as "14",
    priogrid_gid as "15"
FROM '''+lookup_schema+'''.'''+lookup_table+'''
WHERE month_id_end BETWEEN :m1 AND :m2;
        ''')
        con.execute(query,m1=month_start,m2=month_end)

        query = alchemy_text('''
ALTER TABLE '''+lookup_schema+'''.geoi_out_all ADD COLUMN month_start BIGINT;
ALTER TABLE '''+lookup_schema+'''.geoi_out_all ADD COLUMN month_end BIGINT;
ALTER TABLE '''+lookup_schema+'''.geoi_out_all ADD COLUMN type_of_violence BIGINT;
        ''')
        con.execute(query)

        query = alchemy_text('''
        UPDATE '''+lookup_schema+'''.geoi_out_all SET
  month_start=c.month_id_start,
  month_end=c.month_id_end,
  type_of_violence=c.type_of_violence
FROM '''+lookup_schema+'''.gedfull c
WHERE '''+lookup_schema+'''.geoi_out_all.id = c.id;
'''
         )
        con.execute(query)


def geoi_pgm_dummy_update(
        imputation_id=1,
        db_engine_name='postgresql://VIEWSADMIN@VIEWSHOST:5432/views',
        lookup_schema='geoimputation',
        month_start=400,
        month_end=400
):

    if not isinstance(imputation_id, (int, long)):
        print ("ERROR")
        return None

    imputation_id = str(imputation_id)

    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        trans = con.begin()
        query = alchemy_text('''UPDATE '''+lookup_schema+'''.pgm SET  
        ged_sb_dummy_'''+imputation_id+'''=0,  
        ged_ns_dummy_'''+imputation_id+'''=0,
        ged_os_dummy_'''+imputation_id+'''=0 
        WHERE month_id BETWEEN :m1 AND :m2''')
        con.execute(query,m1=month_start,m2=month_end)
        trans.commit()

        trans = con.begin()
        query = alchemy_text('''
    with a as
(
    SELECT
      "'''+imputation_id+'''" as priogrid_gid,
      type_of_violence,
      random_series_int(month_start :: INT, month_end :: INT + 1) AS month_id
    FROM  '''+lookup_schema+'''.geoi_out_all
)
UPDATE
  '''+lookup_schema+'''.pgm as i SET ged_ns_dummy_'''+imputation_id+'''=1
FROM a
WHERE a.type_of_violence=2 AND a.priogrid_gid=i.priogrid_gid AND a.month_id=i.month_id''')
        con.execute(query)


        query = alchemy_text('''
    with a as
(
    SELECT
      "'''+imputation_id+'''" as priogrid_gid,
      type_of_violence,
      random_series_int(month_start :: INT, month_end :: INT + 1) AS month_id
    FROM  '''+lookup_schema+'''.geoi_out_all
)
UPDATE
  '''+lookup_schema+'''.pgm as i SET ged_os_dummy_'''+imputation_id+'''=1
FROM a
WHERE a.type_of_violence=3 AND a.priogrid_gid=i.priogrid_gid AND a.month_id=i.month_id''')
        con.execute(query)

        query = alchemy_text('''
            with a as
        (
            SELECT
              "''' + imputation_id + '''" as priogrid_gid,
              type_of_violence,
              random_series_int(month_start :: INT, month_end :: INT + 1) AS month_id
            FROM  ''' + lookup_schema + '''.geoi_out_all
        )
        UPDATE
          ''' + lookup_schema + '''.pgm as i SET ged_sb_dummy_''' + imputation_id + '''=1
        FROM a
        WHERE a.type_of_violence=3 AND a.priogrid_gid=i.priogrid_gid AND a.month_id=i.month_id''')
        #print (query)
        con.execute(query)
        trans.commit()


if __name__ == "__main__":
    geoi_run()
