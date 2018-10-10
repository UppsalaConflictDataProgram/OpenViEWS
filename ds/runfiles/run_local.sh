#!/bin/bash

export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

cd ..
source activate dynasim



declare -a run_ids=("cm_canon_mean_eval_test"
                    "cm_canon_demog_eval_test"
                    "cm_canon_eco_eval_test"
                    "cm_canon_hist_eval_test"
                    "cm_canon_inst_eval_test"
                    "cm_canon_meandemog_eval_test"
                    "cm_canon_meaneco_eval_test"
                    "cm_canon_meanhist_eval_test"
                    "cm_canon_meaninst_eval_test"
                    "cm_canon_meandemoghist_eval_test"
                    "cm_canon_meanecohist_eval_test"
                    "cm_canon_meaninsthist_eval_test"
                    "cm_canon_meandemogeco_eval_test"
                    "cm_canon_meandemogecoinst_eval_test"
                    "cm_canon_meandemogecoinsthist_eval_test")

for run_id in "${run_ids[@]}"
do
   python main.py  --dir_scratch /storage/temp/scratch \
                    --run_id $run_id \
                    --dir_input /storage/temp/runs/current/ds/input \
                    --ncores 4 \
                    --dir_paramfiles ~/github/Views/models/output/ds/paramfiles \

done
