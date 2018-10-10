# File name: cost_based_model_evaluation.r
# A pipeline to perform cost based evaluation by using different measures

# Libraries
library('ROCR');           # For plotting ROC,PR,Accuracy Curves
library('separationplot'); # For separation plot (Greenhill, Ward & Sacks, 2011) package
library('RColorBrewer');   # For plotting in different colors
library('ggplot2');        # For histogram plot of forecast data
library('verification')    # For Brier Score
library('PRROC')           # For area under the PR-curve (auc)
library('stargazer')       # For latex tables etc.
library('purge')

# Clean workspace
rm(list=ls())

# Loading performance utilities saved in a separate file
source("/Users/sayyed/Dropbox/ViEWS/my_ViEWSmodeling/Scripts/Evaluation/simple_evaluation_utilities.r");
source("/Users/sayyed/Dropbox/ViEWS/my_ViEWSmodeling/Scripts/Evaluation/misc_utilities.r");


# Setting working directory
setwd("/Users/sayyed/Dropbox/ViEWS/my_ViEWSmodeling/Runs/June2017_Full/");


#############################################################################################
# Pipe input : 1. Read calibration and test data and specifying the actual observations
#              2. Read trained models that are saved as rds objects by using saveRDS function
#              3. Make a prediction matrix on given calibration and test data
#              4. Add model average in prediction matrix
#############################################################################################
data_file_location <- "Data/Full/";
actual_var_name <- "ged_dummy_sb";
test.df    <- readRDS( paste0(data_file_location,"test.pgm.df.rds") );
calib.df   <- readRDS( paste0(data_file_location,"calibration.pgm.df.rds") );

model_file_location <- "trained_models/DS/";
model_file_names    <- list( "Big_mlevel.rds", "Expansive_glm.rds", "Geography_glm.rds", "Geography_mlevel.rds", "History_gam.rds",
                             "History_glm.rds", "Poverty_gam.rds",  "Resources_gam.rds", "Resources_glm.rds", "rowcol_gam.rds");

model_list <- read_models(model_file_location,model_file_names);
P_calib <- make_prediction_matrix(calib.df, model_list);
P_test  <- make_prediction_matrix(test.df, model_list);
actual_calib <- calib.df[,actual_var_name];
actual_test  <- test.df[,actual_var_name];

# Missing values status of prediction matrix for calibration and test data
apply(P_calib,2, function(x) sum(is.na(x)))
apply(P_test ,2, function(x) sum(is.na(x)))

# Add model average into the prediction matrix
P_calib <- add_average_model(P_calib);
P_test  <- add_average_model(P_test);

# Validate if there is a missing value in 'actual' variable
select.cases <- which(complete.cases(actual_calib));
P_calib      <- P_calib[select.cases,];

select.cases <- which(complete.cases(actual_test));
P_test       <- P_test[select.cases,];


##########################################################################################
# Pipe input:  1. Read already trained ebma rds object created by 'EBMAforecast' package
#              2. Extract prediction matrix, actual and ebma weights by @ opertor 
#              3. Add model average in prediction matrix
#########################################################################################
ebma_file_location <- "trained_models/DS/";
ebma_file_name <- paste0(ebma_file_location,"EBMA.rds");

ebma.calib <- read_ebma_obj(ebma_file_name,OnCalib = TRUE);
ebma.test  <- read_ebma_obj(ebma_file_name,OnCalib = FALSE);
ebma_weights <- unlist( ebma.test@weights );

# Missing values status of prediction matrix for calibration, test data
apply(ebma.calib@P,2, function(x) sum(is.na(x)))
apply(ebma.test@P ,2, function(x) sum(is.na(x)))

# Adding model average
ebma.calib@P <- add_average_model(ebma.calib@P);
ebma.test@P  <- add_average_model(ebma.test@P);

# Validate if there is a missing value in actual variable
select.cases <- which(complete.cases(ebma.calib@actual));
ebma.calib@P <- ebma.calib@P[select.cases,];

select.cases <- which(complete.cases(ebma.test@actual));
ebma.test@P  <- ebma.test@P[select.cases,];


##################################################################################################
# Pipe Cost: 1. Specify a set of possible cost functions by using cost_matrix representation:
#            2. Find an optimal threshold, a hyper parameter for each model on calibration dataset 
#            3. Given optimal thresholds in step 2, Estimate the expected cost on test dataset
#################################################################################################

