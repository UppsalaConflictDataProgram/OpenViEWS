source config.sh

N_IMP=5

echo "clearing and setting up dirstructure in $DIR_THIS_RUN"
rm -rf $DIR_THIS_RUN
mkdir $DIR_THIS_RUN
mkdir -p $DIR_THIS_RUN/ds
mkdir -p $DIR_THIS_RUN/ds/input
mkdir -p $DIR_THIS_RUN/ds/input/pgm/spatial
mkdir -p $DIR_THIS_RUN/ds/input/cm/spatial
mkdir -p $DIR_THIS_RUN/ds/logs
mkdir -p $DIR_THIS_RUN/ds/results
mkdir -p $DIR_THIS_RUN/maps
mkdir -p $DIR_THIS_RUN/maps/logs
mkdir -p $DIR_THIS_RUN/video
mkdir -p $DIR_THIS_RUN/osa
mkdir -p $DIR_THIS_RUN/osa/logs
mkdir -p $DIR_THIS_RUN/osa/results
mkdir -p $DIR_THIS_RUN/imp
mkdir -p $DIR_THIS_RUN/agg/results
mkdir -p $DIR_THIS_RUN/imp/logs
mkdir -p $DIR_THIS_RUN/ensemble
mkdir -p $DIR_THIS_RUN/ensemble/logs
mkdir -p $DIR_THIS_RUN/ensemble/results
mkdir -p $DIR_THIS_RUN/calibrated/results
mkdir -p $DIR_THIS_RUN/cl/results
mkdir -p $DIR_INPUT_PGM_DATA
mkdir -p $DIR_INPUT_CM_DATA
mkdir -p $DIR_INPUT_PGM_SPATIAL
mkdir -p $DIR_LOGS_MAPS
mkdir -p $DIR_LOGS_DESCRIPTIVE

bash spatial/get_shapefiles_from_db.sh

echo "activating py3 environment"
source $ENV_PY3_JANUS

cd $DIR_GITHUB_OPS
echo "Fetching pgm_imp_ 1-$N_IMP"
for imp in `seq 1 $N_IMP`;
    do
        PATH_QUERY=$DIR_GITHUB/SQLSelects/pgm_imp_$imp.sql
        python fetch_data.py \
            --dir_data $DIR_INPUT_PGM_DATA \
            --path_query $PATH_QUERY
    done
#@TODO rename cm_imp to imp_cm
echo "Fetching cm_imp_"
for imp in `seq 1 $N_IMP`;
    do
        PATH_QUERY=$DIR_GITHUB/SQLSelects/cm_imp_$imp.sql
        python fetch_data.py \
            --dir_data $DIR_INPUT_CM_DATA \
            --path_query $PATH_QUERY
    done

python balance_panel_inputdata_cm.py

echo "Pushing run dir to $HOSTNAME_UPPMAX:$DIR_RUN_UPPMAX"
rsync -avz --delete $DIR_THIS_RUN/ $HOSTNAME_UPPMAX:$DIR_RUN_UPPMAX

