

def make_queries_add_column(varlist, schema, table):
    st = schema + "." + table
    varlist_names = [var['name_db'] for var in varlist]
    query = ""
    for var in varlist_names:
        query += "ALTER TABLE " + st + " ADD COLUMN  " + var + " FLOAT;\n"
    return query



def make_query_update(varlist):
    query = """
WITH a AS
(
    SELECT
      staging.country_year.id,
      staging.country_year.year_id,
      staging.country_year.country_id,
      staging.country.gwcode
    FROM staging.country_year
      LEFT JOIN staging.country
        ON staging.country_year.country_id = staging.country.id
),
b AS (
  SELECT 
    """

    for var in varlist:
        query += var['name_masterdata'] + " AS " + var['name_db'] + ",\n"
    query += "a.country_id,\n"
    query += "a.year_id"

    query += """
FROM dataprep.fovp, a
WHERE
(a.year_id = dataprep.fovp.year AND a.gwcode = dataprep.fovp.gwno)
)
UPDATE staging.country_year SET

    """

    for var in varlist:
        query += var['name_db'] + " = " + "b."+var['name_db'] + ",\n"

    # remove "," from the last var
    query = query.strip(",\n")

    query += """
FROM b
WHERE b.country_id = staging.country_year.country_id
AND b.year_id = staging.country_year.year_id;
"""
    
    return query

def read_varlist(path_varlist, excludevars = ["gwno", "year"]):
    excludevars = ["gwno", "year"]
    with open(path_varlist, 'r') as f:
        varlist = f.readlines()
    varlist = [line.lower().strip() for line in varlist]
    varlist = [line for line in varlist if not line[0]=="#"]
    varlist = [line for line in varlist if line not in excludevars]

    dictlist = []
    for line in varlist:
        d = {}
        if "," in line:
            d['name_masterdata'] = line.split(",")[0].strip()
            d['name_db'] = line.split(",")[1].strip()
        else:
            d['name_masterdata'] = line
            d['name_db'] = line

        d['name_li'] = d['name_db'] + "_li"
        dictlist.append(d.copy())
    return dictlist

def make_fueling_cy_selects(varlist):
    cy_selects = ""
    for var in varlist:
        cy_selects += "cy."+var['name_db'] + ",\n"
    return cy_selects

def main():
    path_varlist = "/Users/VIEWSADMIN/github/Views/SQLDataImport/fvp/varlist_masterdata.txt"
    schema_from = "dataprep"
    table_from = "fovp"
    schema_to = "staging"
    table_to = "country_year"
    schema_ipolate = "dataprep"
    table_ipolate = "cy_interp"


    varlist = read_varlist(path_varlist)

    drops = make_queries_drops(varlist, schema_to, table_to)
    adds = make_queries_add_column(varlist, schema_to, table_to)
    updates = make_query_update(varlist)

    cy_selects = make_fueling_cy_selects(varlist)

    create_cy_interp = make_query_create_cy_interp(varlist)
    populate_cy_interp = make_queries_add_column_li(varlist, schema_ipolate, 
                                                    table_ipolate)
    ipolate_update = make_queries_ipolate_update(varlist, schema_ipolate, 
                                                    table_ipolate)
    replace_staging_li = make_replace_staging_li(varlist)
    update_staging_li = make_update_staging_li(varlist)

    print(drops)
    print(adds)
    print(updates)
    print("#"*80)
    print("Paste into SQLFuelingplans!")
    print("#"*80)
    print(cy_selects)
    print("#"*80)
    print("Paste into SQLStaging/interpolatePGYCY")
    print("#"*80)        
    print(create_cy_interp)
    print(populate_cy_interp)
    print(ipolate_update)
    print(replace_staging_li)
    print(update_staging_li)


main()