# Specify cost functions
#cf <- matrix(nrow=2, ncol=2, c(cost_tp, cost_fn, cost_fp, cost_tn) );  # Filled column-wise

cf0 <- matrix(nrow=2, ncol=2, c(0.0,  10.0,  1.0, 0.0)  );     

cf1 <- matrix(nrow=2, ncol=2, c(0.0,  -1.0,   -1.0, 0.0)  );   # Simple symmetric
cf2 <- matrix(nrow=2, ncol=2, c(0.0,  -10.0,  -1.0, 0.0)  );   # Simple asymmetric
cf3 <- matrix(nrow=2, ncol=2, c(1.0,  -1.0,   -1.0, 1.0)  );   # Cost-benefit symmetric
cf4 <- matrix(nrow=2, ncol=2, c(10.0, -10.0,  -1.0, 1.0)  );   # Cost-benefit asymmetric
cf5 <- matrix(nrow=2, ncol=2, c(20.0, -10.0,  -5.0, 1.0)  );   # Lisa-Dessan function



# Find optimal threshold and print output
P <- ebma.calib@P;
a <- ebma.calib@actual;
cost_matrix <- cf2;
  
optimal0 <- compute_optimal_threshold(P,a,cf0);
optimal1 <- compute_optimal_threshold(P,a,cf1);
optimal2 <- compute_optimal_threshold(P,a,cf2);
optimal3 <- compute_optimal_threshold(P,a,cf3);
optimal4 <- compute_optimal_threshold(P,a,cf4);
optimal5 <- compute_optimal_threshold(P,a,cf5);


print(optimal2) 
 

# Estimate the expected cost for each model
costs <- compute_cost(ebma.test@P,ebma.test@actual,cf2,unlist(optimal3[,"cutoff"]));
print(costs)


# Normalizing cost by the number of predictions each model made and order them
total_obs = length(actual_test);
pred_vec = total_obs - apply(P_test,2, function(x) sum(is.na(x)));
costs <- costs / pred_vec;
costs <- costs[order(costs[,1], decreasing = FALSE),]
print(costs);



# Specify the result directory
outfile_location = "Results/PMDS/";
post_fix = "June2017";
outfile = paste0(outfile_location,"cost_plot_",post_fix);
plot_cost_function(ebma.calib@P,ebma.calib@actual,cf2, outfile) 





plot_expected_cost(costs,outfile);







# plotting normalized total cost per prediction
outfile = paste0(outfile_location,"cost_per_pred_",post_fix);
plot_cost_per_prediction(P,a,outfile);

# Set cost according to rare-ity of positives in the test dataset.
# i.e., by taking the ratio of negatives to positives (rare cases). 
# total_obs = length(actual);
# cost_fn = ( length(which(actual==0)) / length(which(actual==1)) ) ;  


# plot"optimal cost" on cost set to the ratio of negative to positive 
outfile = paste0(outfile_location,"cost_fnc10_",post_fix,".pdf");
plot_optimal_cost_per_pred(P[,-6],a,cost_fp,cost_fn,outfile);


# plot rocr explicit cost as a function of threshold
outfile = paste0(outfile_location,"cost_curve_fnc10_",post_fix,".pdf");
plot_simple_cost_function(P[,],actual, cost_fp, cost_fn, outfile);


############################################################
# plotting other performance measures
############################################################

# To see missing data summary for predicting probabilities
cat('Missing Predictions out of total ', dim(P)[1]);
apply(P,2, function(x) sum(is.na(x)))

# Summarizing the performance measures
outfile = paste0(outfile_location,"performance_summary_",post_fix);
write_performance_table(P,actual,outfile);

# Plotting ROC curve: (x-axis = fpr, y-axis = tpr)
outfile = paste0(outfile_location,"roc_curves_",post_fix,".pdf");
plot_performance(P,actual,"fpr","tpr",outfile);

# Plotting PR curve: (x-axis = recall, y-axis = precision)
outfile = paste0(outfile_location,"pr_curves_",post_fix,".pdf");
plot_performance(P,actual,"rec","prec",outfile);

# Plotting PR curve in display matrix of size 3x2 
outfile = paste0(outfile_location,"pr_curves_sep_",post_fix,".pdf");
plot_performance_separate(P,actual,"rec","prec",c(3,2),outfile);

