source("../views_utils/dbutils.R")
source("imputils.R")

library("Amelia")
library("foreign")
library("methods")
library("parallel")

time.start <- Sys.time()

path.query <- 'select_cy.sql'
query <- readChar(path.query, file.info(path.query)$size)

host <-      "VIEWSHOST" #Janus
db <-        "views"
username <-  "VIEWSADMIN"
port <-      "5432"
query <-     query
schema.output <- "launched"
table.output.stem <- "cy_imp_"
path.imp.stems <- "cy_imp_"

df <- DbToDf(
  host =      host, 
  db =        db, 
  username =  username, 
  port =      port, 
  query =     query)

var.ts <- "year_id"
var.group <- "country_id"
n.imputations <- 5
n.cpus <- 5


# Drop all vars that don't vary
df <- KeepOnlyVarying(df)
# Drop all non-numeric vars
df <- KeepOnlyNumerics(df)

nominals <- c()

# Find the bounds of each var, we don't want never-before seen values
bounds <- FindBounds(df)

# Run the imputation
obj.amelia <- amelia(df,m = n.imputations, 
                        ts = var.ts, cs = var.group, noms = nominals,
                        p2s=2, polytime = 1, 
                        intercs = TRUE, empri = .1*nrow(df),
                        bounds = bounds, 
                        max.resample = 1000, 
                        parallel="multicore", ncpus= n.cpus)

print("Finished imputing")

write.amelia(obj=obj.amelia,
             file.stem = path.imp.stems, format = "csv")
print("Saved imputed datasets")

# Push imputated datasets to db
for (i in 1:n.imputations) { 
  string.assign.imp = paste0("df.imputed <- obj.amelia$imputations$imp",i)
  eval(parse(text=string.assign.imp))

  table.output.imp <- paste0(table.output.stem, i)
  DfToDb(df=df.imputed, host=host, db=db, username=username, 
    port=port, schema=schema.output, table=table.output.imp,
    overwrite=TRUE)
    }

time.end <- Sys.time()
time.total = time.end - time.start
print("FINISHED!")
print(paste("Total runtime:", time.total))

