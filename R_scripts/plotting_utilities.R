# File name: plotting_utilities.r
# Author: H??vard Hegre
#######################################################################
# Scripts to produce various plots for ViEWS
#######################################################################


# Create a 100-step color palette useful for plotting probabilites, going from white through yellow through red #
zerocolor <- colorRampPalette(c(rgb(1,1,1,1), rgb(1,1,1,1)), alpha=TRUE)(1) # One slot of pure white
vlowcolor <- colorRampPalette(c(rgb(1,1,1,1), rgb(1,1,0,1)), alpha=TRUE)(1) # Slot of white to yellow
lowcolor <- colorRampPalette(c(rgb(1,1,0,1), rgb(1,1,0.65,1)), alpha=TRUE)(3) # Slots of yellow to light orange
mediumcolor <- colorRampPalette(c(rgb(1,0.65,0,1), rgb(1,0.35,0,1)), alpha=TRUE)(10) # Slots of light orange - heavy orange
highcolor <- colorRampPalette(c(rgb(1,.35,0,1), rgb(1,0,0,1)), alpha=TRUE)(25) # Slots of heavy orange - red
extremecolor <- colorRampPalette(c(rgb(1,0,0,1), rgb(.25,0,0,1)), alpha=TRUE)(160) # Slots of red - crimson
prob_palette <- c(zerocolor,vlowcolor,lowcolor, mediumcolor,highcolor,extremecolor)
barplot(c(1:200), col=prob_palette)



# Plot predicted proportion with confidence bands
# Sample call: plot_proportion_ci(Cairo.pgm.df,"ns","Cairo", .5)

plot_proportion_ci <- function(dataframe, outcome, location_name, ar) {
  plot <- ggplot(dataframe, aes(x=month_id)) +
    ggtitle(paste(location_name,",",outcome)) +
    ylab(paste("prob. of",outcome)) +
    theme_bw() + theme(aspect.ratio=ar) + 
    geom_ribbon(aes_string(ymin=paste0("p_ged_dummy_", outcome, "_pct10"), ymax=paste0("p_ged_dummy_", outcome, "_pct90")), fill = "grey80") +
    geom_ribbon(aes_string(ymin=paste0("p_ged_dummy_", outcome, "_pct25"), ymax=paste0("p_ged_dummy_", outcome, "_pct75")), fill = "grey60") +
    geom_line(aes_string(y=paste0("p_ged_dummy_", outcome, "_mean")), color = "black", size=.5) +
    ylim(0,1)
  outfile <- paste0(outfile_location, location_name, "_", outcome, "_pgm_proportions.pdf",sep="");
  ggsave(file=outfile, plot=plot)
}


# Function to compute the proportion per each country per each month
compute_proportions <- function(sim.pgm.df,prop_var_name) {
  
  month_wise = unique(sim.pgm.df$month_id);
  #  month_wise = head(month_wise,-4);   # Removing last 4 month
  year_wise  = unique(sim.pgm.df$year_id);
  country_wise = unique(sim.pgm.df$gwcode);
  
  numMonths    <- length(month_wise);
  numYears     <- length(year_wise);
  numCountries <- length(country_wise);
  
  prop = matrix(nrow=numCountries,ncol=numMonths,data=NA);  
  
  col_names <- list();
  for (i in 1:numCountries) {
    for(j in 1:numMonths) {
      
      select.rows = (sim.pgm.df$gwcode == country_wise[i]) & (sim.pgm.df$month_id == month_wise[j]) ;
      
      prop [i,j] = sum( sim.pgm.df[select.rows,prop_var_name]   ) / length(sim.pgm.df[select.rows,]) ;
      #prop [i,j] = sum( sim.pgm.df[select.rows,prop_var_name]   )  ;
      
      m <- unique( sim.pgm.df[select.rows,"month_id"] );
      y <- unique( sim.pgm.df[select.rows,"year_id"]);
      col_names[[j]] <- paste0(y,"/",m);
    }
  }
  colnames(prop) <- unlist(col_names);
  rownames(prop) <- country_wise;
  gwabbs <- c("402 CAP", "403 ???", "404 GNB", "411 EQG", "420 GAM", "432 MLI", 
              "433 SEN", "434 BEN", "435 MAA", "436 NIR", "437 CDI", "438 GUI", 
              "439 BFO", "450 LBR", "451 SIE", "452 GHA", "461 TOG", "471 CAO", "475 NIG", 
              "481 GAB", "482 CEN", "483 CHA", "484 CON", "490 DRC", "500 UGA", "501 KEN", 
              "510 TAZ", "516 BUI", "RWA", "520 SOM", "DJI", "ETH", "ERI", "540 ANG", "MZM", "ZAM", "ZIM", "MAW", "560 SAF", 
              "NAM", "LES", "BOT", "SWA", "580 MAG", "COM", "MAS", "600 MOR", "615 ALG", "616 TUN", "LIB", "625 SUD", "626	SSD", 
              "651	EGY", "666", "670");
  #  rownames(prop) <- gwabbs;
  return(prop);
}

