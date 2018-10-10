import sys

import pandas as pd

sys.path.insert(0, "../..")

from views_utils.dbutils import make_connectstring, df_to_db

prefix = "postgres"
db = "views"
uname = "VIEWSADMIN"
hostname = "VIEWSHOST"
port = "5432"
connectstring = make_connectstring(prefix, db, uname, hostname, port)

loas = ["pgm", "cm"]

schema = "launched"
if_exists = "replace"
for loa in loas:
    for imp in range(1,6):
        table = loa + "_imp_ds_" + str(imp)
        path_input = "/storage/runs/current/ds/results/"
        path_input += loa +"_transforms/" + loa + "_imp_" + str(imp) + ".hdf5"
        print(schema, table)
        print(path_input)
        #df = pd.read_hdf(path_input)
        #df_to_db(connectstring, df, schema, table, if_exists, write_index=True)
