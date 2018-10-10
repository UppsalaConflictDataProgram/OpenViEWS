#!/usr/bin/Rscript

# Name: EBMA.R
# Inputs: list of models
# Outputs: Estimates of model's weights 
# Description: Ensemble Bayesian Model Averaging (EBMA) using EBMAforecast package
# Prepared for running on uppmax cluster

# Cleaning workspace
rm(list=ls());

# Loading libraries
library(EBMAforecast) # For Ensemble Bayesian Model Averaging (EBMA)
library(stats)        # For Generalized Linear Models i.e., glm()
library(lme4)         # For Generalized Linear Mixed Effects Model (GLMM) i.e., glmer
library(mgcv)         # For Generalized Additive Model (GAM) i.e, gam()

# Setting working directory
# To run this script on uppmax cluster, 
# the working directory will be the same as the directory containing script.
# setwd("/Users/sayyed/Dropbox/ViEWS/my_ViEWSmodeling/Runs/June2017_Full/");


# Read calibration and test datasets
calibration.df <- readRDS("calibration.pgm.df.rds");  # "ds" or "full"
test.df        <- readRDS("test.pgm.df.rds");


# Reading models (trained on June 2017 pgm data) and saving into a list structure
model_file_names = list("Big_mlevel.rds",	"Geography_glm.rds",  "History_glm.rds", "History_gam.rds", "Resources_glm.rds",  
                        "Geography_mlevel.rds", "Poverty_gam.rds", "rowcol_gam.rds",  "Expansive_glm.rds", 	"Resources_gam.rds");  
  
  
NumModels  <- length(model_file_names); 
ModelNames <- gsub('.{4}$', '', unlist(model_file_names));
model_list <- list();

for(i in 1:NumModels) {
  filename = paste0(model_file_location,model_file_names[[i]]);
  model = readRDS(file=filename);
  model_list[[i]] = model;
}
names(model_list) <- ModelNames;


# Reading prior on model's weights from a csv file containing model name and corresponding weight
uniform_weights = TRUE;
if(!uniform_weights) {
  InputModelsAndWeightsLocation = "modelsAndWeights.csv";
  modelsAndWeights <- read.csv(InputModelsAndWeightsLocation, header=FALSE, stringsAsFactors=FALSE);
  
  #check that weights are specified for all models and sum to 1 
  if( NumModels != dim(modelsAndWeights)[1] ) { 
    print("Weights should be specified for all models");
    break
  }
  if (sum(modelsAndWeights[,2])!=1) {
    print("Weights do not sum to 1, re-specify")
    break
  } 
}


# Function for making the predictions for each model in the calibration and test data set
# The input is:
#   listOfModels: list of models, of lenght k, where k is number of models, names will be kept (list of models)
#   Data   : Calibration or Test Data, (dataframe)
#   outcomeName : Name of outcome column in calibData  (as a string)
#   predType: "response" for predicted probabilities
# The output will be a dataframe with rows corresponds to observations and 
# a column corresponds to a prediction vector for each model in the model list.
# First column of the dataframe will be the actual variable.
GetPredsOutcomes <- function(listOfModels, Data,outcomeName,predType="response"){
  getPreds <- function(model,newdata,type=predType) {
     pred <- predict(model, newdata=newdata, type=type, allow.new.levels=TRUE)
     return(pred)
  }
  myPreds <- lapply(listOfModels, getPreds, newdata=Data)
  myPreds.df<- data.frame(myPreds)
  Outs <- cbind(Data[outcomeName],myPreds.df)
  return(Outs)
}

# Specify the outcome varaible name
outcomeName <- "ged_dummy_sb";

# Estimating the model predicted probabilities
# which are required to create a model object for forecastEBMA's makeForecastData function
# need both i.e., on calibration data, and then the test data
print("Predicting Probabilities...");
MyCalibPredOuts <- GetPredsOutcomes(model_list, calibration.df, outcomeName,"response");
MyTestPredOuts  <- GetPredsOutcomes(model_list, test.df, outcomeName,"response");

# Preprocessing step1:  Check if predicted probabilities are within the zero to one.
are_valid_predictions = apply(MyCalibPredOuts[, -1], MARGIN = 2, function(x) all(x>=0 & x<=1,na.rm=TRUE))
if( all(are_valid_predictions) )
  print("All predicted probabilities are within [0,1]");


# Preprocessing step2: Check if atleast one of the model have prediction
# This is to filter-out cases where all models fail to predict.
row_indices_calib = rowSums( is.na(MyCalibPredOuts[,2:(NumModels+1)]) ) < NumModels;
row_indices_test  = rowSums( is.na(MyTestPredOuts[,2:(NumModels+1)] ) ) < NumModels;
MyCalibPredOuts <- MyCalibPredOuts[row_indices_calib,];
MyTestPredOuts  <- MyTestPredOuts[row_indices_test,];

#Make Forecast object for EBMAforecast
print("Preparing EBMA forecast data object");
MyForecastData  <- makeForecastData(.predCalibration= MyCalibPredOuts[,ModelNames],
                                    .predTest = MyTestPredOuts[,ModelNames], 
                                    .outcomeCalibration= MyCalibPredOuts[,outcomeName],
                                    .outcomeTest = MyTestPredOuts[,outcomeName],
                                    .modelNames=ModelNames
)


#Setting parameters
model_param = "logit";        # The model type that should be used given the type of data that is being predicted
tol_param = 0.01;             # Tolerance for improvements in the log-likelihood before the EM algorithm will stop optimization.
shrinkage_param = 3;          # The exponential shrinkage term: Forecasts are raised to the (1/exp) power on the logit scale for the purposes of bias reduction.
const_param = 0.01;           # is the minimum weight for a model, makes sure weak models do not get pushed to zero, aka "wisdom of the crowd"


# Vector of initial model weights
if(uniform_weights) { 
  initial_weights = rep((1/NumModels),times=NumModels); 
} else {
  initial_weights = as.numeric(modelsAndWeights[,2]);
}

print("Running EBMA forecast...");

# Setting start time 
start.time <- Sys.time();

#Calibrate EBMA and get weights.
MyEnsemble <- calibrateEnsemble(MyForecastData, 
                                model=model_param,
                                tol=tol_param,
                                exp=shrinkage_param, 
                                const= const_param,
                                W=initial_weights)


# Reporting the computational time
print("calibration operation takes:")
end.time <- Sys.time();
time.taken <- end.time - start.time
print(time.taken);

#Saving resulted EBMA object into a file
print("Saving results");
saveRDS(MyEnsemble, file="EBMA.rds");
print("Computation done!")


