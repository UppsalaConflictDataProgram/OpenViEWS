# File name: simple_evaluation_utilities.r
# Author: Sayyed Auwn Muhammad
# Performance evaluation functions like roc-auc, pr-auc, Brier score, plots, separation plots etc


# Load required libraries
require('ROCR');           # For plotting ROC,PR,Accuracy Curves
require('separationplot'); # For separation plot (Greenhill, Ward & Sacks, 2011) package
require('RColorBrewer');   # For plotting in different colors
require('ggplot2');        # For histogram plot of forecast data
require('verification')    # For Brier Score
require('PRROC')           # For area under the PR-curve (auc)
require('stargazer')       # For latex tables etc.
require('precrec')


WritePerformanceTable<-function(P,a,outfile) {
  # Function for summarizing performance measures such as Brier Score, AUC-ROC, AUC-PR
  # to tables by using stargazer routines
  # Input parameter P is a prediction matrix, each column represents the predicted probabilites from a model
  # Input paramter a is a vector containing corresponding actual oberved values for the prediction matrix P
  # The number of elements in a should be equal to the row dimention of matrix P. i.e., nrow(P) = length(actual)
  # Column name will be used to name the models
  # Output will be the stargazer files (txt and tex) containing "ROC_AUC","Brier_Score","PR_AUC" performance measure  

  NumModels = dim(P)[2];
  
  pm = matrix(nrow = NumModels, ncol = 3, data = NA);
  colnames(pm) <- c("ROC_AUC","Brier_Score","PR_AUC");
  rownames(pm) <- colnames(P);
  
  for (i in 1:NumModels) {
    pred <- prediction(predictions=P[,i], labels = a);
    pref <- performance(pred , measure = "auc");
    
    # I have to discard missing cases here
    idx = complete.cases(P[,i]);
    scores <- data.frame(predictions=P[idx,i], labels=a[idx]);
    pr <- pr.curve(scores.class0=scores[scores$labels=="1",]$predictions,
                   scores.class1=scores[scores$labels=="0",]$predictions,
                   curve=T)
    
    roc_auc     <- pref@y.values[[1]];
    brier_score <- brier(a, P[,i])$bs;
    pr_auc      <- pr$auc.integral;
    
    pm[i,] <- c(roc_auc,brier_score,pr_auc);
  }
  
  file <- paste(outfile,".tex",sep="");
  stargazer(pm,type='latex',out = file, title="Table: Performance Measures Summary");
  
  file <- paste(outfile,".txt",sep="");
  stargazer(pm,type='text' ,out = file, title="Table: Performance Measures Summary");
}

PlotPerformance<-function(P,a,x_measure,y_measure,outfile) {
  # Function for ploting performance measure such as ROC, PR, Accuracy etc.
  # Input parameter P is a prediction matrix, each column represents the predicted probabilites from a model
  # Input paramter a is a vector containing corresponding actual oberved values for the prediction matrix P
  # The number of elements in a should be equal to the row dimention of matrix P.
  # x_measure and y_measure are the performance measures plotted on x-axis and y-axis respectively.
  # and can be chosen from the list of some commonly used measures:
  # "acc" : Accuracy estimated as (TP+TN)/(P+N)
  # "fpr" : False positive rate = FP/N
  # "tpr" : True positive rate = TP/P 
  # "rec" : Recall = TP/(TP+FN)
  # "prec": Precision = TP/(TP+FP)
  # "mi"  : Mutual information I(Y',Y) = H(Y) - H(Y|Y')
  # "f"   : Precision-Recall F-measure = Weighted harmonic mean of precision (P) and recall (R).
  # "cutoff" : Denotes different cutoffs on the x-axis i.e., (x-axis = cutoff, y-axis = performace_measure)
  # Output will be plot of performance measure curves for each model, for example 
  # call plot_performance(P,a,"fpr","tpr",outfile) will plot ROC curve.
  # call plot_performance(P,a,"rec","prec",outfile) will plot PR curve. 
  # call plot_performance(P,a,"spec","sens",outfile) will plot plot sensitivity/specificity curve.
  # call plot_performance(P,actual,"cutoff","acc",outfile) will plot accuracy as function of threshold etc. 

  if( dim(P)[1] != length(a) ) 
    return;
  
  n = dim(P)[2];
  colors   <- rainbow(n);
  linetype <- c(1:n) ;
  plotchar <- seq(18,18+n,1);
  
  not_NA = TRUE;
  if(not_NA) {
    idx = complete.cases(P);
    P <- P[idx,];
    a <- a[idx];
  }
  
  strict_ylimit <- TRUE;
  
  pdf(outfile);
  par(oma=c(0, 0, 0, 8))
  for (i in 1:n) {
    
    # Creating a prediction object 
    # Predictions are the estimated probabilities (or log odds) and the labels are binary values.
    pred <- prediction(predictions = P[,i], labels = a);
    
    # Prepare a performance object
    pref <- performance(pred , measure = y_measure, x.measure = x_measure);
    
    # Setting y limit
    if(strict_ylimit) { ylim <- c(0,1.0); }
    else {  ylim <- range(pretty(c(0, unlist(pref@y.values) )));  }  
    
    # Plotting the curves on the same plot
    plot(pref, add=(i!=1),lwd=1.0,colorize=FALSE ,lty=linetype[i], col=colors[i], pch=plotchar[i], ylim = ylim);
    
  }
  legend(par('usr')[2], par('usr')[4],  bty='n', xpd=NA, lty=linetype, col=colors, legend=colnames(P), cex=0.8);
  dev.off();
  return;
}