# Plotting Sensitivity/specificity curve: (x-axis = specificity, y-axis = sensitivity)
outfile = paste0(outfile_location,"ss_curves_",post_fix,".pdf");
plot_performance(P,actual,"spec","sens",outfile);

# Ploting accuracy: (x-axis = cutoff, y-axis = accuracy)
outfile = paste0(outfile_location,"accuracy_plot_",post_fix,".pdf");
plot_performance(P,actual,"cutoff","acc",outfile);

# Plot histogram of predicted probabilities for binary outcome
performance_combine_hist(P,actual,outfile_location);

# ploting EBMA weights
outfile = paste(outfile_location,"ebma_weights_plot",".pdf",sep='');
plot_EBMA_Weights(ebma_weights,outfile);











########################################################################################
########################################################################################

# New analysis for the comparison of DS and Full approach ...
# not connected ...

mat_cost_fl <- mat_cost;
mat_cost_ds <- mat_cost;


# Converting matrix into dataframe
df.fl <- as.data.frame(as.table(mat_cost_fl));
df.fl[,"Data"] <- rep("Full",times=dim(df.fl)[1]);

df.ds <- as.data.frame(as.table(mat_cost_ds));
df.ds[,"Data"] <- rep("DS",times=dim(df.ds)[1]);

df.plot <- rbind(df.fl,df.ds);

colnames(df.plot)<-c("fn_cost","models","total_cost","Data");
df.plot[,2] <- as.factor(df.plot[,2]);
df.plot[,1] <- as.numeric(log(df.plot[,1]));
df.plot[,4] <- as.factor(df.plot[,4]);



plot3 <-  ggplot(data = df.plot, aes(x = fn_cost, y = total_cost, color = models, group = models)) +
  geom_line(aes(colour=models,linetype=models))+
  scale_color_manual(values=myPalette)+
  ylim(0,1)+
  xlab("Log of false negative cost")+
  ylab("Normaized total cost")+
  facet_grid(Data ~ .)


outfile_location = "Results/";
post_fix = "June2017";
outfile = paste0(outfile_location,"cost_per_pred_cmp_",post_fix,".pdf");
ggsave(filename=outfile, plot=plot3);




# # Converting matrix into dataframe
# df.plot <- as.data.frame(as.table(mat_cutoff));
# df.plot[,1] <- rep(fn_cost_var,times=dim(mat_cutoff)[2]);
# colnames(df.plot)<-c("fn_cost","models","cutoff");
# df.plot[,2] <- as.factor(df.plot[,2]);
# 
# 
# plot2 <-  ggplot(data = df.plot, aes(x=fn_cost, y=cutoff, color=models),group = models) + 
#           geom_line(aes(colour=models))+
#           geom_point(shape=1,size = 1)+
#           xlim(min(fn_cost_var),max(fn_cost_var));
# 
# 
# plot(plot2)
# 
# outfile = paste0(outfile_location,"costplot2_",post_fix,".pdf");
# ggsave(filename=outfile, plot=plot2);
# 











############################################################
# For models collected in a single list i.e., list1 option
############################################################

