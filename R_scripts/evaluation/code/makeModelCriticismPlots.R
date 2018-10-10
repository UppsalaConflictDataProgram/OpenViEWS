#Code to make model criticism plots for ViEWS Summer 2018
#MPC, 9/10/18
#Dependencies, run code/prepEnviron.R first, see readMe.md
# Input (5 args):
#  inputData: location of data to use in csv format (data/cm_actuals_preds.csv)
#  inputModelNames: location of a csv with one column, with model names, these names should match column names in the inputData. They can be a subset. No spaces after last entry, no newline at end
#  inputActualLocation: String of column name where actual observation is located in inputData ()
#  inputLabelLocation: String of column name where label is located in inputData ()
#  outputPlotName: stub for plot name
#Output:
#  will create output/MCPlot*modelName*.pdf, where *modelName* is replaced by the actual model name that produced these predictions)

source("code/prepEnviron.R")
args = commandArgs(trailingOnly=TRUE)
#for testing
#args = c("data/cm_actuals_preds.csv","data/modNames.csv", "ged_dummy_sb","country_id","MCPlotSB")


#define inputs
inputData = args[1]
inputModelNames = args[2]
inputActualLocation = args[3]
inputLabelLocation = args[4]
print("Read args")


#define outputs
outputPlotName=args[5]

#read in data
d1 = readr::read_csv(inputData)
print(paste0("read in ",inputData))

modVec = pull(readr::read_csv(inputModelNames,col_names=FALSE)[1])
print(paste0("read in ", inputModelNames))

diagPlotFun = function(f,y,labels,modName) {
  plotName = paste0("output/",outputPlotName,modName,".pdf")
  ptemp = DiagPlot(f,y,labels, title=modName, right_margin=8, lab_adjust=.25,  label_spacing=30, text_size=8)
  #close default grid device
  dev.off()
  pdf(plotName, height=9, width=9)
  grid::grid.draw(ptemp)
  dev.off()
}

for (i in modVec) {
  diagPlotFun(f=pull(d1[i]),y=pull(d1[inputActualLocation]), label=pull(d1[inputLabelLocation]), modName=i)
  print(paste0("produced plot for ",i))
}
print("The End")
