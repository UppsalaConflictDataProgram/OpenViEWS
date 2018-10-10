## Miscellaneous utilities
## RBJ 2-11-2017

# To do:
# - Water cells 
# - Fixed probability distribution plot
# - color coding set to country names

## Required libraries
if (!require("pacman")) install.packages("pacman")
pacman::p_load(ggplot2, cshapes, rgdal, maptools, classInt, broom, ggthemes)

###############################
## Function to add date columns
###############################

add_yearcolumns <- function(df, yearlabel, ymlabel) {
  # Args:
  #   df:         Dataframe to add the columns to.
  #   yearlabel:  Label for year column (optional). Default is "year".
  #   ymlabel:    Label for the year-month column (optional). Default is "date_id".
  # Returns:
  #   The dataframe with added columns.
  
  # Set up identifier
  month_id <- 109:700   
  year <- c()
  base_year <- 1988
  for (i in month_id) {
    month_count <- rep(1:12, length(month_id), length.out = length(month_id))
    if (i %% 12 == 0 + 1) {
      base_year = base_year + 1
      year <- append(year, base_year)
    } else {
      year <- append(year, base_year)
    }
  }
  
  date_id <- paste(year, month_count, sep = "-")
  date_identifier <- cbind(month_id, year, date_id)
  
  # Merge with input dataframe
  out <- merge(df, date_identifier, by = "month_id")
  
  # Redo factor levels
  out$year <- factor(out$year)
  out$date_id <- factor(out$date_id)
  
  # Optional argument 1
  if (!missing(yearlabel)){
      colnames(out)[names(out) == "year"] <- paste(yearlabel)
  }
  
  # Optional argument 2
  if (!missing(yearlabel)){
      colnames(out)[names(out) == "date_id"] <- paste(ymlabel)
  }
  
  return(out)
}

##############################################################
## Function to plot time series of probability level frequency
##############################################################

plot_pfreq <- function(df, varid, lvl) {
  # Args:
  #   df:     Dataframe that holds the variable to assess.
  #   varid:  Variable to assess over dataframe's months.
  #   lvl:    Level of probability (0-1).
  # Returns:
  #   Plot of associated frequencies per month in df. 
  
  # Subset input dataframe
  at_risk <- subset(df, varid >= lvl)
  
  # Calculate the frequencies
  count_probs <- count(at_risk, month_id)
  count_probs_ym <- add_yearcolumns(count_probs)
  count_probs_ym$date_id <- factor(count_probs_ym$date_id, levels = unique(count_probs_ym$date_id))

  # Plot
  plevelfreq <- ggplot(count_probs_ym, aes(date_id, n, group = 1)) +
    geom_line(colour = "grey") +
    geom_point() +
    labs(title = paste(sub('.*\\$',"", deparse(substitute(varid))), " >= ", deparse(substitute(lvl))),  x = "Date ID", y = "Frequency") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1)) 
  
  return(plevelfreq)
}

###############################################################
## Function to display spatial lag function in a specified area
###############################################################

compute_areavalues <- function(df, m, var_name, startrow, endrow, startcol, endcol) {
  # Args:
  # Note! Length of rows and columns needs to be equal. Also needs a solution for non-land cells.
  #
  #   df:       Dataframe that holds the variable to assess.
  #   m:        Number month_id to assess.
  #   varname:  Variable to assess.
  #   startrow: The starting prio grid row (>=). 
  #   endrow:   The ending prio grid row (<=).
  #   startcol: The starting prio grid col (>=).
  #   endcol:   The ending prio grid col (<=).
  # Returns:
  #   Heatmap for the variable values over the specified prio grid area.
  
  # Subset area
  area <- subset(df, row >= startrow & row <= endrow & col >= startcol & col <= endcol)
  
  # Subset month
  month_identifier <- m
  set_month <- area[area$month_id == month_identifier,]
  
  # Put in rows and cols
  col_wise = unique(set_month$col)
  col_wise = sort(as.numeric(as.character(col_wise)))
  row_wise = unique(set_month$row)
  row_wise = sort(as.numeric(as.character(row_wise)))
  numCols <- length(col_wise)
  numRows <- length(row_wise)
  
  # Produce matrix
  varid = paste0(sub('.*\\$',"", deparse(substitute(var_name))))
  loc = paste0("set_month$", varid)
  out = t(matrix(nrow = numRows, ncol = numCols, data = eval(parse(text = loc)))) 
  
  # Add labels
  colnames(out) <- c(col_wise)
  rownames(out) <- c(row_wise)
  
  # Reshape data for ggplot
  melt_out <- melt(out)
  melt_out$Var1 <- factor(melt_out$Var1, levels = (unique(melt_out$Var1)))
  melt_out$Var2 <- factor(melt_out$Var2, levels = (unique(melt_out$Var2)))
  
  # Plot data
  output <- ggplot(melt_out, aes(Var2, Var1)) +
    geom_tile(aes(fill = value)) + 
    geom_text(aes(label = round(value, 1))) +
    scale_fill_gradient(low = "white", high = "orange") +
    scale_x_discrete(expand=c(0,0)) +
    scale_y_discrete(expand=c(0,0), limits = rev(levels(melt_out$Var1))) +
    labs(x = "grid col", y = "grid row", title = paste(sub('.*\\$',"", deparse(substitute(var_name))), "for month", m)) +
    theme_bw()
    
  return(output)
}

