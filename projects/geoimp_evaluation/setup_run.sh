source config.sh

N_IMP=5

echo "clearing and setting up dirstructure in $DIR_THIS_RUN"
rm -rf $DIR_THIS_RUN
mkdir -p $DIR_THIS_RUN

mkdir -p $DIR_INPUT_PGM_DATA_NOIMP
mkdir -p $DIR_INPUT_PGM_DATA_GEOIMP
mkdir -p $DIR_INPUT_PGM_DATA_NAIVE

mkdir -p $DIR_INPUT_PGM_SPATIAL_NOIMP
mkdir -p $DIR_INPUT_PGM_SPATIAL_GEOIMP
mkdir -p $DIR_INPUT_PGM_SPATIAL_NAIVE

mkdir -p $DIR_THIS_RUN/ds/logs
mkdir -p $DIR_THIS_RUN/ds/results

echo "Fetching shapefile to $DIR_INPUT_PGM_SPATIAL_NOIMP"
pgsql2shp -h VIEWSHOST -u VIEWSADMIN -f $DIR_INPUT_PGM_SPATIAL_NOIMP/priogrid -r  views 'SELECT gid, geom FROM staging.priogrid WHERE in_africa=TRUE;'
echo "Finished getting shapefiles"

echo "Fetching shapefile to $DIR_INPUT_PGM_SPATIAL_NAIVE"
pgsql2shp -h VIEWSHOST -u VIEWSADMIN -f $DIR_INPUT_PGM_SPATIAL_NAIVE/priogrid -r  views 'SELECT gid, geom FROM staging.priogrid WHERE in_africa=TRUE;'
echo "Finished getting shapefiles"

echo "Fetching shapefile to $DIR_INPUT_PGM_SPATIAL_GEOIMP"
pgsql2shp -h VIEWSHOST -u VIEWSADMIN -f $DIR_INPUT_PGM_SPATIAL_GEOIMP/priogrid -r  views 'SELECT gid, geom FROM staging.priogrid WHERE in_africa=TRUE;'
echo "Finished getting shapefiles"

echo "activating py3 environment"
source $ENV_PY3_JANUS

cd $DIR_GITHUB_OPS

python fetch_data.py \
    --dir_data $DIR_INPUT_PGM_DATA_NOIMP \
    --path_query $DIR_GITHUB_PROJECT/SQLSelects/noimp.sql

python fetch_data.py \
    --dir_data $DIR_INPUT_PGM_DATA_NAIVE \
    --path_query $DIR_GITHUB_PROJECT/SQLSelects/naive.sql

echo "Fetching pgm_imp_ 1-$N_IMP"
for imp in `seq 1 $N_IMP`;
    do
        PATH_QUERY=$DIR_GITHUB_PROJECT/SQLSelects/pgm_imp_$imp.sql
        python fetch_data.py \
            --dir_data $DIR_INPUT_PGM_DATA_GEOIMP \
            --path_query $PATH_QUERY 
    done

echo "Pushing run dir to $HOSTNAME_UPPMAX:$DIR_RUN_UPPMAX"
rsync -avz --delete $DIR_THIS_RUN $HOSTNAME_UPPMAX:$DIR_RUN_UPPMAX

