# File name: plotting_utilities_rb.R
# Author: RBJ
#######################################################################
# Scripts to produce various plots for ViEWS
#######################################################################


# Create a 100-step color palette useful for plotting probabilites, going from white through yellow through red #
#zerocolor <- colorRampPalette(c(rgb(127,80,252,1), rgb(1,1,1,1)), alpha=TRUE)(1) # One slot of pure white
#vlowcolor <- colorRampPalette(c(rgb(1,1,1,1), rgb(1,1,0,1)), alpha=TRUE)(1) # Slot of white to yellow
#lowcolor <- colorRampPalette(c(rgb(1,1,0,1), rgb(1,1,0.65,1)), alpha=TRUE)(3) # Slots of yellow to light orange
#mediumcolor <- colorRampPalette(c(rgb(1,0.65,0,1), rgb(1,0.35,0,1)), alpha=TRUE)(10) # Slots of light orange - heavy orange
#highcolor <- colorRampPalette(c(rgb(1,.35,0,1), rgb(1,0,0,1)), alpha=TRUE)(25) # Slots of heavy orange - red
#extremecolor <- colorRampPalette(c(rgb(1,0,0,1), rgb(.25,0,0,1)), alpha=TRUE)(160) # Slots of red - crimson
#prob_palette <- c(zerocolor,vlowcolor,lowcolor, mediumcolor,highcolor,extremecolor)
#barplot(c(1:200), col=prob_palette)

# change to reflect changes at lower end
vlowcolor <- colorRampPalette(c(rgb(127,80,252, maxColorValue = 255), rgb(85,194,231, maxColorValue = 255)), alpha=TRUE)(10) # Slot purple to cyan
lowcolor <- colorRampPalette(c(rgb(85,194,231, maxColorValue = 255), rgb(181,241,147, maxColorValue = 255)), alpha=TRUE)(10) # Slots of cyan to green
lowmedcolor <- colorRampPalette(c(rgb(181,241,147, maxColorValue = 255), rgb(236,200,110, maxColorValue = 255)), alpha=TRUE)(10) # Slots of green to yellow
mediumcolor <- colorRampPalette(c(rgb(236,200,110, maxColorValue = 255), rgb(239,137,70, maxColorValue = 255)), alpha=TRUE)(10) # Slots of yellow to orange
highcolor <- colorRampPalette(c(rgb(239,137,70, maxColorValue = 255), rgb(233,63,51, maxColorValue = 255)), alpha=TRUE)(60) # Slots of orange - red
prob_palette <- c(vlowcolor,lowcolor, lowmedcolor, mediumcolor,highcolor)
barplot(c(1:100), col=prob_palette)


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


######################################################################
## Function to compute the proportion per each country per each month
######################################################################