##############################################################
## Function to produce ggplot world map for specified variable
##############################################################

# Use set.seed to get consistent coloring

plot_world <- function(mapdate, df, var_name) {
  # Args:
  #   mapdata:    The date of the required cshape map in a string (ex: "2015-1-1").
  #   df:         Dataframe that holds the variable to plot and the gwno.
  #   var_name:   Variable to plot (ex: "knn_clusters")
  # Returns:
  #   Continuous or categorical variable plotted on world map.
  
  # Geospatial data
  world <- cshp(date = as.Date(mapdate))
  world@data$id <- rownames(world@data)
  world.df <- tidy(world)
  world.df$arrange <- 1:192762 
  world.df <- join(world.df, world@data, by = "id") 
  
  # Data to map
  map.data <- subset(df, select = c("gwno", var_name)) 
  o <- match(world$GWCODE, map.data$gwno)
  map.data <- map.data[o,]
  row.names(map.data) <- world$FEATUREID
  colnames(map.data)[names(map.data) == "gwno"] <- "GWCODE"
  world.df <- join(world.df, map.data, by = "GWCODE")
  world.df <- arrange(world.df, arrange)
  
  # Set up color scheme
  numcolors <- length(unique(map.data[,2]))
  color = grDevices::colors()[grep('gr(a|e)y', grDevices::colors(), invert = T)]
  col = sample(color, numcolors) # for random color schemes
  
  # Plot the map (takes a couple seconds),  distinguishing continuous from categorical
  if (is.numeric(df[, var_name])) {
    
    ggplot() +
      geom_polygon(data = world.df, aes(x = long, y = lat, group = group, fill = eval(parse(text = var_name)))) +
      coord_equal() +
      theme(
        panel.background = element_rect(fill = "white"),
        plot.background = element_rect(fill = "white"),
        axis.line = element_blank(), axis.text = element_blank(), 
        axis.ticks = element_blank(), axis.title = element_blank(), 
        panel.border = element_blank(), 
        panel.grid.major = element_blank(), panel.grid.minor = element_blank()
      ) +
      labs(fill = "Value", title = paste("Values for", sub('.*\\$',"", deparse(substitute(var_name)))))
    
  } else {
    
    ggplot() +
      geom_polygon(data = world.df, aes(x = long, y = lat, group = group, fill = factor(eval(parse(text = var_name))))) +
      coord_equal() +
      theme(
        panel.background = element_rect(fill = "white"),
        plot.background = element_rect(fill = "white"),
        axis.line = element_blank(), axis.text = element_blank(), 
        axis.ticks = element_blank(), axis.title = element_blank(), 
        panel.border = element_blank(), 
        panel.grid.major = element_blank(), panel.grid.minor = element_blank()
      ) +
      scale_fill_manual(values = col) +
      labs(fill = "Clusters", title = paste("Clustering per", sub('.*\\$',"", deparse(substitute(var_name)))))
  }
}

#############################################
## Function to set up stylecodes in dataframe
#############################################

style_code <- function(df, name) {
  # Args:
  #   df:     Dataframe to add stylecodes per country to.
  #   name:   List of names of the countries you want to distinguish in a ggplot.    
  # Returns:
  #   A column 'stylecode' providing a unique number for countries to distinguish in a ggplot.
  
  # set up stylecodes
  stylecode <- 1:length(name)
  styledf <- data.frame(name, stylecode)
  df <- merge(df, styledf, by = "name", all = TRUE) # make all others zero
  df$stylecode[is.na(df$stylecode)] <- 0
                
  return(df)
}

#################################################
## Grid arrange function to plot multiple ggplots
#################################################

