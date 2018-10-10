#!/bin/bash -l
#SBATCH -A snic2017-7-47
#SBATCH -p core

#SBATCH -n 10
#SBATCH -t 72:00:00
#SBATCH -J imp_60_16
#SBATCH -o /home/VIEWSADMIN/gulla/imp/log1960_2016.txt


cd /home/VIEWSADMIN/gulla/imp
Rscript imp_fvp_1960_2016.R

