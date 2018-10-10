#!/bin/bash
source config.sh

echo "Fetching ds results from uppmax"
rsync -avz $HOSTNAME_UPPMAX:$DIR_RUN_UPPMAX $DIR_THIS_RUN/

