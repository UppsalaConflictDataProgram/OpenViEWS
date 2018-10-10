FindBounds <- function(df){
  print("finding bounds")
  lower <- c()
  upper <- c()
  for (i in 1:length(df)) {
    lower <- c(lower, min(df[,i], na.rm=T))    
    upper <- c(upper, max(df[,i], na.rm=T))    
  }
  
  varnr <- c(1:ncol(df))
  lower <- lower[varnr]
  upper <- upper[varnr]
  bounds <- matrix(cbind(varnr,lower,upper),ncol(df))

  return(bounds)

}

KeepOnlyVarying <- function(df){
  print("Removing non-varying columns from dataframe")
  # Find variance to remove non-varying variables.
  variances <- sapply(df, var, na.rm = TRUE)

  # Some vars are all missing, they get variance NA, give them zero instead
  variances[is.na(variances)] <- 0

  names.zero.variance <- colnames(df[variances == 0])
  names.positive.variance <- colnames(df[variances > 0])
  df <- df[names.positive.variance]

  return(df)
}

KeepOnlyNumerics <- function(df){
  print("Removing non-numeric columns from dataframe")
  numerics <- sapply(df, is.numeric)
  df <- df[numerics]

  return(df)
}