PlotPerformanceSeparate<-function(P,a,x_measure,y_measure,subfig_dim,outfile) {
  # plot_performance_separate is the varaint of the above function
  # The only difference is that it plot in a matrix style, where each cell is individual plot
  # the subfig_dim is the input parameter, which is dimension of a plot
  # Example call is as follows: 
  # plot_performance_separate(P,actual,"rec","prec",c(3,2),outfile) plot PR curve in a 3 by 2 matrix plot windows.

  if( dim(P)[1] != length(a) ) 
    return;
  
  n = dim(P)[2];
  colors <- rainbow(6,s = 0.5); #rainbow(n);
  linetype <- c(1:n) ;
  plotchar <- seq(18,18+n,1);
  
  not_NA = TRUE;
  if(not_NA) {
    idx = complete.cases(P);
    P <- P[idx,];
    a <- a[idx];
  }
  
  strict_ylimit <- TRUE;
  
  model_names <- colnames(P);
  
  pdf(outfile);
  par(mfrow = subfig_dim,oma=c(0, 0, 0, 8))
  for (i in 1:n) {
    
    # Creating a prediction object 
    # Predictions are the estimated probabilities (or log odds) and the labels are binary values.
    pred <- prediction(predictions = P[,i], labels = a);
    
    # Prepare a performance object
    pref <- performance(pred , measure = y_measure, x.measure = x_measure);
    
    # Setting y limit
    if(strict_ylimit) { ylim <- c(0,1.0); }
    else {  ylim <- range(pretty(c(0, unlist(pref@y.values) )));        }  
    
    # Plotting the curves on the same plot
    plot(pref, lwd=1.0, lty=1, col="red", ylim = ylim, main=model_names[i],cex.main=1.0);
    
  }
  dev.off();
  return;
}

PlotEBMAWeights<-function(W,outfile) {
  # This function will plot EBMA weights
  # where W is a (named) list containing the weights for each model.
  # note that W should be a name list i.e., each element should be named by the corresponding model.
  
  df <- data.frame ( Models = names(W), Weight  = W ); 
  
  myPlot <- ggplot(df, aes(x=Models, y=Weight, fill=Models)) + 
    geom_bar(stat='identity', color='black') + 
    scale_y_continuous(limits = c(0, 1))+
    scale_fill_brewer(palette='Pastel1') +
    theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust=0.5)) +
    geom_text(aes(label=round(Weight,2)), vjust=-0.25, color='black', size = 3.0, position=position_dodge(.9))
  
  #plot(myPlot);
  ggsave(filename=outfile, plot=myPlot);
}

