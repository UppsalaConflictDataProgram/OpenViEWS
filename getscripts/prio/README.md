#get-priogrid

Small fetcher script for data from PRIO-GRID (http://grid.prio.org/).
Populates the schema dataprep in the database with two tables: prio_static and prio_yearly. 
Works fully but isn't beautiful.
Runtime is over 2h because of how the data is inserted to the database.

TODO:
* Rewrite to use proper base/scartch joining algo for the input.
* Rewrite static_to_db() and yearly_to_db() as one function with different parameters.
* General cleanup.

By Frederick
