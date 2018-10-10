# rewrite of Auwns "cost_based_model_evaluation.R"

# to do:
# specify a directory to put confusion matrices .tex into

#libraries
if (!require("pacman")) install.packages("pacman")
pacman::p_load(ROCR, separationplot, RColorBrewer, ggplot2, caret,
               verification, PRROC, stargazer, purge, xtable, dplyr)

# Clean workspace
rm(list=ls())

# Loading performance utilities saved in a separate file
rscript_location <- "~/Github/ViEWS/R_scripts/"
alt_loc <- "~/github/Views/views_utils/"
source(paste0(rscript_location,"simple_evaluation_utilities.r"))
source(paste0(rscript_location,"misc_utilities.r"))
source(paste0(alt_loc,"dbutils.R"))

# Setting working directory
setwd("~/Dropbox (ViEWS)/ViEWS/ViEWSModeling/CostEvaluation/Tables")

# read data
data_file_location <- "/Users/remco/github/Views/views_utils/scripts/"
cm_actuals_preds <- read.csv(paste0(data_file_location, "cm_actuals_preds_08.csv"))
pgm_actuals_preds <- read.csv(paste0(data_file_location, "pgm_actuals_preds.csv"))

# read the data from DB (*) 
#host <- "VIEWSHOST"
#db <- "views"
#port <- "5432"
#dir_certs <- paste0("/Users/",user,"/.postgres")
#query <- "SELECT id, month_id, country_id, ged_dummy_sb FROM preflight.flight_cm;"
#df_preflight <- DbToDf(host, db, port, query, dir_certs)

# specify cost function (simple symmetric)
cf0 <- matrix(nrow=2, ncol=2, c(0.0, 1.0, 1.0, 0.0))

# Functions
apply_cf <- function(df, costfunction, vtype) {
  # Finds optimal threshold for partition given a costfunction
  # Per model, returns 'costs', 'confusion matrix', '
  
  # extract columns of interest (note: -contains(..) excludes)
  if (vtype=="pr") {
    a <- df[, colnames(df %>% select(ends_with(paste0("dummy_sb"))))]
  } else {
    a <- df[, colnames(df %>% select(ends_with(paste0("dummy_", vtype))))]
  }
  p <- df[, colnames(df %>% select(contains(paste0("_",vtype)), 
                                   ends_with(paste0("average_",vtype)),
                                   -starts_with("ged_dummy")))]
  # compute the optimal threshold (provide for all types!)
  optimal <- compute_optimal_threshold(p, a, costfunction)
  cutoff <- as.data.frame(optimal[,"cutoff"])
  colnames(cutoff)[1] <- "cutoff"
  # set up matrix, set up colrownames
  costs <- matrix(NA, ncol=1, nrow=length(p))
  rownames(costs) <- colnames(p)
  colnames(costs) <- cbind("cost per cf")
  # apply cost function
  costs[,1] <- compute_cost(p, a, costfunction, unlist(optimal[,"cutoff"]))$total_cost
  confmat_all <- compute_cost(p, a, costfunction, unlist(optimal[,"cutoff"]))$conf_mat
  # return
  return(list(costs=costs, confmat_all = confmat_all, describe=optimal, cutoff=cutoff))
}

get_matrix <- function(df, modelname) {
  # function to get individual confusion matrices from return of apply_cf
  
  confmat <- matrix(NA, ncol=2, nrow=2, dimnames=list(c("Pos", "Neg"), c("Pos", "Neg")))
  names(dimnames(confmat)) <- c("Predicted", "Observed")
  data <- as.data.frame(df$confmat_all[modelname, ])
  confmat[1,1] = data[1,1]
  confmat[2,2] = data[2,1]
  confmat[1,2] = data[3,1]   
  confmat[2,1] = data[4,1]
  confmat <- addmargins(as.table(confmat))
  cutoff <- round(df$cutoff[modelname, ], 3)
  accuracy <- round((confmat[1,1] + confmat[2,2]) / confmat[3,3], 3) #round?
  print(confmat)
  
  # latex, correction for underscores in modelnames and make caption
  fix_modelname <- paste(strsplit(modelname, "_")[[1]])
  fix_modelname <- paste(fix_modelname, collapse="\\_")
  caption <- paste("Confusion matrix for", fix_modelname)
  
  # latex, add outer dimnames and notes per solution:
  # https://stackoverflow.com/questions/33511311/add-two-commands-to-the-add-to-row-arguments-in-xtable
  # instructions
  rws <- c(nrow(confmat))
  dimnames <- c(paste("& \\multicolumn{2}{c}{Predicted} \\\\\n", "\\cline{2-3}",
                "Observed & Pos & Neg & Sum \\\\\n", "\\cline{1-4}"))
  note <- c(paste("\\hline \n",  # replace all default hlines with this and the ones below
                  "\\multicolumn{4}{p{.4\\columnwidth}}{\\textit{Note}. Accuracy = ", 
                  accuracy, ". Cutoff = ", cutoff, ".}  \n", sep = ""))
  # create list to receive instructions for add.to.row
  addtorow <- list()
  # position arguments addtorow (?)
  addtorow$pos <- as.list(c(0, rws))
  # assign corresponding commands
  addtorow$command <- as.vector(c(dimnames, note))
  # print
  print(xtable(confmat, caption = caption, align = c("p{1.5cm}", "p{1.5cm}", "p{1.5cm}", "p{1.5cm}"),
               digits=c(0,0,0,0)), 
        caption.placement="top", add.to.row = addtorow, hline.after=c(-1), 
        include.colnames = FALSE, file = paste0("confmat_",modelname,".tex"))
  # returns
  return(confmat)
}

write_matrices <- function(df) {
  for (model in rownames(df$costs)) {
    get_matrix(df, model) }
}

# get returns for selected costfunction, level, and vtype
cf_cm_returns <- apply_cf(cm_actuals_preds, cf0, "os")
cf_pgm_returns <- apply_cf(pgm_actuals_preds, cf0, "sb")

# print all information (also see other objects outputted by apply_cf())
print(cf_cm_returns$describe)
print(cf_pgm_returns$describe)
xtable(cf_cm_returns$describe)
xtable(cf_pgm_returns$describe)

# or just the constituent parts
print(cf_cm_returns$confmat_all)
print(cf_pgm_returns$confmat_all)
print(cf_cm_returns$cutoff)
print(cf_pgm_returns$cutoff)
print(cf_cm_returns$costs)
print(cf_pgm_returns$costs)

# get confusion matrix in contingency table per specified modelname, from associated cf dataframe
cm_model_matrix <- get_matrix(cf_cm_returns, "average_sb")
pgm_model_matrix <- get_matrix(cf_pgm_returns, "average_select_sb")

# or use a loop to produce them all
for (item in c("sb", "ns", "os", "pr")) {
  cf_cm_returns <- apply_cf(cm_actuals_preds, cf0, item)
  write_matrices(cf_cm_returns)
}
