"""dbutils provides a set of wrapper functions for interacting between pandas 
DataFrame's and the ViEWS DB"""

from __future__ import print_function
from __future__ import division

import os

import tempfile
from textwrap import dedent

import pandas as pd
import sqlalchemy
import time
import psycopg2
import numpy as np


__author__ = "Frederick Hoyles"
__copyright__ = "(C) 2017 ViEWS, Uppsala University"
__credits__ = ["Frederick Hoyles", "Haavard Hegre"]
__license__ = "All Rights Reserved"
__version__ = "0.1"
__maintainer__ = "Frederick Hoyles"
__email__ = "frederick.hoyles@gmail.com"
__status__ = "Development"


class bcolors:
    """fancy colors for printing OK in green, very important"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def make_connectstring(prefix, db, uname, hostname, port):
    """return an sql connectstring"""
    connectstring = prefix + "://" + uname + "@" + hostname + \
                    ":" + port + "/" + db
    return connectstring

def df_to_db(connectstring, df, schema, table, if_exists, write_index=False):
    """Pushes a pandas dataframe to the specified database table using pandas to_sql method
    Args:
        connectstring:
        df:
        schema:
        table:
        if_exists: 'fail', 'replace', 'append'
        write_index:
    Returns:
        None
    """

    def sqlcol(dfparam):
        """Matches pandas datatypes to their sqlalchemy equivalents, returns the mapping as a dict"""
        dtypedict = {}
        for i, j in zip(dfparam.columns, dfparam.dtypes):
            if "object" in str(j):
                dtypedict.update({i: sqlalchemy.types.VARCHAR(length=255)})

            if "datetime" in str(j):
                dtypedict.update({i: sqlalchemy.types.DateTime()})

            # Underflow errors can happen when precision is set
            if "float" in str(j):
                #dtypedict.update({i: sqlalchemy.types.Float(precision=3, asdecimal=True)})
                dtypedict.update({i: sqlalchemy.types.Float(asdecimal=True)})

            if "int" in str(j):
                dtypedict.update({i: sqlalchemy.types.INT()})

        return dtypedict

    typedict = sqlcol(df)

    engine = sqlalchemy.create_engine(connectstring, connect_args=make_ssl_args())
    t1 = time.time()
    schema_table = schema+"."+table
    print("Pushing", str(len(df)), "rows to", schema_table)
    df.to_sql(name=table, con=engine, if_exists=if_exists, schema=schema, 
        index=write_index, dtype=typedict, chunksize=10000)
    t2 = time.time() - t1
    rows = len(df)
    rps = rows/t2
    print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)
    print("runtime: ", str(t2), "rows/second: ", str(rps))

def drop_table(connectstring, schema, table):
    """Drops a table in the database"""
    print("Connecting to ", connectstring,  "using sqlalchemy", end=" ... ")
    engine = sqlalchemy.create_engine(connectstring)
    print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)
    schema_name = schema + "." + table
    with engine.connect() as con:
        query = ("DROP TABLE IF EXISTS " + schema_name)
        print(query)
        con.execute(query)

def get_tables_schema(connectstring, schema):
    print("Connecting to ", connectstring, "using psycopg2", end=" ... ")
    conn = psycopg2.connect(connectstring)
    cursor = conn.cursor()
    print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)
    query = """SELECT table_name FROM information_schema.tables
       WHERE table_schema = '{}'""".format(schema)
    cursor.execute(query)
    tables = []
    for table in cursor.fetchall():
        tables.append(table[0])
    return tables

def copy_df_to_db(connectstring, df, schema, table, if_exists, write_index=False, chunksize = 4096):
    """Uses a cStringIO buffer and psycopg2's copy_from command to push large dataframes to a db table
    Args:
        connectstring:
        df:
        schema:
        table:
        if_exists: 'replace' or 'append'
        write_index:
        chunksize: number of rows to write simulatenously, default 4096
    Returns:
        None
    Note:
        The procedure is as follows:
        First the empty table is created (overwritten) with the columns inferred from the dataframe using df_to_db()
        Then the df is split into chunks using numpy array_split
        The chunks are iterated over and written to a .csv in a buffer in memory using cStringIO
        psycopg2 reads each .csv from the buffer and pushes to the database using copy_from
    """
    from cStringIO import StringIO

    t1 = time.time()

    schema_table = schema+"."+table

    # Create (overwrite) the table in the db with the columns from df
    if if_exists=='replace':
        # df_empty now contains all columns of df with the correct types but no rows
        df_empty = df[np.full((len(df)), False, dtype=bool)]
        df_to_db(connectstring, df_empty, schema, table, 'replace', write_index=write_index)

    # Create our cursor
    print("Connecting to ", connectstring, "using psycopg2", end=" ... ")
    conn = psycopg2.connect(connectstring)
    curs = conn.cursor()
    print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)

    # Open a cStringIO buffer (in memory)
    s_buf = StringIO()

    # Set the number of rows in each chunk. This can probably be optimized by taking columns into consideration too
    rows = len(df)
    splits = int(rows / chunksize)

    chunk_counter = 1
    # Split the df into chunks and start looping
    for chunk in np.array_split(df, splits):
        t1_chunk = time.time()

        print("Writing chunk ", str(chunk_counter), "/", str(splits), "of length:", str(len(chunk)), end = " ... ")

        # Treat the stringIO buffer as a file and use pandas write_csv
        chunk.to_csv(s_buf, index=write_index, header=False, na_rep="NULL")

        # "Rewind" the buffer to the start
        s_buf.seek(0)

        # Write the csv contents of the buffer to the db using COPY
        curs.copy_from(s_buf, schema_table, sep=',', null="NULL")

        # Not sure if needed
        conn.commit()


        t2_chunk = time.time() - t1_chunk
        print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC + "chunktime: " + str(t2_chunk))
        chunk_counter += 1

        # Empty the buffer
        s_buf.truncate(0)

    # How fast did we go?
    t2 = time.time() - t1
    rps = rows/t2
    print("Runtime: ", str(t2), "rows: ", rows, "rows/seconds: ", rps)

def db_to_df(connectstring, schema, table, columns=None, ids=None, verbose=False):
    """Read a column from the database and return as pandas DataFrame"""
    t1 = time.time()

    # if we have ids supplied then add them to the list of cols to get
    if columns and ids:
        columns = columns + ids

    if verbose:
        print("Connecting to", connectstring,  "using sqlalchemy", end=" ... ")

    engine = sqlalchemy.create_engine(connectstring, connect_args=make_ssl_args())    
    if verbose:
        print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)
    if columns:
        if verbose:
            print("Getting " + str(len(columns)) + " cols from ", schema+"."+ table, " from ", connectstring, end= " ... ")        
    else:
        if verbose:
            print("Getting table ", schema+"."+ table, " from ", connectstring, end= " ... ")

    df = pd.read_sql_table(table_name=table, con=engine, schema=schema, columns = columns)

    t2 = time.time() - t1
    rows = len(df)
    rps = rows/t2
    if verbose:
        print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)
    if verbose:
        print("runtime: ", str(t2), "rows: ", rows, "rows/seconds: ", rps)

    if ids:
        df.set_index(ids, inplace=True)

    return df

def db_run_queries_from_file(connectstring, path):
    """Read ; sql queries from file at path"""
    with psycopg2.connect(connectstring) as conn:
        cur = conn.cursor()

        with open(path, 'r') as fd:
            sql_file_contents = fd.read()

        # all SQL commands (split on ';')
        sql_commands = sql_file_contents.split(';')
        # @TODO: proper sql command from file parser
        # assuming the last command in a file is ended with a ; the split will make an empty entry 
        # in the last element of the list, so we delete it. Hacky :(
        del sql_commands[-1]

        # Execute every command from the input file
        for command in sql_commands:
            print(command)
            cur.execute(command)

def db_to_file(connectstring, schema, table, columns, dir_data, fformat, verbose=False):
    engine = sqlalchemy.create_engine(connectstring, server_side_cursors=True)    

    name_table = ".".join([schema, table])
    print("Getting ", name_table, "this might take a while...")

    # get the data to temp chunk filese
    i = 0
    paths_chunks = []
    with tempfile.TemporaryDirectory() as td:
        for df in pd.read_sql_table(table, engine, schema, columns=columns, 
            chunksize = 100000):
            path = td + "/chunk" + str(i) + ".hdf5"
            df.to_hdf(path, key='data')
            if verbose:
                print("wrote", path)
            paths_chunks.append(path)
            i+=1

        print("finished getting data to tempfiles, merging...")
        dfs = []
        for path in paths_chunks:
            df = pd.read_hdf(path)
            dfs.append(df)
            if verbose:
                print("read", path)

    df = pd.concat(dfs)

    if "csv" in fformat:
        path = dir_data+name_table+".csv"
        df.to_csv(path)
    elif "hdf5" in fformat:
         path = dir_data+name_table+".hdf5"
         df.to_hdf(path, key='data')
    else:
        print("I don't recognise the fformat ", fformat)
        raise NotImplementedError

    print("wrote", path)
    return path
    
def query_to_file(connectstring, path_query, dir_data, fformat, verbose=False):
    engine = sqlalchemy.create_engine(connectstring, server_side_cursors=True)    

    with open(path_query, mode='r') as q:
        query=q.read()
        print("read query from", path_query)

    fname_query = path_query.strip(".sql").split("/")[-1]        
    print("Getting", fname_query, "this might take a while...")

    # get the data to temp chunk filese
    i = 0
    paths_chunks = []
    with tempfile.TemporaryDirectory() as td:
        for df in pd.read_sql_query(sql=query, con=engine, chunksize=100000):
            path = td + "/chunk" + str(i) + ".hdf5"
            df.to_hdf(path, key='data')
            if verbose:
                print("wrote", path)
            paths_chunks.append(path)
            i+=1

        print("finished getting data to tempfiles, merging...")
        df = pd.DataFrame()
        for path in paths_chunks:
            df_scratch = pd.read_hdf(path)
            df = pd.concat([df, df_scratch])
            if verbose:
                print("read", path)

    if "csv" in fformat:
        path = dir_data+fname_query+".csv"
        df.to_csv(path)
    elif "hdf5" in fformat:
         path = dir_data+fname_query+".hdf5"
         df.to_hdf(path, key='data', complevel=1, compib='zlib')
    else:
        print("I don't recognise the fformat ", fformat)
        raise NotImplementedError

    print("wrote", path)
    return path
    
def query_to_df(connectstring, query, verbose=False, chunksize=100000):
    """ Return DataFrame from SELECT query and connectstring

    Given a valid SQL SELECT query and a connectstring, return a Pandas 
    DataFrame with the response data.

    Args:
        connectstring: string with connection parameters
        query: Valid SQL, containing a SELECT query
        verbose: prints chunk progress if True. Default False.
        chunksize: Number of lines to read per chunk. Default 100000

    Returns:
        df: A Pandas DataFrame containing the response of query


    """
    
    engine = sqlalchemy.create_engine(connectstring, 
        server_side_cursors=True,
        connect_args=make_ssl_args())    
    
    # get the data to temp chunk filese
    i = 0
    paths_chunks = []
    with tempfile.TemporaryDirectory() as td:
        for df in pd.read_sql_query(sql=query, con=engine, chunksize=chunksize):
            path = td + "/chunk" + str(i) + ".hdf5"
            df.to_hdf(path, key='data')
            if verbose:
                print("wrote", path)
            paths_chunks.append(path)
            i+=1

        # Merge the chunks using concat, the most efficient way AFAIK
        df = pd.DataFrame()
        for path in paths_chunks:
            df_scratch = pd.read_hdf(path)
            df = pd.concat([df, df_scratch])
            if verbose:
                print("read", path)
    
    return df

def df_to_file(df, path, fformat, verbose=False):
    """ Writes a Pandas DataFrame to file, either .csv or .hdf5

    Args:
        df: A Pandas DataFrame to write
        path: Where to write the file
        fformat: Either csv or hdf5
    
    Returns:
        None

    """
    
    if "csv" in fformat:
        df.to_csv(path)
    elif "hdf5" in fformat:
        df.to_hdf(path, key='data', complevel=1, compib='zlib')
    else:
        raise NotImplementedError("I don't recognise the fformat ", fformat)
    if verbose:
        print("Wrote", path)

def db_to_df_limited(connectstring, schema, table, columns, timevar, groupvar, tmin, tmax):
    
    t1 = time.time()

    if not timevar in columns:
        columns.append(timevar)
    if not groupvar in columns:
        columns.append(groupvar)


    print("Getting {} cols from {}.{}".format(
        str(len(columns)), schema, table), end=" ... ")

    query = make_select_limited(
        schema=schema, 
        table=table, 
        columns=columns, 
        timevar=timevar, 
        tmin=tmin, 
        tmax=tmax)
    df = query_to_df(connectstring, query)

    t2 = time.time() - t1
    rows = len(df)
    rps = rows/t2
    print(bcolors.OKGREEN + " [OK] " + bcolors.ENDC)
    print("runtime: ", str(t2), "rows: ", rows, "rows/seconds: ", rps)


    df.set_index([timevar, groupvar], inplace=True)
    df.sort_index(inplace=True)

    return df

def make_ssl_args():
    """ Make a dictionary of connection arguments to pass to 
    sqlalchemy create_engine as keyword argument connect_args for connecting 
    to postgres from Rackham.
    Assumes certificate files are in ~/.postgres/
    
    Example:
        ssl_args = make_ssl_args()
        engine = sqlalchemy.create_engine(connectstring, connect_args=ssl_args)    

    Args:

    Returns:
        ssl_args: connect_args compatible with sqlalchemy"""

    dir_certs = os.path.expanduser('~/.postgres/')

    cert = dir_certs + "postgresql.crt"
    key = dir_certs + "postgresql.key"
    rootcert = dir_certs + "root.crt"

    ssl_args = {'sslmode'     : 'require',
                'sslcert'     : cert,
                'sslkey'      : key,
                'sslrootcert' : rootcert}

    return ssl_args

def file_to_df(path_input):
    supported_filetypes = [".csv", ".hdf5", ".dta"]
    message = "the input file specified must be one the following types", supported_filetypes
    extension = os.path.splitext(path_input)[-1]
    assert extension in supported_filetypes, message
    print("Reading", path_input, " ... ")
    if path_input.endswith(".csv"):
        df = pd.read_csv(path_input)
    elif path_input.endswith(".hdf5"):
        df = pd.read_hdf(path_input)
    elif path_input.endswith(".dta"):
        df = pd.read_stata(path_input)
    else:
        message = "The file " +  path_input + " didn't have a recognised file type"
        raise NotImplementedError(message)
    print("read ", len(df), " lines from ", path_input)

    return df

def get_colnames_table(connectstring, schema, table):
    q = "SELECT * FROM {schema}.{table} LIMIT 1;".format(
        schema = schema, 
        table=table)
    df = query_to_df(connectstring, q)
    cols = list(df.columns)

    return cols

def make_select_limited(schema, table, columns, timevar, tmin, tmax):
    columns = list(set(columns))
    schema_table = ".".join([schema, table])
    limits = """
    {timevar} >= {tmin} 
    AND 
    {timevar} <= {tmax}""".format(timevar=timevar, tmin=tmin, tmax=tmax)
    limits = limits.strip()
    cols = [col+"," for col in columns]
    cols[-1] = cols[-1].strip(",")
    cols = "\n    ".join(cols)
    select = """
    SELECT 
    {cols} 
    FROM 
    {schema_table} 
    WHERE 
    {limits};""".format(cols=cols, 
        schema_table=schema_table, 
        limits=limits)
    select = dedent(select)
    return select