if(read_model_list1) {
  
  model_names <- names(model_list);
  NumModels   <- length(model_list);
  
  actual_var_name <- model_actual[[1]];
  actual <- test.df[,actual_var_name];
  
  
  # Given trained models and test data set, prepare the prediction matrix
  # set type = "response" to get predicted probabilities
  # A is the matrix containing actual observations corresponding to P prediction matrix
  print("Preparing prediction matrix ...");
  P <- matrix(nrow = dim(test.df)[1], ncol = NumModels, data = NA);
  for (i in 1:NumModels ) {
    print(model_names[i]);
    P[,i]  <- c(predict(model_list[[i]],test.df,type="response",allow.new.levels = TRUE) );
    actual_var_name = model_actual[[i]];
  }
  colnames(P) <- model_names;
  
  # Reading EBMA object containing predictions for each model and for EBMA
  EBMA = FALSE;
  if(EBMA) {
    
    # For hierarchical style inout option e.g. "sb_EBMA.rds"
    print("Reading EBMA object ...");
    ebma_file_location <- "Models_Downsampled/";
    ebma_file_name <- paste(ebma_file_location,"EBMA.rds",sep="");
    ebma_object <- readRDS(ebma_file_name);
    ebma_model_name <- "EBMA";
    model_names = c(ebma_model_name,ebma_object@modelNames);
    NumModels = length(model_names);
    NumObs = dim(ebma_object@predTest)[1];
    P = matrix(nrow = NumObs, ncol = NumModels, data = NA);
    for (i in 1:NumModels) {
      print(model_names[i]);
      P[,i]<- ebma_object@predTest[,i,1];
    }
    colnames(P) <- model_names;
    actual <- ebma_object@outcomeTest;
    ebma_weights <- ebma_object@modelWeights;
  }
  
  # To see missing data summary for predicting probabilities
  cat('Missing Predictions out of total ', dim(P)[1]);
  apply(P,2, function(x) sum(is.na(x)))
  
  
  #Specify the result directory
  outfile_location = "Evaluation_Cost/";
  post_fix = "April2017_Down";
 
  
  # cost based analysis
  outfile = paste0(outfile_location,"cost_analysis_",post_fix,".pdf");
  plot_cost(P,actual, cost_fp=1.0, cost_fn=10.0, outfile);

  # Summarizing the performance measures
  outfile = paste(outfile_location,"performance_summary_",post_fix,sep='');
  write_performance_table(P,actual,outfile);
  
  
  # Plotting ROC curve: (x-axis = fpr, y-axis = tpr)
  outfile = paste(outfile_location,"roc_curves_",post_fix,".pdf",sep='');
  plot_performance(P,actual,"fpr","tpr",outfile);
  
  # Plotting PR curve: (x-axis = recall, y-axis = precision)
  outfile = paste(outfile_location,"pr_curves_",post_fix,".pdf",sep='');
  plot_performance(P,actual,"rec","prec",outfile);
  
  # Plotting Sensitivity/specificity curve: (x-axis = specificity, y-axis = sensitivity)
  outfile = paste(outfile_location,"ss_curves_",post_fix,".pdf",sep='');
  plot_performance(P,actual,"spec","sens",outfile);
  
  # Ploting accuracy: (x-axis = cutoff, y-axis = accuracy)
  outfile = paste(outfile_location,"accuracy_plot_",post_fix,".pdf",sep='');
  plot_performance(P,actual,"cutoff","acc",outfile);
  
  # Ploting mutual information: (x-axis = cutoff, y-axis = mi)
  outfile = paste(outfile_location,"mi_plot_",post_fix,".pdf",sep='');
  plot_performance(P,actual,"cutoff","mi",outfile);
  
  # Drawing separation plot
  outfile = paste(outfile_location,"separation_plot_",post_fix,".pdf",sep='');
  plot_separation(P,actual,outfile);
  
  # Plot histogram of predicted probabilities for binary outcome
  performance_hist(P,actual,outfile_location);
  
}




###############################################################################################
# For models arranged in a list of lists i.e., hierarchical style e.g., "sb_" "ns_" "os_"
# Please note that the script onward is set for the input option of "list2" i.e., list of lists
###############################################################################################

