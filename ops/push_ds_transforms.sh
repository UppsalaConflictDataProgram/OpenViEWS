source config.sh
echo "activating py3 environment"
source $ENV_PY3_JANUS

python push_data_from_dir.py --dir_data /storage/runs/current/ds/transforms/cm_transforms/data --table_prefix transforms
python push_data_from_dir.py --dir_data /storage/runs/current/ds/transforms/pgm_transforms/data --table_prefix transforms