PlotEBMAWeightsAccuracy<-function(P,a,W,outfile) {
  # This function will plot EBMA weights for each model with thier accuracies computed from prediction matrix P.
  # Same as above P is the prediction matrix and a is the corresponding vector of actual obervations. and nrow(P) = length(actual)
  # W is a (named) list containing the weights for each model.
  # note that W should be a name list i.e., each element should be named by the corresponding model.
  
  NumModels = dim(P)[2];
  
  pm = matrix(nrow = NumModels, ncol = 3, data = NA);
  colnames(pm) <- c("ROC_AUC","Brier_Score","PR_AUC");
  rownames(pm) <- colnames(P);
  
  for (i in 1:NumModels) {
    
    pred <- prediction(predictions=P[,i], labels = a);
    pref <- performance(pred , measure = "auc");
    
    idx = complete.cases(P[,i]);
    scores <- data.frame(predictions=P[idx,i], labels=a[idx]);
    pr <- pr.curve(scores.class0=scores[scores$labels=="1",]$predictions,
                   scores.class1=scores[scores$labels=="0",]$predictions,
                   curve=T)
    
    roc_auc     <- pref@y.values[[1]];
    brier_score <- brier(a, P[,i])$bs;
    pr_auc      <- pr$auc.integral;
    
    pm[i,] <- c(roc_auc,brier_score,pr_auc);
    
  }
  
  # Include EBMA itself
  #model_names = c("EBMA", names(W))
  #W = c(1.0,W);
  #names(W) <- model_names;
  #A = pm[,"ROC_AUC"];
  
  model_names <- names(W);
  A = pm[2:NumModels,"ROC_AUC"];
  
  df <- data.frame ( Models = c(rep(model_names,times=2)),
                     Performance = c( rep("Weight",length(model_names)), 
                                      rep("AUC",length(model_names))), 
                     Weight  = c(W,A) ); 
  
  
  
  myPlot <- ggplot(df, aes(x=Models, y=Weight, fill=Performance)) + 
    geom_bar(stat='identity', position='dodge', color='black') + 
    scale_y_continuous(limits = c(0, 1))+
    scale_fill_brewer(palette='Pastel1') +
    theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
    geom_text(aes(label=round(Weight,2)), vjust=1.5, color='black', size = 2.0, position=position_dodge(.9))
  
  ggsave(filename=outfile, plot=myPlot,  width = 7, height = 4);
}

PlotSeparation <- function (P,a,outfile) {
  # Function for customized (plotting on the same plot) separation plot
  # Input parameter P is a prediction matrix, each column represents the predicted probabilites from a model
  # Input paramter a is a vector containing corresponding actual oberved values for the prediction matrix P
  # The number of elements in a should be equal to the row dimention of matrix P. i.e., nrow(P) = length(actual)
  # Output will be a sinlge plot containing separation strips for each model in P matrix. 


  NumModels = dim(P)[2];
  
  select.rows = complete.cases(P); 
  p = P[select.rows,];
  a = a[select.rows];
  pdf(outfile);
  
  # Set mar() for margin and oma() for outer margin area.
  # in order to set there are 4 values i.e., (bottom, left, top, right)
  # For example, par(mar=c(4,0,0,0)) draws a margin of 4 lines only on the bottom of the chart.
  par(mfrow=c(NumModels,1), oma = c(5,4,0,0) + 0.1, mar = c(0,0,1,1) + 0.1)
  
  for (i in 1:NumModels) {
    separationplot(pred=p[,i],actual=a, heading=colnames(p)[i],shuffle=TRUE, line=TRUE, type="line",newplot=F);
  }
  dev.off();
  return;
}

