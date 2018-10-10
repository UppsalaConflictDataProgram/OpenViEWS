from __future__ import print_function
from __future__ import division


import requests
import sqlalchemy
import pandas as pd 
import json
import time
import os

__author__ = "Frederick Hoyles"
__copyright__ = "(C) 2017 ViEWS, Uppsala University"
__credits__ = ["Frederick Hoyles", "Håvard Hegre"]
__license__ = "All Rights Reserved"
__version__ = "0.1"
__maintainer__ = "Frederick Hoyles"
__email__ = "frederick.hoyles@gmail.com"
__status__ = "Development"


class GetPRIO(object):
    """Populates database with data from PRIO

    Note:
        The basic structure is this:
        Downloads the data from grid.prio.org
        Stores each variable in a separate .json file
        For each var:
            read from json to pandas DataFrame
            push DataFrame to database using to_sql (slow, minutes per yearly variable)
            joins the variable tables into a temporary table, one for static and one for yearly
        When merging is complete move the joined data into tables prio_static and prio_yearly
    Args:
        read_cached=False: If True use cached versions of the grid and metadata so as not to hit API each run


    """

    def __init__(self, read_cached=False):
        print("init GetPRIO")

        #URL
        self.url_base = "http://grid.prio.org/api/"
        self.url_grid = self.url_base + "data/basegrid"
        self.url_vars = self.url_base + "variables"
        self.url_data = self.url_base + "data/"

        # DB parameters
        self.db_prefix      = "postgresql"
        self.db_db          = "views"
        self.db_uname       = "VIEWSADMIN"
        self.db_hostname    = "VIEWSHOST"
        self.db_port        = "5432"
        self.db_schema      = "dataprep"


        #self.db_prefix      = "postgresql"
        #self.db_db          = "efx"
        #self.db_uname       = "efx"
        #self.db_hostname    = "localhost"
        #self.db_port        = "5432"
        #self.db_schema      = "dataprep"


        self.dir_json = "./jsons/"
        self.path_df_grid = "df_grid.pickle"
        self.path_df_vars = "df_vars.pickle"

        self.db_connectstring = self.make_connectstring(
                                self.db_prefix,
                                self.db_db,
                                self.db_uname,
                                self.db_hostname,
                                self.db_port)

        # these are initialized in get_varinfo()
        self.start_year = None
        self.end_year = None

        # initialize GetPRIO with metadata from the API
        if read_cached:
            try:
                print("Reading cached df_grid and df_vars from ", self.path_df_grid, self.path_df_vars, end=" ... ")
                self.df_grid = pd.read_pickle(self.path_df_grid)
                self.df_vars = pd.read_pickle(self.path_df_vars)
                self.start_year = 1946
                self.end_year = 2013
                print(" [OK] ")
            except IOError:
                print("IOError on fetching cached metadata, getting from API.")
                self.get_grid(self.url_grid)
                self.get_varinfo()

        else:
            self.get_grid(self.url_grid)
            self.get_varinfo()



        # get the data, dump to file
        # self.fetch_data()
        # self.make_skeleton()

    def fetch_data(self):
        """Downloads all variables from grid.prio.org and stores in json named after the variable

        Note:
            Overwrites existing files (files are opened with 'w' parameter)
            """
        if not os.path.isdir(self.dir_json):
           os.makedirs(self.dir_json)

        def var_download(row):
            url = row['get_url']
            print("Downloading: ", url, end=" ... ")
            r = requests.get(url)
            obj = r.json()
            print(" [OK] ")

            filename = self.dir_json + str(row['name']) + ".json"
            with open(filename, 'w') as f:
                print("Dumping to", filename, end=" ... ")
                json.dump(obj,f)
                print(" [OK] ")

        self.df_vars.apply(var_download, axis=1)

    def make_connectstring(self, prefix, db, uname, hostname, port):
        """return an sql connectstring
        """
        connectstring = prefix + "://" + uname + "@" + hostname + \
                        ":" + port + "/" + db

        return connectstring

    def get_grid(self, url_grid):

        print("Getting grid from ", self.url_grid, end=" ... ")
        self.df_grid = pd.read_json(path_or_buf=self.url_grid)
        print(" [OK] ")

        print("Storing cached grid in ", self.path_df_grid, end=" ... ")
        self.df_grid.to_pickle(path=self.path_df_grid)
        print(" [OK] ")


    def get_varinfo(self):
        """Gets metadata from PRIO-GRID API and stores them in self.df_vars as at DataFrame
        """
        
        print("Getting variable list from ", self.url_vars, end=" ... ")
        self.df_vars = pd.read_json(path_or_buf=self.url_vars)
        
        # These throw API errors so exclude them
        self.excludelist = ["gid", "row", "col", "xcoord", "ycoord"]
        # ~ inverts selection: this selects all variables except the excluded
        self.df_vars = self.df_vars[~self.df_vars['name'].isin(self.excludelist)]

        # We need startYear and endYear to make the API-calls
        # static vars are given year=0 by PRIO
        self.start_year = self.df_vars['startYear'][self.df_vars['startYear']>0].min()
        self.end_year = self.df_vars['endYear'].max()

        def url_constructor(row):
            """"Construct the URLs for retrieving each variable.
            Example: http://grid.prio.org/api/data/94?startYear=1946&endYear=2014
            """
            if row['type']=="yearly":
                start = row['startYear']
                end = row['endYear']

                year_range = "?startYear=" + str(start) + \
                             "&endYear=" + str(end)

                get_url = self.url_data + str(row['id']) + year_range
            elif row['type']=="static":
                get_url = self.url_data + str(row['id'])
            return get_url

        def path_constructor(row):
            filename = self.dir_json + str(row['name']) + ".json"
            return filename

        self.df_vars['get_url']  = self.df_vars.apply(url_constructor, axis=1)
        self.df_vars['filepath'] = self.df_vars.apply(path_constructor, axis=1)
        print (" [OK] ")

        print("Storing cached variable lists in ", self.path_df_vars, end= " ... ")
        self.df_vars.to_pickle(path = self.path_df_vars)
        print(" [OK] ")
        
    def summarize(self):
        print("Vars cols")
        print(self.df_vars.columns)
        print("Vars head")
        print(self.df_vars['name'].head())
        print("Grid head")
        print(self.df_grid.head())
        print("connectstring: ",  self.db_connectstring)

        print("url_base:", self.url_base)
        print("url_grid:", self.url_grid)
        print("url_vars:", self.url_vars)
        print("url_data:", self.url_data)

        # print(self.df_vars[['id', 'name', 'get_url', 'filepath']])

    def json_to_df(self, varname, filepath):
        with open(filepath, 'r') as json_data:
            data = json.load(json_data)
        df = pd.DataFrame.from_dict(data['cells'])
        df.rename(columns={'value' : varname}, inplace = True)

        print("loaded ", varname, " from ", filepath, " with ", len(df), " rows")
        #print(df.head(1))
        return df

    def df_to_db(self, df, table, verbose=False):
        connectstring = self.make_connectstring(self.db_prefix, self.db_db, 
                                                self.db_uname, self.db_hostname, 
                                                self.db_port)
        print("Connecting to ", connectstring, end=" ... ")
        engine = sqlalchemy.create_engine(connectstring)
        print(" [OK] ")

        print("Pushing df to table ", table, end = " ... ")
        t1 = time.time()
        df.to_sql(name=table, con=engine, if_exists="replace", schema=self.db_schema, index=False)
        t2 = time.time() - t1
        print(" [OK] Runtime: ", str(t2))

    def grid_to_db(self):
        print("Pushing static grid to db")
        self.df_to_db(self.df_grid, 'grid')

    def grid_year_to_db(self):
        print("Pushing yearly grid to db")
        self.df_to_db(self.df_grid_year, 'grid_year')


    def left_join_tables(self, merged, left, right, on):
        t1 = time.time()
        self.drop_table(merged)
        engine = sqlalchemy.create_engine(self.db_connectstring)

        merged = self.db_schema + "." + merged
        left = self.db_schema + "." + left
        right = self.db_schema + "." + right

        with engine.connect() as con:
            query_merge = ("CREATE TABLE " + merged + " AS SELECT * FROM " + left + " LEFT JOIN " + right + " USING(" + on + ")")
            print(query_merge)
            con.execute(query_merge)
        t2 = time.time() - t1
        print("Query runtime: ", str(t2))


    def drop_table(self, drop):
        engine = sqlalchemy.create_engine(self.db_connectstring)
        drop = self.db_schema + "." + drop
        with engine.connect() as con:
            query_drop = ("DROP TABLE IF EXISTS " + drop)
            print(query_drop)
            con.execute(query_drop)

    def rename_table(self, oldname, newname):
        engine = sqlalchemy.create_engine(self.db_connectstring)

        oldname = self.db_schema + "." + oldname
        #newname = self.db_schema + "." + newname

        with engine.connect() as con:
            query_drop = ("ALTER TABLE " + oldname + " RENAME TO " + newname)
            print(query_drop)
            con.execute(query_drop)

    def make_grid_year(self):
        """Makes self.df_grid_year containing a skeleton dataframe with rows for each grid-year combination"""
        print(" Constructing grid-year skeleton df", end = " ... ")
        yearlist = list(range(self.start_year, (self.end_year + 1)))
        self.df_grid_year = pd.DataFrame(columns=['year', 'gid'])

        for year in yearlist:
            df = self.df_grid.copy()
            df['year'] = year
            self.df_grid_year = self.df_grid_year.append(df)

        print(" [OK] ")
        print(str(len(self.df_grid_year)), " rows in df_grid_year")

    def static_to_db(self):
        """Pushes all static variables to the database table prio_static

         Note:
            Loop over all the static variables
            Read the data from the stored json (from fetch_data())
            Push the data to table staticvar
            On the first staticvar join the staticvar with the scaffold grid table into table a.
            Then push a new staticvar and join that with table a and store result in table b.
            Then push a new staticvar and join that with b into a, overwriting a.
            Repeat until all static variables are in the database in tables a or b.
            Rename the last a or b to prio_static, drop the second last one

        """
        print("\n")
        print("###########################################")
        print("# Starting pushing static variables to DB #")

        #select only the static variables
        df_vars_static = self.df_vars[self.df_vars['type']=="static"]

        # start joining with grid table as scaffolding
        previous = "grid"
        # a is the first table to merge into.
        merged = "a"

        for i,row in df_vars_static.iterrows():
            print("##############################################################################################")
            name = row['name']
            filepath = row['filepath']
            print(name, filepath)
            df = self.json_to_df(varname = name, filepath = filepath)
            df = df[['gid', name]]

            # push this static var to db table staticvar
            self.df_to_db(df, 'staticvar')
            # drop if exists and create new table merged that is left join of previous merged table and new staticvar
            self.left_join_tables(merged=merged, left=previous, right ='staticvar', on='gid')

            # set
            previous = merged
            # switch the merged output table before next variable
            if merged == "a":
                merged = "b"
            else:
                merged = "a"

        # note that merged here is simply not the previous
        self.drop_table(drop = merged)
        self.drop_table(drop = 'staticvar')

        # rename the big joined table to prio_static
        self.drop_table(drop='prio_static')
        self.drop_table(drop='grid')
        self.rename_table(oldname = previous, newname='prio_static')

        print("All static variables from PRIO now in table prio_static")

    def yearly_to_db(self):
        """Pushes all yearly variables to the database table prio_yearly"""
        print("\n")
        print("###########################################")
        print("# Starting pushing yearly variables to DB #")

        #for the first join use the skeleton as left
        previous = "grid_year"
        # start joining into column a
        merged = "a"

        df_vars_yearly = self.df_vars[self.df_vars['type']=="yearly"]
        for i, row in df_vars_yearly.iterrows():
            print("##############################################################################################")
            name = row['name']
            filepath = row['filepath']
            #print(name, filepath)
            df = self.json_to_df(varname = name, filepath = filepath)
            df = df[['gid', 'year', name]]
            self.df_to_db(df=df, table='yearlyvar')
            self.left_join_tables(merged=merged, left=previous, right='yearlyvar', on="gid, year")

            #
            previous = merged
            # switch the merged output table before next variable
            if merged == "a":
                merged = "b"
            else:
                merged = "a"

        # note that "merged" here is simply not the previous
        self.drop_table(drop=merged)
        self.drop_table(drop='yearlyvar')

        # rename the big joined table to prio_static
        self.drop_table(drop='prio_yearly')
        self.drop_table(drop='grid_year')
        self.rename_table(oldname=previous, newname='prio_yearly')

        print("All static variables from PRIO now in table prio_yearly")

    def xy_to_db(self):
        df_xy = pd.read_csv('gid_x_y.csv', sep=",")
        self.df_to_db(df_xy, table="gid_xy")
        engine = sqlalchemy.create_engine(self.db_connectstring)
        with engine.connect() as con:
            query = "ALTER TABLE prio_static ADD COLUMN xcoord DOUBLE PRECISION"
            print(query)
            con.execute(query)
            query = "ALTER TABLE prio_static ADD COLUMN ycoord DOUBLE PRECISION"
            print(query)
            con.execute(query)









def main():
    foo = GetPRIO()
    # foo.fetch_data()
    foo.grid_to_db()
    foo.make_grid_year()
    foo.grid_year_to_db()
    foo.static_to_db()
    foo.yearly_to_db()

if __name__ == "__main__":
    main()