if(read_model_list2){
  
for( list_name in names(model_list2) ) {
  
  # Prepare a model list with name according to Hierarchical style e.g., "sb_" "ns_" "os_"
  model_list   <- list();
  model_actual <- list();
  for ( model_name in names(model_list2[[list_name]]) ){
    
    mod.name <- paste(list_name,"_",model_name,sep="");
    mod.obj  <- model_list2[[list_name]][[model_name]];
    
    mod.actual <- all.vars(formula(mod.obj))[1]; 
    
    model_list[[mod.name]]   <- mod.obj;
    model_actual[[mod.name]] <- mod.actual;
  }
  model_names <- names(model_list);
  NumModels   <- length(model_list);
  
  # Specify the outcome varaible name
  # Set actual varaible from the formula of the first model in the list
  actual_var_name <- model_actual[[1]];
  actual <- test.df[,actual_var_name];
  
  
  # Model perform for "unexpected conflicts"
  # I would like to define the true outcome to 1 if: 
  # ged_dummy_X == 1 and ged_months_since_last_X > 12 and ged_months_since_last_X_lag1 >12 and ged_months_since_last_X_lag2 > 12 
  
  unexpected_conflicts_performance = TRUE;
  if(unexpected_conflicts_performance) {
      
       if(list_name=="sb") {
         actual <-    ifelse ( test.df$ged_dummy_sb==1 & 
                               test.df$ged_months_since_last_sb>12 &
                               test.df$ged_months_since_last_sb_lag1>12 & 
                               test.df$ged_months_since_last_sb_lag2>12    ,1,0);
         
       }
       
       if(list_name=="ns") {
         actual <-    ifelse ( test.df$ged_dummy_ns==1 & 
                                 test.df$ged_months_since_last_ns>12 &
                                 test.df$ged_months_since_last_ns_lag1>12 & 
                                 test.df$ged_months_since_last_ns_lag2>12   ,1,0);
         
       }
       
       if(list_name=="os") {
         actual <-    ifelse ( test.df$ged_dummy_os==1 & 
                                 test.df$ged_months_since_last_os>12 &
                                 test.df$ged_months_since_last_os_lag1>12 & 
                                 test.df$ged_months_since_last_os_lag2>12   ,1,0);
         
       }
  }
  
  
  
  # Given trained models and test data set, prepare the prediction matrix
  # set type = "response" to get predicted probabilities
  # A is the matrix containing actual observations corresponding to P prediction matrix
  print("Preparing prediction matrix ...");
  P <- matrix(nrow = dim(test.df)[1], ncol = NumModels, data = NA);
  for (i in 1:NumModels ) {
    print(model_names[i]);
    P[,i]  <- c(predict(model_list[[i]],test.df,type="response",allow.new.levels = TRUE) );
    actual_var_name = model_actual[[i]];
  }
  colnames(P) <- model_names;


  # Reading EBMA object containing predictions for each model and for EBMA
  EBMA = FALSE;
  if(EBMA) {
    
    # For hierarchical style inout option e.g. "sb_EBMA.rds"
    print("Reading EBMA object ...");
    ebma_file_location <- "Models/";
    ebma_file_name <- paste(ebma_file_location,list_name,"_EBMA.rds",sep="");
    ebma_object <- readRDS(ebma_file_name);
    ebma_model_name <- paste(list_name,"_EBMA",sep="");
    model_names = c(ebma_model_name,ebma_object@modelNames);
    NumModels = length(model_names);
    NumObs = dim(ebma_object@predTest)[1];
    P = matrix(nrow = NumObs, ncol = NumModels, data = NA);
    for (i in 1:NumModels) {
      print(model_names[i]);
      P[,i]<- ebma_object@predTest[,i,1];
    }
    colnames(P) <- model_names;
    actual <- ebma_object@outcomeTest;
    ebma_weights <- ebma_object@modelWeights;
  }

  # To see missing data summary for predicting probabilities
  cat('Missing Predictions out of total ', dim(P)[1]);
  apply(P,2, function(x) sum(is.na(x)))

  #Specify the result directory
  outfile_location = "Evaluation_Unexpected/";

  
  # Summarizing the performance measures
  outfile = paste(outfile_location,"performance_summary_",list_name,sep='');
  write_performance_table(P,actual,outfile);

  
  # Plotting ROC curve: (x-axis = fpr, y-axis = tpr)
  outfile = paste(outfile_location,"roc_curves_",list_name,".pdf",sep='');
  plot_performance(P,actual,"fpr","tpr",outfile);

  # Plotting PR curve: (x-axis = recall, y-axis = precision)
  outfile = paste(outfile_location,"pr_curves_",list_name,".pdf",sep='');
  plot_performance(P,actual,"rec","prec",outfile);

  # Plotting Sensitivity/specificity curve: (x-axis = specificity, y-axis = sensitivity)
  outfile = paste(outfile_location,"ss_curves_",list_name,".pdf",sep='');
  plot_performance(P,actual,"spec","sens",outfile);

  # Ploting accuracy: (x-axis = cutoff, y-axis = accuracy)
  outfile = paste(outfile_location,"accuracy_plot_",list_name,".pdf",sep='');
  plot_performance(P,actual,"cutoff","acc",outfile);

  # Ploting mutual information: (x-axis = cutoff, y-axis = mi)
  outfile = paste(outfile_location,"mi_plot_",list_name,".pdf",sep='');
  plot_performance(P,actual,"cutoff","mi",outfile);

  # Drawing separation plot
  outfile = paste(outfile_location,"separation_plot_",list_name,".pdf",sep='');
  plot_separation(P,actual,outfile);
  
  # Plot histogram of predicted probabilities for binary outcome
  performance_hist(P,actual,outfile_location);
  
  
  # Plot weights of each model with accuracy 
  if(EBMA) {
    outfile = paste(outfile_location,"ebma_weights_plot_",list_name,".pdf",sep='');
    plot_EBMA_Weights(P,actual,ebma_weights,outfile);
  }

}

}