PerformanceHist <- function(P, a, outfile_location) {
  # Plotting the distribution of predicted probabilities for positive "Conflict" and negative "Peace" events.
  # Input parameter P is a prediction matrix, each column represents the predicted probabilites from a model and
  # Input paramter a is a vector containing corresponding actual oberved values for the prediction matrix P.
  # Input parameter outfile_location is the location of the output file, function will save plot in separate file of same name as model names in P.
  # Output will be the number of plots (files) equal to the number of columns in P.

  if( dim(P)[1] !=  length(a) ) return;
  
  not_NA = TRUE;
  if(not_NA) {
    idx = complete.cases(P);
    P <- P[idx,];
    a <- a[idx];
  }
  
  NumModels = dim(P)[2];
  model_names = colnames(P);
  for (i in 1:NumModels) {
    pred_ones =  P[(a == 1),i];
    pred_zeros = P[(a == 0),i];
    df <- data.frame ( label  = c( rep("conflict",length(pred_ones)), 
                                   rep("peace"   ,length(pred_zeros))), 
                       predicted_prob = c(pred_ones,pred_zeros) ); 
    
    myPlot <- ggplot(df)+ geom_histogram(aes(x=predicted_prob,y=..ncount.., fill=label), color="grey80") + scale_y_continuous(limits=c(0,1)) + facet_grid(label~.)
    outfile = paste(outfile_location,"perfHist_",model_names[i],".pdf",sep='');
    ggsave(filename=outfile, plot=myPlot,  width = 7, height = 4);
  }
}  

PerformanceCombineHist <- function(P, a, outfile_location) {
  # Same function as above however it tries to plot all models on the same plot for better comparisons.
  # Plotting model combined performance histograms for all models

  if( dim(P)[1] !=  length(a) ) return;
  
  not_NA = TRUE;
  if(not_NA) {
    idx = complete.cases(P);
    P <- P[idx,];
    a <- a[idx];
  }
  
  NumModels = dim(P)[2];
  model_names = colnames(P);
  
  idx0 = which(a==0);
  idx1 = which(a==1);
  
  df.plot <- as.data.frame(as.table(P));
  df.plot <- df.plot[,-1];
  colnames(df.plot) <- c("models","predicted_prob");
  l <- ifelse(a==1,"conflict","peace");
  df.plot[,"label"] <- rep(l,times=dim(P)[2]);
  
  df.plot[,1] <- as.factor(df.plot[,1]);
  df.plot[,2] <- as.numeric(df.plot[,2])
  df.plot[,3] <- as.factor(df.plot[,3]);
  
  
  myPlot <-  ggplot(df.plot, aes(x = predicted_prob)) +
    geom_histogram(aes(x=predicted_prob,y=..ncount.., fill=label), color="grey80") +
    scale_y_continuous(breaks = c(0.0,0.5,1.0), limits=c(0,1)) +
    facet_grid(models ~ label, scales = "free_x")+
    theme(strip.text.y = element_text(size = 8, angle = 0))+
    xlab("Predicted probability")+
    ylab("Relative frequency");
  
  #plot(myPlot);
  outfile = paste0(outfile_location,"perfHist_combine.pdf");
  ggsave(filename=outfile, plot=myPlot);
} 


##########################################################################################
##########################################################################################
# Cost based model comparison  
##########################################################################################
##########################################################################################


ComputeOptimalThreshold<-function(P,a,cost_matrix) {
  # This function, for a given cost matrix, will determine the optimal threshold for each model,
  # By optimal threshold, we mean a threshold, which minimizes the cost function specified by the cost matrix. 
  # Input parameter P is a prediction matrix, each column represents the predicted probabilites from a model
  # Input paramter a is a vector containing corresponding actual oberved values for the prediction matrix P
  # Note: The number of elements in a should be equal to the row dimention of matrix P. i.e., nrow(P) = length(actual)
  # Input "cost_matrix" should be ordered like cost_tp, cost_fn, cost_fp, cost_tn (filled column-wise)
  # The function will return a matrix pm containing rows for each model like:
  # c(TP(optimal_threshold),TN(optimal_threshold),FP(optimal_threshold),FN(optimal_threshold), optimal_threshold, cost_at_optimal_threshold)

  cost_tp = cost_matrix[1,1];
  cost_tn = cost_matrix[2,2];
  cost_fp = cost_matrix[1,2];          
  cost_fn = cost_matrix[2,1];
  
  NumModels = dim(P)[2];
  
  optimal = matrix(nrow = NumModels, ncol = 6, data = NA);
  rownames(optimal) <- colnames(P);
  colnames(optimal) <- c("tp","tn","fp","fn","cutoff","cost");
  
  for (i in 1:NumModels) {
    
    pred <- prediction(predictions=P[,i], labels = a);
    # The pred object contains one line for each prediction in the P object,
    # sorted by cutoffs in descending order, 
    # and the cumulative number of tp, tn, fp, fn as the object is gone through sequentially
    tp <- pred@tp[[1]][];
    tn <- pred@tn[[1]][];
    fp <- pred@fp[[1]][];
    fn <- pred@fn[[1]][];
    
    cost <- (tp * cost_tp) + (tn * cost_tn) + (fn * cost_fn) + (fp * cost_fp);
    
    optimal.ind <- which.min(cost);
    optimal.cost <- cost[optimal.ind];
    optimal.cutoff <- pred@cutoffs[[1]][optimal.ind];
    if( is.infinite( optimal.cutoff ) ) { optimal.cutoff = 1.0; }
    
    optimal[i,] <- c(tp[optimal.ind],tn[optimal.ind],fp[optimal.ind],fn[optimal.ind],optimal.cutoff,optimal.cost);
  }
  
  return(optimal);
}

