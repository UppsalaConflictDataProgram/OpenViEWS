#!/bin/bash
source config.sh

echo "activating py3 environment"
source $ENV_PY3_JANUS

cd $DIR_GITHUB_DS
for filename in ../models/output/ds/publishes/*; do
    bash "$filename"
done
