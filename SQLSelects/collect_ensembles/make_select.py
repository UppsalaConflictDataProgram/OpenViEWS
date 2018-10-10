
for time in ["eval_test", "fcast_test"]:
    table_name = "ensemble_pgm_{}".format(time)
    query = "DROP TABLE IF EXISTS landed.{};\n".format(table_name)
    query += "CREATE TABLE landed.{} AS \n".format(table_name)
    query += "SELECT \n"
    query += "sb.pg_id,\n"
    query += "sb.month_id,\n"

    for outcome in ["sb", "ns", "os"]:
        with open("template_varlist.sql", 'r') as f:
            template = f.read()

        template = template.replace("TIME", time)
        template = template.replace("OUTCOME", outcome)
        query += template
    query = query.strip(",\n")

    with open("template_join.sql", 'r') as f:
        template_from = f.read()
    time_tablename = time.replace("_test", "")
    join = template_from.replace("TIME", time_tablename)
    query += join

    path = "pgm_{}.sql".format(time)

    with open(path, 'w') as f:
        f.write(query)
    print("wrote", path)

    ############################################################################
    #   CM
    ############################################################################

    table_name = "ensemble_cm_{}".format(time)
    query = "DROP TABLE IF EXISTS landed.{};\n".format(table_name)
    query += "CREATE TABLE landed.{} AS \n".format(table_name)
    query += "SELECT \n"
    query += "sb.country_id,\n"
    query += "sb.month_id,\n"

    for outcome in ["sb", "ns", "os"]:
        with open("template_varlist_cm.sql", 'r') as f:
            template = f.read()

        template = template.replace("TIME", time)
        template = template.replace("OUTCOME", outcome)
        query += template
    query = query.strip(",\n")

    with open("template_join_cm.sql", 'r') as f:
        template_from = f.read()
    time_tablename = time.replace("_test", "")
    join = template_from.replace("TIME", time_tablename)
    query += join



    path = "cm_{}.sql".format(time)

    with open(path, 'w') as f:
        f.write(query)
    print("wrote", path)