ConfusionMatrix <- function(obs,pred,threshold=0.5){
  # Code taken from https://github.com/jjvanderwal/SDMTools
  # Credit goes to Jeremy VanDerWal jjvanderwal@gmail.com
  # Just for the direct computation of a confusion matrix for a given threshold in the presence of missing values etc.
  # Issue warnings on missing values etc

  #input checks
  if (length(obs)!=length(pred)) stop('this requires the same number of observed & predicted values')
  if (!(length(threshold)==1 & threshold[1]<=1 & threshold[1]>=0)) stop('inappropriate threshold value... must be a single value between 0 & 1.')
  n = length(obs); if (length(which(obs %in% c(0,1,NA)))!=n) stop('observed values must be 0 or 1') #ensure observed are values 0 or 1
  
  #deal with NAs
  if (length(which(is.na(c(obs,pred))))>0) {
    na = union(which(is.na(obs)),which(is.na(pred)))
    warning(length(na),' data points removed due to missing data')
    obs = obs[-na]; pred = pred[-na]
  }
  #apply the threshold to the prediction
  if (threshold==0) {
    pred[which(pred>threshold)] = 1; pred[which(pred<=threshold)] = 0
  } else {
    pred[which(pred>=threshold)] = 1; pred[which(pred<threshold)] = 0
  }
  #return the confusion matrix
  mat = table(pred=factor(pred,levels=c(0,1)),obs=factor(obs,levels=c(0,1)))
  attr(mat,'class') = 'confusion.matrix'
  return(mat)
}

ComputeCost<-function(P,a,cost_matrix,optimal.thresholds) {
  # This function, for a given prediction matrix "P", actual "a" and thresholds, 
  # will compute the cost function specified by given cost matrix.
  
  if ( dim(P)[1]!= length(a))
    stop('rows in prediction matrix should be equal to the number of actual values')
  
  cost_tp = cost_matrix[1,1];
  cost_tn = cost_matrix[2,2];
  cost_fp = cost_matrix[1,2];          
  cost_fn = cost_matrix[2,1];
  
  NumModels   <- dim(P)[2];
  model_names <- colnames(P);
  total_cost <- matrix(nrow = dim(P)[2], ncol = 1, data = NA);
  row.names(total_cost) <- model_names;
  colnames(total_cost)  <- "cost"
  confmat <- matrix(nrow=dim(P)[2],ncol = 4, data = NA);
  colnames(confmat) <- c("tp","tn","fp","fn")
 
   for( i in 1:NumModels ) {
    
    model <- model_names[i];
    
    # Compute confusion matrix on test data for "optimal threshold"  
    confusion <- confusion.matrix(a,  P[,model], threshold = optimal.thresholds[i]);
    
    # Enteries of confusion matrix
    tp <- confusion[2,2];
    tn <- confusion[1,1];
    fp <- confusion[2,1];
    fn <- confusion[1,2];
    
    # Compute total cost formula
    total_cost[i,1] <- (tp * cost_tp) + (tn * cost_tn) + (fn * cost_fn) + (fp * cost_fp);
    confmat[i,1] <- tp;
    confmat[i,2] <- tn;
    confmat[i,3] <- fp;
    confmat[i,4] <- fn;
   }
  # add rownames
  rownames(confmat) <- colnames(P)
  #returns
  return(list(total_cost=total_cost,conf_mat=confmat, orig_conf_mat=confusion));
#  return(total_cost);
}


