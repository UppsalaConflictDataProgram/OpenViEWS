-- The following looks weird, as there are two functions with an identical name : onset_months_table.
-- This is on purpose, the second is an overloading of the first for generalization. Defaulting works much worse in this application,
-- as query plans.
-- You need to load BOTH functions for the system to work; there won't be a problem loading them in whatever order you want.

CREATE OR REPLACE FUNCTION onset_months_table (schema_name varchar, table_name varchar, column_name varchar)
RETURNS TABLE (
id int8,
onset_distance int8
) AS
$$
BEGIN
RETURN QUERY EXECUTE format('with a as (
    SELECT
      id,
      priogrid_gid,
      month_id
    FROM %s.%s
    WHERE %s > 0
),
  b as
  (
      SELECT
        id,
        priogrid_gid,
        month_id,
        lag(month_id)
        OVER (
          PARTITION BY priogrid_gid
          ORDER BY month_id ASC ) as onset_month
      FROM a
  )
SELECT id, coalesce(month_id-onset_month-1,9999) as onset_months FROM b
WHERE month_id-coalesce(onset_month,0)-1>0',schema_name,table_name,column_name);
END;
$$
LANGUAGE plpgsql;

-- Second function

CREATE OR REPLACE FUNCTION onset_months_table (schema_name varchar, table_name varchar, column_name varchar, grouping_name text)
RETURNS TABLE (
id int8,
onset_distance int8
) AS
$$
BEGIN
RETURN QUERY EXECUTE format('with a as (
    SELECT
      id,
      %s as priogrid_gid,
      month_id
    FROM %s.%s
    WHERE %s > 0
),
  b as
  (
      SELECT
        id,
        priogrid_gid,
        month_id,
        lag(month_id)
        OVER (
          PARTITION BY priogrid_gid
          ORDER BY month_id ASC ) as onset_month
      FROM a
  )
SELECT id, coalesce(month_id-onset_month-1,9999) as onset_months FROM b
WHERE month_id-coalesce(onset_month,0)-1>0',grouping_name, schema_name,table_name,column_name);
END;
$$
LANGUAGE plpgsql;


-- Usage example
-- ALTER TABLE staging.priogrid_month ADD COLUMN onset_months_sb int8;
-- with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_sb'))
--  UPDATE staging.priogrid_month SET onset_months_sb = a.onset_distance--
-- FROM a
-- WHERE a.id=staging.priogrid_month.id;
-- Estimated runtime 48 seconds on linus, 19 seconds on Janus


CREATE OR REPLACE FUNCTION public.onset_lags (
  priogrid bigint,
  month_id bigint,
  lags int default 1,
  schema_name text default 'staging',
  table_name text default 'priogrid_month',
  column_name text default 'ged_best_sb')
  -- Do not call this on the whole table. It will finish in months!
  RETURNS INTEGER AS
$$
  DECLARE query_bit text := 'SELECT max(month_id) FROM ' || schema_name || '.' || table_name ||' WHERE month_id<'||month_id||' AND ';
  DECLARE calculatedres integer;
  BEGIN
  query_bit := query_bit || column_name || '> 0 AND priogrid_gid IN (' || priogrid;
  IF lags<=2 THEN
  END IF;
  IF lags>=1 THEN
    query_bit := query_bit || ',' || priogrid-1 ||','|| priogrid+1 ||','|| priogrid+720 ||','|| priogrid+721 ||','|| priogrid+719 ||','|| priogrid-721 ||','|| priogrid-720 ||','|| priogrid-719;
  END IF;
  IF lags>=2 THEN
    query_bit := query_bit || ',' || priogrid-2 ||','|| priogrid+2 ||','|| priogrid+722 ||','|| priogrid+718 ||','|| priogrid-722 ||','|| priogrid-718 ||','|| priogrid-1442 ||','|| priogrid+1442 ||','|| priogrid-1441 ||','|| priogrid+1441 ||','|| priogrid-1440 ||','|| priogrid+1440 ||','|| priogrid-1439 ||','|| priogrid+1439 ||','|| priogrid-1438 ||','|| priogrid+1438;
  END IF;
  query_bit := query_bit || ')';
  IF lags>=3 THEN
    RETURN NULL;
  END IF;
  EXECUTE query_bit INTO calculatedres;

  calculatedres = month_id-calculatedres-1;

  IF calculatedres IS NULL THEN RETURN 9999;
  END IF ;

  IF calculatedres = 0 THEN RETURN NULL;
  ELSE
    RETURN calculatedres;
  END IF;
  END;
$$
RETURNS NULL ON NULL INPUT
LANGUAGE 'plpgsql' IMMUTABLE;
