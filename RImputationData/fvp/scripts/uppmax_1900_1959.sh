#!/bin/bash -l
#SBATCH -A snic2017-7-47
#SBATCH -p core

#SBATCH -n 10
#SBATCH -t 48:00:00
#SBATCH -J imp_00_59
#SBATCH -o /home/VIEWSADMIN/gulla/imp/log1900_1959.txt


cd /home/VIEWSADMIN/gulla/imp
Rscript imp_fvp_1900_1959.R