compute_proportions <- function(sim.pgm.df,prop_var_name) {
  
  sim.pgm.df = eval.df
  sim.pgm.df <- sim.pgm.df[order(sim.pgm.df$month_id),]
  
  month_wise = unique(sim.pgm.df$month_id);
  #  month_wise = head(month_wise,-4);   # Removing last 4 month
  year_wise  = unique(sim.pgm.df$year);
  country_wise = unique(sim.pgm.df$gwno);
  country_name = unique(sim.pgm.df$name);
  
  numMonths    <- length(month_wise);
  numYears     <- length(year_wise);
  numCountries <- length(country_wise);
  
  prop = matrix(nrow=numCountries,ncol=numMonths,data=NA);  
  
  col_names <- list();
  for (i in 1:numCountries) {
    for(j in 1:numMonths) {
      
      select.rows = (sim.pgm.df$gwno == country_wise[i]) & (sim.pgm.df$month_id == month_wise[j]) ;
      # "nrow" formerly "length", but that provides the number of variables, not observations!
      prop [i,j] = sum( sim.pgm.df[select.rows,prop_var_name]   ) / nrow(sim.pgm.df[select.rows,]) ;
      #prop [i,j] = sum( sim.pgm.df[select.rows,prop_var_name]   )  ;
      
      m <- unique( sim.pgm.df[select.rows,"month_id"] );
      y <- unique( sim.pgm.df[select.rows,"year"]);
      ym <- unique(sim.pgm.df[select.rows, "date_id"])
      col_names[[j]] <- paste0(ym)
      #col_names[[j]] <- paste0(y,"/",m);
    }
  }
  colnames(prop) <- unlist(col_names);
  #rownames(prop) <- country_wise;
  rownames(prop) <- country_name;
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


############################################################################
## Plotting heatmap of results where prop is a matrix containing proportions
############################################################################

plot_heatmap <- function(prop,outfile) { 
  
  sim.pgm.df.plot <- data.frame(Countries = row.names(prop) , prop, check.names = FALSE);
  
  # reverse country order
  sim.pgm.df.plot$Countries = factor(sim.pgm.df.plot$Countries, levels = rev(levels(sim.pgm.df.plot$Countries)))
  numMonths <- dim(prop)[2];
  
  names(sim.pgm.df.plot)[2:(numMonths+1)] <- colnames(prop);
  sim.pgm.df_heatmap <- melt(sim.pgm.df.plot, id.vars = "Countries");
  names(sim.pgm.df_heatmap)[2:3] <- c("Time", "Proportions");
  
  #bump up
  sim.pgm.df_heatmap$Proportions[sim.pgm.df_heatmap$Proportions<log(0.001/(1-0.001))] <- log(0.001/(1-0.001))
  
  #labels <- c("0","","","0.01","0.02","0.05","0.1","1")
  myPlot<-ggplot(sim.pgm.df_heatmap, aes(Time, Countries)) +
    geom_tile(aes(fill = Proportions), color = "lightgray") +
    scale_fill_gradientn(colors=prob_palette,
                         breaks=c(log(0.005/(1-0.005)), 
                                  log(0.05/(1-0.05)), log(0.40/(1-0.40)),
                                  log(0.90/(1-0.90)), log(0.99/(1-0.99))),
                         labels=c("0.5%", "5%", "40%", "90%", "99%"),
                         limits=c(log(0.001/(1-0.001)), log(0.99/(1-0.99))),
                         name = "Proportions\n") +  
    ylab("") +
    xlab("") +
    theme(legend.title = element_text(size = 10),
          legend.text = element_text(size = 8),
          plot.title = element_text(size=16),
          axis.title=element_text(size=14,face="bold"),
          axis.text.x = element_text(angle = 90, hjust = 1),
          axis.text.y = element_text(size = 8)) + #adjust
    #scale_x_discrete(breaks = c()) #adjust
    labs(Fmeasure = "Proportions");
  
  ggsave(filename=outfile, plot=myPlot);
  return(myPlot)
}


#####################################################################################
## Function for customizing ggplot to show accuracy as a function of time (month wise)
#####################################################################################

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


#########################
## sim measure over time
#########################

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


#############################################
## Lineplot for proportions per countrynames
#############################################

prop_lineplot <- function(prop, sim.df, countrynames, out){
  # Args:
  #   prop: Matrix of proportions produced by compute_proportions() function.
  #   countrynames: Vector of names of the countries you want to compare.  
  #   sim.df: Data with countrynames used in compute_proportions()
  #   out: String name you want to give the output.
  # Returns:
  #   A lineplot for selected countries. Automatic axes.
  
  # create regular dataframe for plot
  sim.pgm.df.plot <- data.frame(Countries = row.names(prop) , prop, check.names = FALSE);
  numMonths <- dim(prop)[2];
  names(sim.pgm.df.plot)[2:(numMonths+1)] <- colnames(prop);
  sim.pgm.df_plot <- melt(sim.pgm.df.plot, id.vars = "Countries");
  names(sim.pgm.df_plot)[2:3] <- c("Time", "Proportions");

  # subset for plot
  sim.pgm.df_plot <- sim.pgm.df_plot[sim.pgm.df_plot$Countries %in% countrynames,]

  # order by month_id (maybe make separate file for monthid merges)
  monthids <- subset(sim.df, select = c(month_id, date_id))
  monthids <- monthids[!duplicated(monthids), ]
  colnames(monthids)[2] <- "Time"
  sim.pgm.df_plot <- merge(sim.pgm.df_plot, monthids, by = "Time")
  sim.pgm.df_plot <- sim.pgm.df_plot[order(sim.pgm.df_plot$month_id),]

  # adjust types
  sim.pgm.df_plot$Countries <- as.character(sim.pgm.df_plot$Countries)
  sim.pgm.df_plot$Time <- as.character(sim.pgm.df_plot$Time)
  xlabels = unique(sim.pgm.df_plot$Time)

  # plot, using integer monthid
  lineplot <- ggplot(sim.pgm.df_plot) +
    geom_line(aes(month_id, Proportions, color = Countries), size = 1) +
    scale_x_continuous(breaks = unique(sim.pgm.df_plot$month_id), 
                       labels = xlabels, expand = c(0, 0)) +
    xlab("") +
    theme_bw() +
    theme(panel.grid.minor.x = element_blank(),
          panel.grid.minor.y = element_blank(),
          panel.grid.major.x = element_blank(),
          axis.text.x = element_text(angle = 90, hjust = 1))

  ggsave(filename=out, plot=lineplot)
  return(lineplot)
}
 
