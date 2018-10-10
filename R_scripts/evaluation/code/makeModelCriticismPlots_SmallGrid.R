#Manual version of code to make Model Criticism plots (MPC)
#RBJ, 9/23/18

user = "Remco"

if(user == "HH") {
  rscript_location <- "~/Github/ViEWS/R_scripts/evaluation/"
}
if(user == "Remco") {
  setwd("~/github/Views/R_scripts/evaluation/")
}

source("code/prepEnviron.R")
source("code/Diag_Plot.R")
library(grid)
#args = commandArgs(trailingOnly=TRUE)
#for testing
args = c("data/cm_actuals_preds_08.csv","data/modNames.csv", "ged_dummy_sb","iso_date","MCPlotSmall_")

#define inputs
inputData = args[1]
inputModelNames = args[2]
inputActualLocation = args[3]
inputLabelLocation = args[4]
outputPlotName=args[5]

#read in data
d1 = readr::read_csv(inputData)
print(paste0("read in ",inputData))

#moDF = pull(readr::read_csv(inputModelNames,col_names=FALSE)[1])
#print(paste0("read in ", inputModelNames))

# functions:
#alternative: use function to get modelnames from string (?)
get_moDF = function(df, vtype, actual="dummy") {
  actuals = colnames(d1 %>% select(contains(paste0(actual, "_", vtype))))
  preds = colnames(d1 %>% select(contains(vtype), -contains(paste0(actual, "_", vtype))))
  moDF = tibble(X1 = c(rep(actuals, length(preds))), X2 = preds)
  return(moDF)
}

#plot function
diagPlotFun = function(f,y,labels,modName) {
  plotName = paste0("output/",outputPlotName,modName,".pdf")
  ptemp = DiagPlot(f,y,labels, title=modName, right_margin=4.5, top_margin=3.5,
                   lab_adjust=.50, label_spacing=80, text_size=7)
  return(ptemp)
}

#optional manual grid format (2/2x2)
gridBisepPlot = function(p1, p2, p3, format="3") {
  if (format=="3") {
    while (!is.null(dev.list()))  dev.off()
    pdf("output/MCGridPlot.pdf", height=4, width=10)
    grid.arrange(p1, p2, p3, ncol=3)
    dev.off()
  }
}

#specicy the modelnames to get
moDF = get_moDF(d1, vtype="sb")

#specify the modelnames you want to single out here
models = c(pull(moDF[1,2]), pull(moDF[2,2]), pull(moDF[3,2]))

#loop to create numbered "p" objects
for (model in as.list(enumerate(models))) {
  modNameY = model$value
  modNumber = model$index
  assign(paste0("p", modNumber), 
         diagPlotFun(f=pull(d1[modNameY]),y=pull(d1[inputActualLocation]),
                     label=pull(d1[inputLabelLocation]), modName=modNameY))
}

#produce plot
gridBisepPlot(p1, p2, p3)
