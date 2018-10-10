# File name: misc_utilities.r
# Author: Sayyed Auwn Muhammad


# This function will read model files (saved by saveRDS function) from 
# a specified location given by input parameter model_file_location and 
# a list of model file names.
read_models<-function(model_file_location, model_file_names) {
  print("Reading model file one by one ...");
  model_list <- list();
  NumModels  <- length(model_file_names);
  for (i in 1:NumModels) {
    model_file_name <- model_file_names[[i]];
    print(model_file_name);
    model_name <- gsub('.{4}$', '', model_file_name);
    mod.obj <- readRDS( paste0(model_file_location, model_file_name)  );
    model_list[[model_name]] <- mod.obj;
  }
  return(model_list);
}

# Given dataframe as input and list of model objects from above function
# This function will making a prediction matrix, whose columns will present predicted probabilities
# and rows will be the obervations.
make_prediction_matrix<-function(df, model_list) {
  model_names <- names(model_list);
  NumModels   <- length(model_list);
  P <- matrix(nrow = dim(df)[1], ncol = NumModels, data = NA);
  for (i in 1:NumModels ) {
    print(model_names[i]);
    P[,i]  <- c( predict(model_list[[i]],df,type="response",allow.new.levels = TRUE) );
  }
  colnames(P) <- model_names;
  return(P);
}  


# Function to read EBMA object containing predictions for each model and for EBMA
# Input parameter ebma_obj_file will provide the file name (including path)
# Input parameter OnCalib = TRUE will return predicted probabilites and actual variable for calibration data
# whereas OnCalib = TRUE will return predicted probabilites and actual variable for test data presented to ebma package for its learning
read_ebma_obj<-function(ebma_obj_file,OnCalib=FALSE) {
  
  
  setClass(Class="EBMA_OBJ",
           representation(
             P="matrix",
             actual="integer",
             weights = "numeric"
           )
  )
  
  ebma_object <- readRDS(ebma_file_name);
  model_names <- c("EBMA",ebma_object@modelNames);
  NumModels = length(model_names);
  if(OnCalib) { NumObs <- dim(ebma_object@predCalibration)[1] }
  else {  NumObs <- dim(ebma_object@predTest)[1] }
  
  P = matrix(nrow = NumObs, ncol = NumModels, data = NA);
  for (i in 1:NumModels) {
    print(model_names[i]);
    
    if(OnCalib) { P[,i] <-  ebma_object@predCalibration[,i,1] }
    else        { P[,i] <-  ebma_object@predTest[,i,1] }
    
  }
  colnames(P) <- model_names;
  if(OnCalib)  { actual <- ebma_object@outcomeCalibration }
  else         { actual <- ebma_object@outcomeTest}
  weights <- ebma_object@modelWeights; 
  
  ebma.obj <- new("EBMA_OBJ", P = P, actual = actual, weights = weights);

  return(ebma.obj);
}


# Function to add a worst model to the prediction matrix 
add_worst_model <- function(P,actual) {
  NumModels <- dim(P)[2];
  P <- cbind(P,worst_model=ifelse(actual,0.0,1.0));
  return(P);
}

# Function to add average model to the prediction matrix
add_average_model <- function(P) {
  NumModels <- dim(P)[2];
  P <- cbind(P, model_average=rowMeans(P[,2:NumModels] , na.rm=TRUE));
  return(P);
}



