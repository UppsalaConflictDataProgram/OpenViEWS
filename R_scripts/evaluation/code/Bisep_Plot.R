#'Function to create Bi-Separation plot for comparing two models
#'
#'Creates an object to be rendered with "grid.draw()" command
#'
#'@param f1 Vector of forecasts from model 1
#'@param f2 Vector of forecasts from model 2
#'@param y Vector of actual outcomes
#'@param labels Vector of labels per observation
#'@param bestN max num. of "most improved" obs you want labeled per model
#'@param label_spacing = distance between labels
#'@param right_lab_adjust how far from the end of line do you want label? Usually small; default is 0.02
#'@param bottom_lab_adjust how far from end of line do you want label?Usually small; default is 0.03
#'@param right_margin how much whitespace needed on right side of plot? For if labels don't fit; default is 5
#'@param bottom_margin how much whitespace needed on bottom of plot? For if labels don't fit; default is 5
#'@param top_margin how much whitespace needed on top of plot? For if labels don't fit; default is 1
#'@param transp_adjust float from [0,10] to adjust opacity of non-labeled points. Default is 1. Generally on the extremes (1 vs 10). 0 will render them extremely light
#'@param hlines True/False whether you want faded lines horizontally pointing from M2 separation plot to most improved observations. Default is TRUE.
#'@param vlines True/False whether you want faded lines vertically pointing from M1 separation plot to most improved observations. Default is TRUE.
#'@param bw True/False whether you would like a rendition of the plot adjusted for visibility in black and white (lighter blue and darker red). Default is FALSE.
#'@param rare True/False whether you have an excessive number of zeros. Adjusts coloring for visibility. Default is FALSE
#'
#'@return Object to be plotted with "grid.draw()' function
#'
#'@import ggplot2
#'@import dplyr
#'@import grid
#'@import gridExtra
#'
#'@export
#'
BicepPlot <- function(f1, f2, y, labels, bestN=10, label_spacing=10,right_lab_adjust=0.02,bottom_lab_adjust=0.03,right_margin=5,bottom_margin=5,top_margin=1,transp_adjust=10, m1title="Model 1", m2title="Model 2", hlines=TRUE,vlines=TRUE,bw=FALSE,rare=FALSE) {
  
  ######################
  #Code
  ######################	
  data <- data.frame(f1=f1, f2=f2, y=y, labels=labels)
  
  pdata <- data %>% arrange(f1) %>% mutate(forecastOrder1 = row_number())
  pdata <- pdata %>% arrange(f2) %>% mutate(forecastOrder2 = row_number()) 
  pdata <- pdata %>% mutate(fdiff=forecastOrder2-forecastOrder1) %>% arrange(fdiff)
  
  
  ###########################
  #Label the worst N for m1 and m2
  ###########################
  
  #########
  #model 1, labels worstN given y=0, and given y=1
  #########
  
  #label best, given y==1
  pdata <- pdata %>% arrange(fdiff) %>% arrange(-y) %>% mutate(isbestn_m1_y1=ifelse(row_number()<=bestN & fdiff<0,1,0))
  
  #label best, given y==0
  pdata <- pdata %>% arrange(-fdiff) %>% arrange(y) %>% mutate(isbestn_m1_y0=ifelse(row_number()<=bestN & fdiff>0,1,0))
  
  #create "label_best_m1" based on those
  pdata <- pdata %>% mutate(label_best_m1= ifelse(isbestn_m1_y0==1 | isbestn_m1_y1==1, as.character(labels)," "))
  
  #########
  #model 2, same as above
  #########
  
  #label and color best, given y==1
  pdata <- pdata %>% arrange(-fdiff) %>% arrange(-y) %>% mutate(isbestn_m2_y1=ifelse(row_number()<=bestN & fdiff>0,1,0)) 
  
  #label best, given y==0
  pdata <- pdata %>% arrange(fdiff) %>% arrange(y) %>% mutate(isbestn_m2_y0=ifelse(row_number()<=bestN & fdiff<0,1,0))
  
  #create "label_best_m2" based on those
  pdata <- pdata %>% mutate(label_best_m2= ifelse(isbestn_m2_y0==1 | isbestn_m2_y1==1, as.character(labels)," "))
  
  N=nrow(pdata)
  ############
  #Now we need to set up colors for plot
  ############
  
  ####
  #label "best n" for both models
  ####
  pdata$transp[pdata$isbestn_m2_y0==1 | pdata$isbestn_m1_y0==1]<-1
  pdata$transp[pdata$isbestn_m2_y0==0 & pdata$isbestn_m1_y0==0 & pdata$y==0]<-0+(.1*transp_adjust)
  pdata$transp[pdata$isbestn_m2_y1==1 | pdata$isbestn_m1_y1==1]<-1
  pdata$transp[pdata$isbestn_m2_y1==0 & pdata$isbestn_m1_y1==0 & pdata$y==1]<-0+(.1*transp_adjust)
  
  ####
  #1. if either m2 or m1 is "best", and y=0
  #2. if neither m2 nor m1 is "best", and y=0
  #3. if either m2 or m1 is "best" and y=1
  #4. if neither m2 nor m1 is "best" and y=1
  ####
  
  pdata$coloring[pdata$isbestn_m2_y0==1 | pdata$isbestn_m1_y0==1]<-'0b'
  pdata$coloring[pdata$isbestn_m2_y0==0 & pdata$isbestn_m1_y0==0 & pdata$y==0]<-'0'
  pdata$coloring[pdata$isbestn_m2_y1==1 | pdata$isbestn_m1_y1==1]<-'1b'
  pdata$coloring[pdata$isbestn_m2_y1==0 & pdata$isbestn_m1_y1==0 & pdata$y==1]<-'1'
  
  #Colors
  if(transp_adjust==0){
    y0_litecol<-ifelse(bw==F,'#f5f8fc',"#d8d8d8")
    yredlite<-ifelse(bw==F,'#fecfdc','#999999')
    yredliteR<-ifelse(bw==F,'#fd5950','#4c4c4c')
    y1_litecol<-ifelse(rare==TRUE,yredliteR,yredlite)
  } else {
    y0_litecol<-ifelse(bw==F,'#cddff4','#f3f3f3')
    yredlite<-ifelse(bw==F,'#fecfdc','#999999')
    yredliteR<-ifelse(bw==F,'#fd5950','#4c4c4c')
    y1_litecol<-ifelse(rare==TRUE,yredliteR,yredlite)
  }
  yblue=ifelse(bw==F,'#0862ca','#8b8b8b')
  yred=ifelse(bw==F,'#fd1205','#000000')
  ybluelitest=ifelse(bw==F,'#f0f5fb','#f2f2f2')
  yredlitest=ifelse(bw==F,'#fef0f4','#e5e5e5')
  boolcolors<-as.character(c(
    '0'= y0_litecol, #very light blue
    '0b'=yblue, #bold blue
    '1'= y1_litecol, #very light red
    '1b'=yred)) #bold red
  boolscale<-scale_color_manual(name='coloring',values=boolcolors)
  
  ##############
  #Arrange by model 2 for lines/labels
  ##############
  pdata<- pdata %>% arrange(forecastOrder2)
  
  
  ###################
  #initialize plots.
  #	Object "o2" contains the full plot we care about,
  #		minus the lines & labels. 
  ###################
  o1 <- ggplot(pdata, aes(x=forecastOrder1,y=forecastOrder2,color=as.factor(coloring),group=y))+boolscale
  mart=F
  o2 <- o1+geom_point(aes(alpha=((transp))))+geom_rug(sides="br")+geom_abline(intercept=0,slope=1)+xlim(c(0,nrow(pdata)))+ylim(c(0,nrow(pdata)))+theme_bw()+theme(plot.title=element_text(size=rel(1)),legend.position='none',plot.margin=unit(c(top_margin,right_margin,bottom_margin,1),'lines'),axis.title.x=element_blank(),axis.ticks.x=element_blank(),axis.text.x=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(),axis.ticks.y=element_blank(),axis.text.y=element_blank())+labs(y=m2title)+boolscale+ggtitle(m1title)+
    theme(plot.title=element_text(size=rel(.7),hjust=0.5), axis.title=element_text(size=rel(.7)))
  
  ###################
  #1.		Model 2 bestN
  ###################	
  z<-o2
  count=0
  for (i in 1:length(pdata$label_best_m2)) {
    
    if(pdata$label_best_m2[i]==" ") {
      next
    }
    ###############################
    #for the lines
    ###############################
    
    obsy=pdata$y[i]
    label_spacing=label_spacing
    
    #set the first erroneous obs to a flat line
    #	since the next code adds "label_spacing",
    #	I subtract it out here so it'll end up
    #	a flat line.
    #
    #Provides a baseline using previous text
    #	for this current label's position
    
    if(count==0) {
      yinit<-pdata$forecastOrder2[i]-label_spacing
    } else {
      yinit<-ypos_text
    }						
    
    #####	
    #calculate 2nd y-point for every line
    #	note that the first one will be
    #	completely horizontal, 
    #####
    
    ypos_text<-yinit+label_spacing
    count=count+1
    
    #####
    #Determine whether you'll have a negative slope
    #	pointing from FO2 down to label, or a 
    #	positive slope pointing from label up to
    #	the FO2. 
    #####
    
    if(pdata$forecastOrder2[i]>ypos_text) {
      LineSlope<-c(1,0)
    } else {
      LineSlope<-c(0,1)
    }
    
    #Coloring for y
    #yblue<-ifelse(bw==F,'blue','#fee8c8')
    #yred<-ifelse(bw==F,'red','#e34a33')
    ycolor<-ifelse(obsy==0,yblue,yred)	
    ###############################
    #Create the labels on plot
    ###############################
    labeltext<-pdata$label_best_m2[i]
    labjust_left<-1.1
    labjust_right<-right_lab_adjust
    
    current<-
      z+
      annotation_custom(
        grob=textGrob(label=labeltext,
                      x=labjust_left+labjust_right,
                      gp=gpar(col=ycolor,fontsize=7)
        ),
        ymin=ypos_text,
        ymax=ypos_text,
      )+
      annotation_custom(
        grob=linesGrob(
          x=c(1,labjust_left),
          y=LineSlope,
          gp=gpar(col=ycolor),
        ),
        
        #need to constrain min & max y to 
        #	either observed or label position,
        #	depending on direction of slope
        ymin=ifelse(y[i]==0,ypos_text,pdata$forecastOrder2[i]),
        ymax=ifelse(y[i]==0,pdata$forecastOrder2[i],ypos_text),
      )
    
    ###########################
    #Decide whether to add horizontal pointer lines
    ###########################
    hcol<-ifelse(obsy==0,ybluelitest,yredlitest)
    if(hlines==TRUE){
      current_fin<-current+
        annotation_custom(
          grob=linesGrob(
            x=c(0,1),
            y=LineSlope,
            gp=gpar(col=ifelse(mart==F,hcol,ycolor)),
          ),
          ymin=pdata$forecastOrder2[i],
          ymax=pdata$forecastOrder2[i],
          xmin=ifelse(mart==F,pdata$forecastOrder1[i],0)
        )
    } else {
      current_fin<-current
    }
    
    z<-current_fin
  }
  
  pdata <- pdata %>% arrange(forecastOrder1)	
  #########################
  #2. 	Model 1 bestN
  #########################
  
  z2<-z
  count=0
  
  for (i in 1:length(pdata$label_best_m1)) {
    
    ##################################
    #If it's not a worstN, pass it
    ##################################
    
    if(pdata$label_best_m1[i]==" ") {
      next
    }
    
    ###############################
    #for the labels
    ###############################
    
    obsy=pdata$y[i]
    
    #
    #Set the baseline: first label should be
    #	directly under the FOpoint.
    #
    
    if(count==0) {
      xinit<-pdata$forecastOrder1[i]-label_spacing
    } else { #store the previous position so we can tack on space
      xinit<-hpos_text
    }
    
    
    
    #####	
    #calculate 2nd y-point for every line
    #	First line will be vertical, 
    #	each will have labels a certain distance
    #	from the previous label.
    #####
    label_spacing=label_spacing
    
    hpos_text<-xinit + label_spacing
    count=count+1
    
    #Coloring for y
    ycolor<-ifelse(obsy==0,yblue,yred)	
    
    #####
    #Determine whether you'll have a negatively
    #	sloped line pointing to the label,
    #	or a positively sloped line, depending
    #	on where the label must go (based on
    #	its positioning)
    #####
    
    if(pdata$forecastOrder1[i] > hpos_text){
      LineSlope<-c(1,0)
    } else {
      LineSlope<-c(0,1)
    }
    
    
    ###############################
    #Create the labels on plot
    ###############################
    labeltext<-pdata$label_best_m1[i]
    label_adjust_top=bottom_lab_adjust
    
    current<-
      z2+
      annotation_custom(
        grob=textGrob(
          label=labeltext,
          y=-0.1-label_adjust_top,
          rot=-90,
          gp=gpar(col=ycolor,fontsize=7)
        ),
        xmin=hpos_text,
        xmax=hpos_text,
      )+
      annotation_custom(
        grob=linesGrob(
          y=c(0,-.1),
          x=LineSlope,
          gp=gpar(col=ycolor),
        ),
        
        xmin=ifelse(
          pdata$forecastOrder1[i] > hpos_text,
          hpos_text,
          pdata$forecastOrder1[i]
        ),
        xmax=ifelse(
          pdata$forecastOrder1[i] > hpos_text,
          pdata$forecastOrder1[i],
          hpos_text
        ),
      )
    
    ########################
    #Decide whether to add vertical pointer lines
    ########################
    vcol<-ifelse(obsy==0,ybluelitest,yredlitest)
    if(vlines==TRUE){
      current_fin<-current+
        annotation_custom(
          grob=linesGrob(
            y=c(0,1),
            x=LineSlope,
            gp=gpar(col=ifelse(mart==F,vcol,ycolor)),
          ),
          xmin=pdata$forecastOrder1[i],
          xmax= pdata$forecastOrder1[i],
          ymax=ifelse(mart==F,pdata$forecastOrder2[i],N)
        )
    } else {
      current_fin<-current
    }
    z2<-current_fin
  }
  
  
  
  #Turn off clipping so we can render the plot
  gt <- ggplot_gtable(ggplot_build(z2))
  gt$layout$clip[gt$layout$name == "panel"] <- "off"
  o3<-arrangeGrob(gt)
  return(o3)
}