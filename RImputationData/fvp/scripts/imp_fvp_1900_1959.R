library("Amelia")
library("foreign")
library("methods")
library("parallel")

date.start <- Sys.time()

path.input <- "df_1900_1959.rds"
path.image <- "fvp_imp_1900_1959_image.RData"
path.imp.stems <- "fvp_imp_1900_1959"

n.imputations <- 10
n.cpus <- 10

var.ts <- "year"
var.group <- "gwno"
nominals <-c("FVP_demo", "FVP_semi", "FVP_auto", 
             "FVP_regime3c", "regimechange")


df <- readRDS(path.input)

# finding the bounds
lower <- c()
upper <- c()
for (i in 1:length(df)) {
  print(i)
  lower <- c(lower, min(df[,i], na.rm=T))    
  upper <- c(upper, max(df[,i], na.rm=T))    
}

# numbers of all cols except 1 and 2: the timevar and var.group
varnr <- c(3:ncol(df))
lower <- lower[varnr]
upper <- upper[varnr]
bounds <- matrix(cbind(varnr,lower,upper),ncol(df)-2)

object.amelia <- amelia(df, 
  m = n.imputations, 
  ts = var.ts, cs = var.group, noms = nominals,
  p2s=2, polytime = 2, 
  intercs = TRUE, empri = .1*nrow(df),
  bounds = bounds, 
  max.resample = 1000, 
  parallel="multicore", ncpus= n.cpus)

#Saving the imputed data sets in .dta format
write.amelia(obj=object.amelia,
             file.stem = path.imp.stems, format = "dta")
print("Saved imputed datasets")

save.image(file = path.image)
print("Saved R image")

#Total time of imputation
date.end <- Sys.time()
duration <- date.end - date.start
print(duration)

