Here are the definitions of the SQL models to be run, as well as the scripts to populate the relations.

First create the model, and then populate it

REQUIREMENTS:

- UCDP GED imported via the API loader script.
- PRIOGRID STATIC imported via the API loader script.
- PRIOGRID YEARLY imported via the API loader script.
- PRIOGRID GEOGRAPHY (col,row,xcoord,ycoord,geom) imported MANUALLY since the PRIO API is broken.
- CSHAPES imported MANUALLY.

**You also need to import the helper functions in the SQL functions section before continuing**

These should  be imported before any of the creation scripts are run.

RUN THESE LIKE THIS TO POPULATE DATABASE FROM SCRATCH:

1. Starting from an empty database:
    1. Create an empty model: **create_model.sql**
    2. Populate the model with relations and basic identification data (priogrid descriptors, country descriptors). This takes VERY LONG to run (7-9 h on linus). **populate_model.sql**
2. Filling it up/updating the database:
    3. Fill up priogrid with the static values coming from priogrid: **populate_priogrid.sql**
    4. Fill up priogrid_year with the yearly values coming from priogrid: **populate_priogrid_year.sql**
    5. Fill up spatial lags for countries using: **populate_country_lags.sql**

**Don't forget that recreating the model from scratch will produce new ids and new relations, incompatible with old versions**
