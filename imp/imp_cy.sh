#!/bin/bash -l
#SBATCH -A snic2017-1-306
#SBATCH -p core
#SBATCH -n 5

#SBATCH -t 98:00:00
#SBATCH -J imp_cy
#SBATCH -o /proj/snic2017-1-306/runs/current/imp/logs/imp_cy.log

module load PostgreSQL
cd ~/github/Views/imp
Rscript imp_cy.R

