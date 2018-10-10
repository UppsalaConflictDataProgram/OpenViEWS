# For visualistion some variables need to be scaled to 0-1
import numpy as np
import os
import sys

sys.path.append("..")

import views_utils.dbutils as dbutils

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
                                           port="5432", prefix="postgres",
                                           uname="VIEWSADMIN")

def scale_to_range(x, min_new, max_new, reverse=False):
  """Rescale x to new max and min"""
  if reverse:
    x = -x

  max_old = np.max(x)
  min_old = np.min(x)

  # scaling factor
  k = (max_new - min_new) / (max_old - min_old)
  x_scaled = k*(x-max_old) + max_new

  return x_scaled

rescales = [
    {
        "opts": {
            "reverse": False,
            "max_new": 1,
            "min_new": 0
        },
        "name": "ln_pop"
    },
    {
        "opts": {
            "reverse": False,
            "max_new": 1,
            "min_new": 0
        },
        "name": "ln_capdist"
    },
    {
        "opts": {
            "reverse": True,
            "max_new": 1,
            "min_new": 0
        },
        "name": "ln_bdist3"
    }
]

timevar = "month_id"
groupvar = "pg_id"
schema_input = "launched"
table_input = "transforms_pgm_imp_1"
schema_output = "landed"
table_output = "rescaled_pgm"


ids = [timevar, groupvar]
vars_to_rescale = [var['name'] for var in rescales]
vars_rescaled = []
cols = ids + vars_to_rescale


df = dbutils.db_to_df(connectstring, schema_input, table_input, columns=cols, ids=ids)

for rescale in rescales:
    name_new = rescale['name'] + "_rescaled"
    vars_rescaled.append(name_new)
    rescale['opts'].update({'x' : df[rescale['name']]})

    df[name_new] = scale_to_range(**rescale['opts'])

df = df[vars_rescaled]

dbutils.df_to_db(connectstring, df, schema_output, table_output, 
                if_exists="replace", write_index=True)