grid_arrange_shared_legend <- function(..., nrow = 1, ncol = length(list(...)), position = c("bottom", "right")) {
  
  plots <- list(...)
  position <- match.arg(position)
  g <- ggplotGrob(plots[[1]] + theme(legend.position = position))$grobs
  legend <- g[[which(sapply(g, function(x) x$name) == "guide-box")]]
  lheight <- sum(legend$height)
  lwidth <- sum(legend$width)
  gl <- lapply(plots, function(x) x + theme(legend.position = "none"))
  gl <- c(gl, nrow = nrow, ncol = ncol)
  combined <- switch(position, "bottom" = arrangeGrob(do.call(arrangeGrob, gl), legend, ncol = 1, heights = unit.c(unit(1, "npc") - lheight, lheight)),
                     "right" = arrangeGrob(do.call(arrangeGrob, gl), legend, ncol = 2, widths = unit.c(unit(1, "npc") - lwidth, lwidth)))
  
  grid.newpage()
  grid.draw(combined)
}

#####################################################
## Function to produce a spaghetti plot of masterdata
#####################################################

spaghetti_machine <- function(df, var_name) {
  
  spaghetti <- ggplot(data = df) +
    geom_line(aes(year, eval(parse(text = var_name)), group = name, color = stylecode, 
                  size = stylecode)) +
    scale_color_manual("", values = col, labels = clabels) +
    scale_size_manual("", values = ifelse(col == "lightgrey", .3, 1), 
                      labels = clabels) +
    labs(x = "", y = "", title = paste("Spaghetti plot: ", deparse(substitute(var_name))),
         color = "") +
    theme_bw() + 
    theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(), 
          axis.text.y = element_text(size = rel(ticksize)), 
          axis.text.x = element_text(size = rel(ticksize)),
          legend.text=element_text(size= rel(legendsize)), 
          aspect.ratio = lineaspect) 
  
  return(spaghetti)
  
}



########################################### Testing #######################################

# Use set.seed to get consistent coloring

plot_world <- function(mapdate, df, var_name) {
  # Args:
  #   mapdata:    The date of the required cshape map in a string (ex: "2015-1-1").
  #   df:         Dataframe that holds the variable to plot and the gwno.
  #   var_name:   Variable to plot (ex: "knn_clusters")
  # Returns:
  #   Continuous or categorical variable plotted on world map.
  
  # Geospatial data
  world <- cshp(date = as.Date(mapdate))
  world@data$id <- rownames(world@data)
  world.df <- tidy(world)
  world.df$arrange <- 1:192762 
  world.df <- join(world.df, world@data, by = "id") 
  
  # Data to map
  map.data <- subset(df, select = c("gwno", var_name)) 
  o <- match(world$GWCODE, map.data$gwno)
  map.data <- map.data[o,]
  row.names(map.data) <- world$FEATUREID
  colnames(map.data)[names(map.data) == "gwno"] <- "GWCODE"
  world.df <- join(world.df, map.data, by = "GWCODE")
  world.df <- arrange(world.df, arrange)
  
  # Set up color scheme - "cornsilk", "darkseagreen3", "cadetblue3", "deepskyblue3", "lightblue1", "lightseeblue", "navajowhite7", "gray67"
  numcolors <- length(unique(map.data[,2]))
  pal <- palette(c("moccasin", "darkseagreen3", "cadetblue3", "deepskyblue3", "navajowhite4"))
  color = grDevices::colors()[grep('gr(a|e)y', grDevices::colors()[palette(c("moccasin", "darkseagreen3", "cadetblue3", "deepskyblue3", "navajowhite4"))], invert = T)]
  col = palette(c("moccasin", "navajowhite4", "cadetblue3", "deepskyblue3"))
  
  # Plot the map (takes a couple seconds),  distinguishing continuous from categorical
  if (is.numeric(df[, var_name])) {
    
    ggplot() +
      geom_polygon(data = world.df, aes(x = long, y = lat, group = group, fill = eval(parse(text = var_name)))) +
      coord_equal() +
      theme(
        panel.background = element_rect(fill = "white"),
        plot.background = element_rect(fill = "white"),
        axis.line = element_blank(), axis.text = element_blank(), 
        axis.ticks = element_blank(), axis.title = element_blank(), 
        panel.border = element_blank(), 
        panel.grid.major = element_blank(), panel.grid.minor = element_blank()
      ) +
      labs(fill = "Value", title = paste("Values for", sub('.*\\$',"", deparse(substitute(var_name)))))
    
  } else {
    
    ggplot() +
      geom_polygon(data = world.df, aes(x = long, y = lat, group = group, fill = factor(eval(parse(text = var_name))))) +
      coord_equal() +
      theme(
        panel.background = element_rect(fill = "white"),
        plot.background = element_rect(fill = "white"),
        axis.line = element_blank(), axis.text = element_blank(), 
        axis.ticks = element_blank(), axis.title = element_blank(), 
        panel.border = element_blank(), 
        panel.grid.major = element_blank(), panel.grid.minor = element_blank()
      ) +
      scale_fill_manual(values = col) +
      labs(fill = "Clusters", title = paste("Clustering per", sub('.*\\$',"", deparse(substitute(var_name)))))
  }
}

