
""" Writes the result of an SQL Select query, contained in an .sql file, to disk

This module lets the user specify the location of a .sql file containing a 
SELECT query and writes the returned data from that query to a data file, in 
either .csv or .hdf5 format. 
The output file is named after the query file.
It operates through the query_to_file() function, which reads chunkwise to
temporary .hdf5 files.
Memory usage is low throughout the download but peaks a short time at the end
when all the data is concatenated into a single frame.

Example:
    python --path_query ../SQLSelects/imp_imp_1.sql 
    --dir_data /home/VIEWSADMIN/data/ --uname VIEWSADMIN --fformat hdf5 --verbose

Args:
    path_query: path to query file, must be valid SQL
    dir_data: directory to store resulting file in
    uname: username to connect to db as, must have valid certificates installed
    fformat: must be "hdf5" or "csv", sets the type of outputfile
    verbose: True if included, otherwise false. If True each chunk printed

Returns:
    None

Outputs:
    outputfile: /path/to/dir_data/name_of_query_file.(csv/hdf5)

Todo: 
    


"""
from __future__ import print_function

import pandas as pd 
import sqlalchemy
import time
import argparse
import sys

from dbutils import make_connectstring, query_to_file

from varlists import varlist_pgm, varlist_cm, varlist_act


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_query", type=str,
        help="path to .sql query file to get", required=True)
    parser.add_argument("--dir_data", type=str,
        help="directory to store data", required=True)
    parser.add_argument("--uname", type=str,
        help="username for db connection", required=True)
    parser.add_argument("--fformat", type=str,
        help="format of outputfile, can be hdf5 or csv", required=True)
    parser.add_argument('--verbose', action='store_true')

    args = parser.parse_args()

    path_query = args.path_query
    dir_data    = args.dir_data
    uname       = args.uname
    fformat     = args.fformat
    verbose     = args.verbose

    # make sure it ends in /
    if not dir_data[-1] == "/":
        dir_data += "/"

    assert fformat in ["csv", "hdf5"], "The only supported fformats are csv and hdf5"

    return path_query, dir_data, uname, fformat, verbose

def main():
    path_query, dir_data, uname, fformat, verbose = parse_args()

    prefix = "postgresql"
    db = "views"
    port = "5432"
    hostname = "VIEWSHOST"

    connectstring = make_connectstring(prefix, db, uname, hostname, port)
    query_to_file(connectstring, path_query, dir_data, fformat, verbose)

if __name__ == "__main__":
    main()