# ModelCriticism plot
# Citation: Colaresi, Michael., & Mahmood, Zuhaib. (2017). Do the robot: Lessons from machine learning to improve conflict forecasting. Journal of Peace Research. 54(2): 193-214.
# Install command: install_github("zsmahmood89/ModelCriticism/packages/ModelCriticism") using R library(devtools)

# Model1 versus Model2
#library('ModelCriticism')

#BicepPlot(f1, f2, y, labels, bestN=10, label_spacing=3,right_lab_adjust=0.02,
#          bottom_lab_adjust=0.03,right_margin=5,bottom_margin=5,top_margin=1,
#          transp_adjust=1, m1title="Model 1", m2title="Model 2", hlines=TRUE,vlines=TRUE,bw=FALSE,rare=FALSE) 

#dfg=BicepPlot ( f1=P[,1], f2=P[,2], y=actual, labels= (1:dim(P)[1])  );
#grid.draw(dfg)



# separation plot option to specify or highlight the special cases 
# showing specific values
#f = !v;
#f = f[v];
#show these values
#f[5] = TRUE
#f[512] = TRUE
#f[1012] = TRUE
#f[2012] = TRUE
#separationplot(pred=p,actual=a, shuffle=TRUE, line=TRUE, type="line",flag=f,newplot=F);





############################
########################
#####################
###############
# This function will determine the total cost for each model for model comparison 
compute_optimal_cost<-function(P,a,cost_fn=10.0,cost_fp=1.0) {
  
  NumModels = dim(P)[2];
  
  pm = matrix(nrow = NumModels, ncol = 6, data = NA);
  rownames(pm) <- colnames(P);
  colnames(pm) <- c("tp","tn","fp","fn","cutoff","cost");
  
  for (i in 1:NumModels) {
    
    pred <- prediction(predictions=P[,i], labels = a);
    
    # perf <- performance(pred, "cost", cost.fp = cost_fp, cost.fn = cost_fn)
    # optimal.ind    <- which.min(perf@y.values[[1]]);
    # optimal.cutoff <- pred@cutoffs[[1]][optimal.ind];
    # if( is.infinite( optimal.cutoff) ) { optimal.cutoff = 1.0; }
    
    tp <- pred@tp[[1]][];
    tn <- pred@tn[[1]][];
    fp <- pred@fp[[1]][];
    fn <- pred@fn[[1]][];
    
    cost <- (fn * cost_fn) + (fp * cost_fp);
    
    optimal.ind <- which.min(cost);
    optimal.cost <- cost[optimal.ind];
    optimal.cutoff <- pred@cutoffs[[1]][optimal.ind];
    if( is.infinite( optimal.cutoff ) ) { optimal.cutoff = 1.0; }
    
    pm[i,] <- c(tp[optimal.ind],tn[optimal.ind],fp[optimal.ind],fn[optimal.ind],optimal.cutoff,optimal.cost);
    
  }
  
  return(pm);
}



# Setting false negative cost variable
fn_cost_var <- seq(0,1000,by=10);
fn_cost_var[1] <- 1;
cost_fn = 10.0; 
cost_fp = 1.0;


# Computing the number of prediction for each model
total_obs = length(actual);
pred_vec = total_obs - apply(P,2, function(x) sum(is.na(x)));


mat_cost   = matrix(nrow = length(fn_cost_var), ncol = NumModels, data = NA);
for(i in 1:length(fn_cost_var)) {
  
  cost_fn = fn_cost_var[i];
  pm=compute_optimal_cost(P,actual,cost_fn,cost_fp);
  
  accuracy <-  t( ( pm[,"tp"] + pm[,"tn"] ) / ( pm[,"tp"] + pm[,"tn"] + pm[,"fp"] + pm[,"fn"]) );
  cutoff   <-  t( pm[,"cutoff"] ); 
  cost     <-  t( pm[,"cost"] / pred_vec );
  
  mat_cost[i,] = cost;
  
  colnames(mat_cost) <- rownames(pm);
}
rownames(mat_cost) <-fn_cost_var;

