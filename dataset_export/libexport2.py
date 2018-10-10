import pandas as pd
import numpy as np
import json
import sqlalchemy
from sqlalchemy import create_engine,text
import os

# Read JSON and explode it.
# Take JSO


def IntrospectMatchingColumns(db_engine_name = 'postgresql://test@test:5432/views',
                              schema_a =  'staging',
                              schema_b = 'staging',
                              table_a = 'priogrid_year',
                              table_b = 'priogrid_month',
                              exclude_columns=('id')
                              ):
    engine = create_engine(db_engine_name)
    with engine.connect() as con:
        query = text("""
with
    a AS
(
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = :schema_a
          AND table_name = :table_a
),
   b AS
(
      SELECT column_name
      FROM information_schema.columns
      WHERE table_schema = :schema_b
            AND table_name = :table_b
)
SELECT a.column_name FROM a, b WHERE a.column_name = b.column_name""")
        result = con.execute(query, schema_a=schema_a, schema_b=schema_b, table_a=table_a, table_b=table_b).fetchall()
        output = [r[0] for r in result if r[0] not in exclude_columns]

        if len(output) == 0:
            print (output, schema_a, schema_b, table_a, table_b)
            raise ValueError("No columns to join on in the two tables")

        return (output)
#Takes a JSON file and creates the

class Dataset:

    def __init__(self, query_or_table, db_engine_name = 'postgresql://test@test:5432/views'):

        try:
            if ' ' not in query_or_table:
                query_or_table = 'SELECT * FROM '+query_or_table
        except TypeError as errinst:
            if isinstance(query_or_table,sqlalchemy.sql.elements.TextClause):
                pass
            else:
                raise TypeError ('You have not supplied either a table, a string query or an SQLAlchemy query. Will not proceed!')

        engine = create_engine(db_engine_name)
        with engine.connect() as con:
            self.content = pd.read_sql(sql=query_or_table,con=con)

    def head(self, n=10):
        return self.content.head(n=n)

    def as_pandas(self):
        return self.content

    def add_calendar_months(self):
        if self.content is None:
            self.content=None
        if 'month_id' in self.content:
            out = self.content
            out['month_id'] = out['month_id'].astype(int)
            out['month'] = (out['month_id'] % 12).astype(int)
            out.loc[out.month == 0, 'month'] = 12
            out['year'] = (np.floor(out['month_id'] / 12) + 1980).astype(int)
            self.content=out

    def save(self, directory, filename, format = 'csv', compression = None):
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = directory + '/' + filename
        if format=='csv':
            self.content.to_csv(path, compression=compression,index=False)
            return True
        if format=='pickle':
            self.content.to_pickle(path)
            return True
        if format=='hdf':
            self.content.to_hdf(path,key='base',index=False)
            return True


class Predictions:
    def __init__(self, level = 'pgm', level_var = 'pg_id', run = 'fcast', outcome='sb',
                 component_prefix = 'calibrated', ensemble_prefix = 'ensemble', schema = 'landed',
                 db_engine = 'postgresql://test@test:5432/views', verbose = True):
        self.level = level
        self.run = run
        self.outcome = outcome
        self.parse = self.__fetch_ensemble_definition()
        self.ensemble_schema = schema
        self.component_schema = schema
        self.ensemble_table = ensemble_prefix+'_'+level+'_'+run+'_test'
        self.compoent_table = component_prefix+'_'+level+'_'+run+'_test'
        self.db_engine_name = db_engine
        self.level_var = level_var
        self.actuals = False
        self.verbose=verbose

    def __verbose_print(self, content):
        if self.verbose:
            print(content)

    def __fetch_ensemble_definition (self):
        ensemble_file_name = f'../ensemble/ensembles_{self.level}.json'
        with open(ensemble_file_name,'r') as ensemble_file:
            content = ensemble_file.read()
            content = content.replace('RUNTYPE',self.run.lower().strip())
            content = content.replace('OUTCOME',self.outcome.lower().strip())
            self.json_repr = content
            return (json.loads(content))

    def metadata (self, asJson=True):
        if asJson:
            return self.json_repr
        else:
            repr = "*" * 48 + '\n'
            repr += 'Ensemble\n'
            repr += "*" * 48 + '\n'
            for ensemble in self.parse:
                repr += '\n' + ensemble + '\n'
                for element in self.parse[ensemble]:
                    repr += '  |- ' + element + '\n'
            return repr

    def list_constituents(self, ensemble):
        return self.parse[ensemble]

    def list_ensembles(self):
        ensembles = [ensemble for ensemble in self.parse]
        return (ensembles)

    def hook_actuals(self, schema = 'launched', table = 'transforms_pgm_imp_1', column_name = 'ged_dummy_OUTCOME'):
        self.actuals_column_name = column_name.replace('OUTCOME',self.outcome)
        self.actuals_table_path = schema+"."+table
        self.actuals_table_path = self.actuals_table_path.strip(". ")
        self.actuals = True

    def temporal_extent(self):
        query = f"SELECT min(month_id) as min, max(month_id) as max FROM {self.ensemble_schema}.{self.ensemble_table}"
        extent = Dataset(query,db_engine_name=self.db_engine_name).as_pandas()
        return int(extent['min'][0]),int(extent['max'][0])

    def fetch_dataset(self,ensemble):
        #Introspect the columns to merge the two tables on. Ignore the id column
        match_on = IntrospectMatchingColumns(db_engine_name=self.db_engine_name,
                                             schema_a=self.component_schema,
                                             table_a=self.compoent_table,
                                             schema_b=self.ensemble_schema,
                                             table_b=self.ensemble_table,
                                             )
        #Get the components of the ensemble
        components = self.list_constituents (ensemble)

        #Create a merging query
        query = f"SELECT et.month_id, et.{self.level_var}, et.{ensemble}, "
        query += 'cp.'+', cp.'.join(components)
        query += f" FROM {self.ensemble_schema}.{self.ensemble_table} as et, " \
                 f"{self.component_schema}.{self.compoent_table} as cp WHERE "
        query += ' AND '.join([f"cp.{i}=et.{i}" for i in match_on])

        if self.actuals:
            actual_column = 'ged_sb'
            query  = f"WITH a as ( " + query
            query += f") SELECT a.*, b.{self.actuals_column_name} as actuals " \
                    f" FROM a LEFT JOIN {self.actuals_table_path} b " \
                    f" USING (month_id, {self.level_var})"
            #print (query)

        #query += f" cp.month_id = et.month_id AND cp.{self.level_var}=et.{self.level_var}"
        return Dataset(query,db_engine_name=self.db_engine_name)

    def save_one(self, ensemble, directory, format='csv'):
        self.__verbose_print(ensemble)
        dataset = self.fetch_dataset(ensemble)
        dataset.add_calendar_months()
        filename = ensemble + '.' + format
        dataset.save(directory, filename, format=format)

    def save_bulk(self,format='csv', directory='.'):
        ensembles = self.list_ensembles()
        for ensemble in ensembles:
            self.__verbose_print(ensemble)
            dataset = self.fetch_dataset(ensemble)
            dataset.add_calendar_months()
            filename = ensemble+'.'+format
            dataset.save(directory, filename, format=format)


    def __repr__(self):
        return self.metadata(asJson=False)

if __name__ == "__main__":
    print ("Not available from here. Use import libexport2 as ex to import the content")