PlotCostFunction<-function(P, a, cost_matrix, outfile) {
  # This function will plot simple cost fuction specified by the cost parameters i.e., cost_matrix
  # Note that this fucntion will use ROCR package to compute the explicit cost defined by the following formula:
  # explicit cost formula : cost <- ((n.pos / n.samples) * (fn / n.pos) * cost.fn + (n.neg / n.samples) * (fp / n.neg) * cost.fp)
  # For more detial please refer to ROCR package manual
  
  cost_tp = cost_matrix[1,1];
  cost_tn = cost_matrix[2,2];
  cost_fp = cost_matrix[1,2];          
  cost_fn = cost_matrix[2,1];
  
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
    
    tp <- pred@tp[[1]][];
    tn <- pred@tn[[1]][];
    fp <- pred@fp[[1]][];
    fn <- pred@fn[[1]][];
    
    x <- unlist(pred@cutoffs);
    y <- (tp * cost_tp) + (tn * cost_tn) + (fn * cost_fn) + (fp * cost_fp);
    
    
    # Setting y limit
    xlim = range(pretty(c(0, unlist(x) )));
    ylim = range(pretty(c(0, unlist(y) )));
    
    # Plotting cost curves on the same plot
    if (i==1) { plot(x,y,lwd=1.0, type='l', col=colors[i], pch=plotchar[i], ylim = ylim, xlim = xlim); }
    else { line(x,y);}
    # , col=colors[i] 
  }
  legend(par('usr')[2], par('usr')[4],  bty='n', xpd=NA, lty=linetype, col=colors, legend=colnames(P), cex=0.8);
  dev.off();
  return;
}

PlotExpectedCost<-function(costs, outfile) {
  # The method will plot estimated "optimal cost".
  # Input "optimal" is a matrix containing, for each model (row-wise), confusion matrix enteries, optimal cutoff, and optimal cost 
  # Output will be a bar plot showing cost.
  
  df.cost <- data.frame(as.table(costs));
  colnames(df.cost)<- c("models","total_cost");
  
  cost_plot <- ggplot(df.cost, aes(models, total_cost)) +   
    geom_bar(aes(fill = models), position = "dodge", stat="identity") +
    geom_text(aes(label=round(total_cost,2)), position=position_dodge(width=0.9), vjust=-0.25) +
    #coord_cartesian(ylim = c(0, 1)) +
    scale_fill_brewer(palette="Spectral")+
    xlab("Models")+
    ylab("Normaized cost")+
    theme(axis.text.x=element_text(angle=90,hjust=1,vjust=0.5))
  
  plot(cost_plot);
  
  ggsave(filename=outfile, plot=cost_plot);
}

