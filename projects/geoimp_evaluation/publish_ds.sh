#!/bin/bash
source config.sh

echo "activating py3 environment"
source $ENV_PY3_JANUS

cd $DIR_GITHUB_DS
bash ../projects/geoimp_evaluation/ds/publishes/ds_pgm_eval_test.sh
