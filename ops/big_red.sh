#!/bin/bash

if [ "$HOSTNAME" != "VIEWSHOST" ]
then
echo "big_red.sh is meant to run on Janus, this doesn't appear to be him"
exit 1
fi

if [ "$HOSTNAME" == "VIEWSHOST" ]
then
echo "We are on VIEWSHOST"
fi

git pull

bash git_pull_rackham.sh
bash setup_run.sh

