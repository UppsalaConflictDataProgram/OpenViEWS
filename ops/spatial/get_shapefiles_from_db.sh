source config.sh
PATH_INPUT_CM_SPATIAL=$DIR_THIS_RUN/ds/input/cm/spatial
PATH_INPUT_PGM_SPATIAL=$DIR_THIS_RUN/ds/input/pgm/spatial
PATH_C_SHAPE=$PATH_INPUT_CM_SPATIAL/country
PATH_PG_SHAPE=$PATH_INPUT_PGM_SPATIAL/priogrid

echo "Fetching shapefile to $PATH_C_SHAPE"
# The gweyear and gwemonth should give us only countries currently existing
pgsql2shp -h VIEWSHOST -u VIEWSADMIN -f $PATH_C_SHAPE -r views 'SELECT id, geom FROM staging.country WHERE gweyear=2016 AND gwemonth=6'
echo "Fetching shapefile to $PATH_PG_SHAPE"
pgsql2shp -h VIEWSHOST -u VIEWSADMIN -f $PATH_PG_SHAPE -r  views 'SELECT gid, geom FROM staging.priogrid WHERE in_africa=TRUE;'
echo "Finished getting shapefiles"
