# This file defines R functions for interacting with the database
dir_certs_default <- path.expand("~/.postgres")

DbToDf<-function(host, db, username, port, query, 
  dir_certs=dir_certs_default) {
  # Fetches a dataframe from the database
  # 
  # Args:
  #   host: database server hostname or IP adress
  #   db: name of the databse
  #   username: your username on the database
  #   port: default 5432 for postgres
  #   query:  a string containing valid SQL
  #   dir_certs:  the location on your system of certificate files root.crt, 
  #               postgresql.key and postgresql.crt Defaults to ~/.postgres
  #
  # Returns:
  #   df
  #
  # Example:
  #   df <- DbToDf(
  #     host =      "VIEWSHOST", 
  #     db =        "views", 
  #     username =  "VIEWSADMIN", 
  #     port =      "5432", 
  #     query =     "SELECT pg_id, month_id, ged_dummy_sb FROM preflight.flight_pgm;",
  #     dir_certs = "/Users/VIEWSADMIN/.postgres")
  # 
  # Dependencies:
  #   install.packages("DBI")
  #   install.packages("RPostgreSQL", type="source")

  
  library("RPostgreSQL")
  start.time <- Sys.time()
  
  pq_dsn <- paste(
    'dbname=',      db, ' ',
    'sslrootcert=', dir_certs, '/root.crt', ' ',
    'sslkey=',      dir_certs, '/postgresql.key', ' ',
    'sslcert=',     dir_certs, '/postgresql.crt', ' ',
    'sslmode=verify-ca',
    sep=""
  )

  conn <- dbConnect(RPostgreSQL::PostgreSQL(), dbname=pq_dsn, 
                    host=host, port=port, user=username)
  rs <- dbSendQuery(conn, statement=query)
  
  #(-1 to get all rows; for n>0 will only return n rows)
  df <- fetch(rs, n=-1)
  dbDisconnect(conn)
  end.time <- Sys.time()
  time.to.fetch.data <- end.time - start.time
  print("fetched")
  return(df)
}

DfToDb<-function(df, host, db, username, port, schema, table, 
  dir_certs=dir_certs_default, overwrite=FALSE) {
  # Pushes a dataframe to the database
  # 
  # Args:
  #   df: the dataframe you want to push
  #   host: database server hostname or IP adress
  #   db: name of the databse
  #   username: your username on the database
  #   port: default 5432 for postgres
  #   schema: database schema to push to
  #   table: database table to push to
  #   dir_certs:  the location on your system of certificate files root.crt, 
  #               postgresql.key and postgresql.crt Defaults to ~/.postgres
  #
  # Returns:
  #   None
  #
  # Example:
  #   df <- readRDS("/some/path/df.rds")
  #   df <- DbToDf(
  #     host =      "VIEWSHOST", 
  #     db =        "views", 
  #     username =  "VIEWSADMIN", 
  #     port =      "5432", 
  #     dir_certs = "/Users/VIEWSADMIN/.postgres",
  #     schema = "landed_test",
  #     table = "tester_table",
  #     df = df)
  #     
  # Dependencies:
  #   install.packages("DBI")
  #   install.packages("RPostgreSQL", type="source")
  #
  library("RPostgreSQL")
  start.time <- Sys.time()
  
  pq_dsn <- paste(
    'dbname=',      db, ' ',
    'sslrootcert=', dir_certs, '/root.crt', ' ',
    'sslkey=',      dir_certs, '/postgresql.key', ' ',
    'sslcert=',     dir_certs, '/postgresql.crt', ' ',
    'sslmode=verify-ca',
    sep=""
  )

  conn <- dbConnect(RPostgreSQL::PostgreSQL(), dbname=pq_dsn, 
                    host=host, port=port, user=username)

  message = paste0("Writing to ", schema, ".", table)
  print(message)
  dbWriteTable(conn, c(schema, table), value=df, overwrite=overwrite)
  dbDisconnect(conn)

  end.time <- Sys.time()
  time.to.fetch.data <- end.time - start.time
  message = paste("Finished writing, time:", time.to.fetch.data)
  print(message)
}