# Converting matrix into dataframe
df.plot <- as.data.frame(as.table(mat_cost));
df.plot[,1] <- rep(fn_cost_var,times=dim(mat_cost)[2]);
colnames(df.plot)<-c("fn_cost","models","total_cost");
df.plot[,2] <- as.factor(df.plot[,2]);
df.plot[,1] <- as.numeric(log(df.plot[,1]));


# Ploting by ggplot
qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
#col_vector = grDevices::colors()[grep('gr(a|e)y', grDevices::colors(), invert = T)]
#col_vector = rainbow(NumModels,s = 0.5);
#col_vector = brewer.pal(NumModels, "Set3")
#col_vector = rainbow(NumModels, s=.6, v=.9)[sample(1:NumModels,NumModels)]
#myPalette = sample(col_vector, NumModels);
myPalette  = col_vector[1:NumModels];

plot1 <- ggplot(data = df.plot, aes(x=fn_cost, y=total_cost, color=models),group = models) + 
  geom_line(aes(colour=models,linetype=models))+
  scale_color_manual(values=myPalette)+
  #geom_point(shape=1,size = 1)+
  ylim(0,1)+
  xlab("Log of false negative cost")+
  ylab("Normaized total cost");
#xlim(min(fn_cost_var),max(fn_cost_var));

# Specify the result directory
outfile_location = "Results/";
post_fix = "June2017";
outfile = paste0(outfile_location,"cost_per_pred_FL_",post_fix,".pdf");
ggsave(filename=outfile, plot=plot1);

write_cost_based_ranking<-function(mat_cost,fn_cost_var,outfile) {
  
  require(MESS);
  auc_vec = apply(mat_cost, 2, function(x)  auc(log(fn_cost_var),x, type = 'spline')   )  ; 
  auc_vec <- sort(auc_vec);
  auc_mat = matrix(nrow = length(auc_vec), ncol = 1, data = auc_vec);
  colnames(auc_mat) <- c("AUC_Cost");
  rownames(auc_mat) <- names(auc_vec);
  
  file <- paste(outfile,".tex",sep="");
  stargazer(auc_mat,type='latex',out = file, title="Table: Area under the Normalized total cost curve");
  
  file <- paste(outfile,".txt",sep="");
  stargazer(auc_mat,type='text' ,out = file, title="Table: Area under the Normalized total cost curve");
  
}



#######################################################################
# This function will plot cost curve over cutoffs by using ROCR package
#######################################################################
plot_cost<-function(P, a, cost_fp=1.0, cost_fn=10.0, outfile) {
  if( dim(P)[1] != length(a) ) 
    return;
  
  n = dim(P)[2];
  colors <- rainbow(n);
  linetype <- c(1:n) ;
  plotchar <- seq(18,18+n,1);
  
  select.cases = which(complete.cases(a));
  P <- P[select.cases,];
  a <- a[select.cases];
  
  pdf(outfile);
  par(oma=c(0, 0, 0, 8))
  for (i in 1:n) {
    
    # Creating a prediction object 
    # Predictions are the estimated probabilities (or log odds) and the labels are binary values.
    pred <- prediction(predictions = P[,i], labels = a);
    
    # Prepare a performance object
    pref <- performance(pred, measure = "cost", cost.fp=cost_fp, cost.fn=cost_fn);
    
    # ROCR package detail formula for cost
    # cost <- ((n.pos / n.samples) * (fn / n.pos) * cost.fn + (n.neg / n.samples) * (fp / n.neg) * cost.fp)
    
    
    # Setting y limit
    ylim = range(pretty(c(0, unlist(pref@y.values) )));
    
    # Plotting the curves on the same plot
    plot(pref, add=(i!=1),lwd=1.0,colorize=FALSE ,lty=linetype[i], col=colors[i], pch=plotchar[i], ylim = ylim);
    
  }
  legend(par('usr')[2], par('usr')[4],  bty='n', xpd=NA, lty=linetype, col=colors, legend=colnames(P), cex=0.8);
  dev.off();
  return;
}




