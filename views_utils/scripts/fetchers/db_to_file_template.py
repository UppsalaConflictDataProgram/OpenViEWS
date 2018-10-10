import sys
sys.path.append("../..")
import dbutils


uname = "YOUR USERNAME"
schema = "SCHEMA"
table = "TABLE"


columns_example = ["pg_id", "month_id", "ged_dummy_sb"]
# Leave empty to get all cols from table or replace with your list
columns = []

connectstring = dbutils.make_connectstring(db="views", hostname="VIEWSHOST", 
    port="5432", prefix="postgres",uname=uname)

df = dbutils.db_to_df(connectstring, schema, table, columns)

df.to_csv("my_table.csv")
df.to_stata("my_table.dta")