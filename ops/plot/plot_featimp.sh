source ../config.sh

cd $DIR_GITHUB/plot/

python -u feature_importance.py\
    --run_id $RUN_ID