# Plotting heatmap of results where prop is a matrix containing proportions
# rows corresponds to countries and columns corresponds to month/year code
plot_heatmap <- function(prop,outfile) { 
  
  sim.pgm.df.plot <- data.frame(Countries = row.names(prop) , prop);
  numMonths <- dim(prop)[2];
  
  names(sim.pgm.df.plot)[2:(numMonths+1)] <- colnames(prop);
  sim.pgm.df_heatmap <- melt(sim.pgm.df.plot, id.vars = "Countries");
  names(sim.pgm.df_heatmap)[2:3] <- c("Time", "Proportions");
  
  #labels <- c("0","","","0.01","0.02","0.05","0.1","1")
  myPlot<-ggplot(sim.pgm.df_heatmap, aes(Time, Countries)) +
    geom_tile(aes(fill = Proportions), color = "lightgray") +
    scale_fill_gradientn(colors=prob_palette, limits=c(0,1)) +  
    ylab("Country") +
    xlab("Time") +
    theme(legend.title = element_text(size = 10),
          legend.text = element_text(size = 12),
          plot.title = element_text(size=16),
          axis.title=element_text(size=14,face="bold"),
          axis.text.x = element_text(angle = 90, hjust = 1)) +
    labs(Fmeasure = "Proportions");
  
  ggsave(filename=outfile, plot=myPlot);
}


# Function for customizing ggplot to show accuracy as a function of time (month wise)
my_ggplot <- function(time,measure,xlabel,ylabel,outfile) {
  sim.pgm.df.plot <- data.frame (time=time,measure=measure); 
  n <- length(time);
  line_color <- "red";
  ylim = range(pretty(c(0, measure)));
  
  plt <- ggplot(data=sim.pgm.df.plot, aes(x=reorder(time,1:n), y=measure, group=1))+
    scale_y_continuous(limits =ylim )+
    xlab(xlabel)+
    ylab(ylabel)+
    geom_line(color=line_color)+
    theme(axis.text.x = element_text(angle = 90, hjust = 1))+
    geom_point()
  ggsave(filename=outfile, plot=plt);
}


my_ggplot_levels <- function(level_pm,measure_name,outfile) {
  
  conflict_levels <- names(level_pm);
  time <- c();
  type <- c();
  measure <- c();
  for (level in  conflict_levels) {
    
    pm <-  level_pm[[level]];
    t  <-  row.names(pm);
    time <- c(time, t);
    type <- c(type, rep(level,length(t)));
    measure <- c(measure, pm[,measure_name]);
  }
  
  sim.pgm.df.plot <- data.frame (time=time,measure=measure,conflict_type=as.factor(type)); 
  
  xlabel <- "time";
  ylabel <- measure_name;
  ylim   <- range(pretty(sim.pgm.df.plot$measure));
  
  plt <- ggplot(data=sim.pgm.df.plot, aes(x=time, y=measure, group = conflict_type)) +
    geom_line(aes(colour = conflict_type)) +
    geom_point( size=1, shape=21, fill="white") +
    theme(axis.text.x = element_text(angle = 90, hjust = 1))+
    xlab(xlabel)+
    ylab(ylabel) +
    scale_y_continuous(limits=ylim)
  
  #plot(plt);
  ggsave(filename=outfile, plot=plt);
}



 
