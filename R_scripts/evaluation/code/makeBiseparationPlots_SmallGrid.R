#Manual version of code to make Biseparation plots (MPC)
#RBJ, 9/23/18

# Specifying location of files and of included scripts
user = "Remco"

if(user == "HH") {
  rscript_location <- "~/Github/ViEWS/R_scripts/evaluation/"
}
if(user == "Remco") {
  setwd("~/github/Views/R_scripts/evaluation/")
}

source("code/prepEnviron.R")
source("code/Bisep_Plot.R")
#args = commandArgs(trailingOnly=TRUE)
#for testing
args = c("data/pgm_actuals_preds_08.csv","data/BisepModNames.csv", "ged_dummy_sb","row_col","BisepPlotSmall_")

#define inputs
inputData = args[1]
inputModelNames = args[2]
inputActualLocation = args[3]
inputLabelLocation = args[4]
outputPlotName=args[5]

#read in data
d1 = readr::read_csv(inputData)
print(paste0("read in ", inputData))

#optional subset of pgm data
d1 = filter(d1, (name == "Nigeria") & (month_id == 422))

#modDF = readr::read_csv(inputModelNames,col_names=FALSE)
#print(paste0("read in ", inputModelNames))

# functions:
#alternative: use function to get modelnames from string 
get_moDF = function(df, level, vtype, actual="dummy") {
  if (level == "pgm") {
    comp = colnames(df %>% select(contains(paste0("average_calib_select_", vtype))))
    preds = colnames(df %>% select(contains(vtype), -contains(paste0(actual, "_", vtype)),
                                  -contains(paste0("average_calib_"))))
  }
  if (level == "cm") {
    comp = colnames(df %>% select(contains(paste0("average_", vtype))))
    preds = colnames(df %>% select(contains(vtype), -contains(paste0(actual, "_", vtype)),
                                   -contains(paste0("average_", vtype))))
  }
  moDF = tibble(X1 = c(rep(comp, length(preds))), X2 = preds)
  return(moDF)
}

#plot function
# for cm: label_spacing at 80, right adjust .165, bottom adjust .138
bisepPlotFun = function(fx,fy,y,labels,modNameX,modNameY) {
  plotName = paste0("output/",outputPlotName,"_",modNameY,".pdf")
  ptemp = BicepPlot(f1=fx,f2=fy,y=y,labels=labels, m1title=modNameX, m2title=modNameY,  
                    label_spacing=20, bestN=5, right_margin=4.5, bottom_margin=5, top_margin = 2,
                    right_lab_adjust=.115, bottom_lab_adjust=.100, transp_adjust=0.5)
  return(ptemp)
}

#optional manual grid format (3/3x2?)
gridBisepPlot = function(p1, p2, p3, format="3") {
  if (format=="3") {
    while (!is.null(dev.list()))  dev.off()
    pdf("output/BisepGridPlot.pdf", height=4, width=10)
    grid.arrange(p1, p2, p3, ncol=3)
    dev.off()
  }
}

#get modelnames
moDF = get_moDF(d1_sub, level="pgm", vtype="sb")

#fetch specific modelnames manually here...
models = c(pull(moDF[1,2]), pull(moDF[2,2]), pull(moDF[3,2]))

#loop to create "p" objects
for (model in as.list(enumerate(models))) {
  modNameX = pull(moDF[1,1])
  modNameY = model$value
  modNumber = model$index
  assign(paste0("p", modNumber), 
         bisepPlotFun(fx=pull(d1[modNameX]), fy= pull(d1[modNameY]),
                      y=pull(d1[inputActualLocation]), labels=pull(d1[inputLabelLocation]), 
                      modNameX=modNameX, modNameY=modNameY))
}

#make gridplot
gridBisepPlot(p1, p2, p3)
