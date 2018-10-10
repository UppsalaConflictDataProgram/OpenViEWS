CREATE OR REPLACE FUNCTION public.distance_to_nearest_ged
  ( schema_name varchar,
    table_name varchar,
    priogrid bigint,
    month_id BIGINT,
    type_of_violence integer
  )
  RETURNS FLOAT4 AS
  $$
  DECLARE query_bit text;
  DECLARE calculatedres float4;
  DECLARE pgm_geom text;
  BEGIN

  query_bit:='SELECT ST_AsEWKT(geom) FROM staging.priogrid WHERE gid='||priogrid;

  EXECUTE query_bit INTO pgm_geom;

  query_bit:='SELECT min(ST_Distance(
ST_GeomFromEWKT('''|| pgm_geom ||''')::geography
,geom::geography)/1000)::float  FROM '
  || schema_name || '.' || table_name ||
  ' WHERE month_id_end='||month_id||' AND type_of_violence='||type_of_violence;

  EXECUTE query_bit INTO calculatedres;
  RETURN calculatedres;

  END;
  $$
  LANGUAGE 'plpgsql' IMMUTABLE;
