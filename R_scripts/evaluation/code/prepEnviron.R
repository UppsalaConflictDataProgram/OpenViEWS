#install libraries necessary for ModelCriticism
#MPC 9/10/18

necLibs = c("gridExtra","dplyr","ggplot2","devtools","readr","itertools")
for (i in necLibs) {
  if (require(i, character.only=TRUE)) {
    txt=paste(i," attached just fine")
    message(txt)
  } else {
    install.packages(i)
    library(i)
    txt=paste(i, " had to be installed, before being attached")
  }
}

install_github("zsmahmood89/ModelCriticism/packages/ModelCriticism")
library(ModelCriticism)
