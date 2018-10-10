#!/bin/bash -l
#SBATCH -A snic2017-1-306
#SBATCH -p node
#SBATCH -C mem256GB
# One week to run...
#SBATCH -t 168:00:00
#SBATCH -J imp_pgm
#SBATCH -o /proj/snic2017-1-306/runs/current/imp/logs/imp_pgm.log

module load PostgreSQL
cd ~/github/Views/imp
Rscript imp_pgm.R

