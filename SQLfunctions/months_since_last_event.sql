--generalized version
CREATE OR REPLACE FUNCTION public.months_since_last_event(schema_name text, table_name text, column_name text, priogridgid_in bigint, month_id_in bigint) RETURNS int AS
  $$
  DECLARE query_text TEXT;
  DECLARE month_prev INT;
  BEGIN
  query_text := format('SELECT max(month_id) FROM %I.%I WHERE priogrid_gid=%s AND month_id<%s AND %I>0', schema_name, table_name, priogridgid_in, month_id_in, column_name);
  EXECUTE query_text INTO month_prev;
  RETURN month_id_in-month_prev::INT;
  END;
$$
LANGUAGE Plpgsql IMMUTABLE
RETURNS NULL ON NULL INPUT;

--non-generalized version
DROP FUNCTION public.months_since_last_event(text, bigint, bigint);
CREATE OR REPLACE FUNCTION public.months_since_last_event(column_name text, priogridgid_in bigint, month_id_in bigint) RETURNS int AS
  $$
  DECLARE query_text TEXT;
  DECLARE month_prev INT;
  BEGIN
  query_text := format('SELECT max(month_id) FROM staging.priogrid_month WHERE priogrid_gid=%s AND month_id<%s AND %I>0', priogridgid_in, month_id_in, column_name);
  EXECUTE query_text INTO month_prev;
  RETURN month_id_in-month_prev::INT;
  END;
$$
LANGUAGE Plpgsql IMMUTABLE
RETURNS NULL ON NULL INPUT;




CREATE OR REPLACE FUNCTION public.cm_months_since_last_event(column_name text, country_id_in bigint, month_id_in bigint) RETURNS int AS
  $$
  DECLARE query_text TEXT;
  DECLARE month_prev INT;
  BEGIN
  query_text := format('SELECT max(month_id) FROM staging.country_month WHERE country_id=%s AND month_id<%s AND %I>0', country_id_in, month_id_in, column_name);
  EXECUTE query_text INTO month_prev;
  RETURN month_id_in-month_prev::INT;
  END;
$$
LANGUAGE Plpgsql IMMUTABLE
RETURNS NULL ON NULL INPUT;

--TESTED ON 80318 135, 138, 178, 179, 195
