#Code to make Biseparation plots for ViEWS Summer 2018
#MPC, 9/10/18
#Dependencies, run code/prepEnviron.R first, see readMe.md
# Input (5 args):
#  inputData: location of data to use in csv format (data/cm_actuals_preds.csv)
#  inputModelNames: location of a csv with two columns, model on x in the first column, model on y in the second column. These names should match column names in the inputData. They can be a subset. No spaces after last entry, no newline at end (data/BisepModNames.csv)
#  inputActualLocation: String of column name where actual observation is located in inputData ()
#  inputLabelLocation: String of column name where label is located in inputData ()
#  outputPlotName: stub for plot name
#Output:
#  will create output/*outputPlotName**modelNameX**modelNameY*.pdf, where *outputPlotName* is replaced by the stub and *modelNameX* and *modelNameY* are replaced by the actual model names that produced the respective predictions)

source("code/prepEnviron.R")
args = commandArgs(trailingOnly=TRUE)
#for testing
#args = c("data/cm_actuals_preds.csv","data/BisepModNames.csv", "ged_dummy_sb","country_id","TestBisep")

#define inputs
inputData = args[1]
inputModelNames = args[2]
inputActualLocation = args[3]
inputLabelLocation = args[4]
print(paste0("read in args"))

#define outputs
outputPlotName=args[5]

#read in data
d1 = readr::read_csv(inputData)
print(paste0("read in ", inputData))

modDF = readr::read_csv(inputModelNames,col_names=FALSE)
print(paste0("read in ", inputModelNames))

bisepPlotFun = function(fx,fy,y,labels,modNameX,modNameY) {
  plotName = paste0("output/",outputPlotName,"_",modNameX,"_",modNameY,".pdf")
  ptemp = BicepPlot(f1=fx,f2=fy,y=y,labels=labels, m1title=modNameX, m2title=modNameY,  
                    label_spacing=30, bestN=20, right_margin=8, bottom_margin=8,
                    right_lab_adjust = .05, bottom_lab_adjust = .05)
  #close default grid device
  dev.off()
  pdf(plotName, height=9, width=9)
  grid::grid.draw(ptemp)
  dev.off()
}

for (i in 1:dim(modDF)[1]) {
  modNameX = pull(modDF[i,1])
  modNameY = pull(modDF[i,2])
  bisepPlotFun(fx=pull(d1[modNameX]), fy= pull(d1[modNameY]),
   y=pull(d1[inputActualLocation]), labels=pull(d1[inputLabelLocation]), modNameX=modNameX, modNameY=modNameY)
  print(paste0("produced plot for ",modNameX,"/",modNameY))
}
print("The End")
