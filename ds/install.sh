#!/bin/bash

# This script installs all you need for dynasim
# It will
#   * Update conda
#   * Create a conda environment named dynasim
#   * Create a dynasim directory in your home directory for storage

echo "Updating conda"
conda update conda --yes

echo "Removing previous existing conda env named dynasim"
conda remove --name dynasim --all --yes

echo "Creating env from environment.yml"
conda env create -f dynasim.yml


echo "Install finished"