PlotCostPerPrediction<-function(P,a,outfile) {
  # This function will plot normalized total cost per prediction by using the above "compute_optimal_cost" function.
  # - The total cost at "optimal threshold" is given by the "compute_optimal_cost" function defined.
  # - The total cost is then normalized by the number of predictions each model made. 
  # - The x-axis of the plot is log scaled false negative cost
  # - The y-axis of the plot is the normalized total cost at optimal threshold for different cost functions
  # Input parameter P is a prediction matrix, each column represents the predicted probabilites from a model
  # Input paramter a is a vector containing corresponding actual oberved values for the prediction matrix P
  # Note: The number of elements in a should be equal to the row dimention of matrix P. i.e., nrow(P) = length(actual)
  # outfile is to specify the plot file name not including the extention.
  # This method will also provide the txt and txt file for the AUC based ranking.
  
  # Setting false negative cost parameters
  fn_cost_var <- seq(0,1000,by=10);
  fn_cost_var[1] <- 1;
  cost_fp = 1.0;
  
  # Computing the number of prediction for each model
  total_obs = length(actual);
  pred_vec = total_obs - apply(P,2, function(x) sum(is.na(x)));
  NumModels = dim(P)[2];
  
  # Prepare the cost per prediction matrix by using the total cost at "optimal threshold", whose
  # rows are set to the discrete cost variable covering different cost of false neagtives and
  # columns correspond to models in the prediction matrix P.
  mat_cost   = matrix(nrow = length(fn_cost_var), ncol = NumModels, data = NA);
  for(i in 1:length(fn_cost_var)) {
    
    # Total cost at optimal threshold on a given cost of false negative 
    pm <- compute_optimal_cost(P,actual,fn_cost_var[i],cost_fp);
    
    # Normalizing the total cost by the number of prediction each model made
    mat_cost[i,] <-  t( pm[,"cost"] / pred_vec );
    
    # specifying the model name
    colnames(mat_cost) <- rownames(pm);
  }
  rownames(mat_cost) <-fn_cost_var;
  
  # Converting matrix into dataframe
  df.plot <- as.data.frame(as.table(mat_cost));
  df.plot[,1] <- rep(fn_cost_var,times=dim(mat_cost)[2]);
  colnames(df.plot)<-c("fn_cost","models","total_cost");
  df.plot[,2] <- as.factor(df.plot[,2]);
  df.plot[,1] <- as.numeric(log(df.plot[,1]));
  
  
  # Setting the color palette
  qual_col_pals = brewer.pal.info[brewer.pal.info$category == 'qual',]
  col_vector = unlist(mapply(brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))
  #col_vector = grDevices::colors()[grep('gr(a|e)y', grDevices::colors(), invert = T)]
  #col_vector = rainbow(NumModels,s = 0.5);
  #col_vector = brewer.pal(NumModels, "Set3")
  #col_vector = rainbow(NumModels, s=.6, v=.9)[sample(1:NumModels,NumModels)]
  #myPalette = sample(col_vector, NumModels);
  myPalette  = col_vector[1:NumModels];
  
  
  # creating by ggplot object
  cost_plot <-  ggplot(data = df.plot, aes(x=fn_cost, y=total_cost, color=models),group = models) + 
                geom_line(aes(colour=models,linetype=models))+
                scale_color_manual(values=myPalette)+
                ylim(0,1)+
                xlab("Log of false negative cost")+
                ylab("Normaized total cost");
  
  # Saving the ggplot
  file <- paste0(outfile,"_plot", ".pdf");
  ggsave(filename=file, plot=cost_plot);
  
  
  # Reporting the area under the normalized total cost curve to rank the models
  require(MESS);
  auc_vec = apply(mat_cost, 2, function(x)  auc(log(fn_cost_var),x, type = 'spline')   )  ; 
  auc_vec <- sort(auc_vec);
  auc_mat = matrix(nrow = length(auc_vec), ncol = 1, data = auc_vec);
  colnames(auc_mat) <- c("AUC_Cost");
  rownames(auc_mat) <- names(auc_vec);
  
  file <- paste0(outfile,"_rank",".tex");
  stargazer(auc_mat,type='latex',out = file, title="Table: Area under the Normalized total cost curve");
  
  file <- paste0(outfile,"_rank",".txt");
  stargazer(auc_mat,type='text' ,out = file, title="Table: Area under the Normalized total cost curve");
}


# I re-named all the functions to follow the Google R Style guide
# Copies here to not break anyones references
write_performance_table <- WritePerformanceTable
plot_performance <- PlotPerformance
plot_performance_separate <- PlotPerformanceSeparate
plot_EBMA_Weights <- PlotEBMAWeights
plot_EBMA_Weights_Accuracy <- PlotEBMAWeightsAccuracy
performance_hist <- PerformanceHist
performance_combine_hist <- PerformanceCombineHist
compute_optimal_threshold <- ComputeOptimalThreshold
confusion.matrix <- ConfusionMatrix
compute_cost <- ComputeCost
plot_cost_function <- PlotCostFunction
plot_expected_cost <- PlotExpectedCost
plot_cost_per_prediction <- PlotCostPerPrediction
plot_separation <- PlotSeparation
