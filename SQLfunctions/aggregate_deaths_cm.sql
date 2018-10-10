  CREATE OR REPLACE FUNCTION public.aggregate_cm_deaths_on_date_end (country_month_id BIGINT, count bool, high bool, lags int, type_of_violence integer)
  RETURNS INTEGER AS
  $$
  DECLARE query_bit text := 'SELECT ';
  DECLARE calculatedres integer;
  DECLARE country_id INTEGER;
  DECLARE month_id BIGINT;
  BEGIN
  IF count THEN query_bit := query_bit || 'count(*)::integer';
  ELSEIF high THEN query_bit := query_bit || 'sum(high)::integer';
  ELSE query_bit := query_bit || 'sum(best)::integer';
  END IF;
  query_bit := query_bit || ' FROM preflight.ged_attached_full WHERE type_of_violence='||type_of_violence;
  IF lags=0 THEN
    query_bit := query_bit || ' AND country_month_id_end = ' || country_month_id;
  END IF;
  IF lags=1 THEN
    EXECUTE 'SELECT country_id, month_id FROM staging.country_month WHERE id='||country_month_id INTO country_id, month_id;
    query_bit := query_bit || ' AND country_month_id_end IN (SELECT id FROM staging.country_month WHERE
  country_id IN (SELECT country_id_a FROM staging.country_spatial_lag WHERE country_id_b='||country_id||') AND
  month_id = '|| month_id ||')';
  --RAISE EXCEPTION 'QUERY is %', query_bit;
  END IF;
  EXECUTE query_bit INTO calculatedres;
  RETURN COALESCE(calculatedres,0)::integer;
  END;
  $$
  LANGUAGE 'plpgsql' IMMUTABLE;


CREATE OR REPLACE FUNCTION public.aggregate_cm_deaths_on_date_start (country_month_id BIGINT, count bool, high bool, lags int, type_of_violence integer)
  RETURNS INTEGER AS
  $$
  DECLARE query_bit text := 'SELECT ';
  DECLARE calculatedres integer;
  DECLARE country_id INTEGER;
  DECLARE month_id BIGINT;
  BEGIN
  IF count THEN query_bit := query_bit || 'count(*)::integer';
  ELSEIF high THEN query_bit := query_bit || 'sum(high)::integer';
  ELSE query_bit := query_bit || 'sum(best)::integer';
  END IF;
  query_bit := query_bit || ' FROM preflight.ged_attached_full WHERE type_of_violence='||type_of_violence;
  IF lags=0 THEN
    query_bit := query_bit || ' AND country_month_id_start = ' || country_month_id;
  END IF;
  IF lags=1 THEN
    EXECUTE 'SELECT country_id, month_id FROM staging.country_month WHERE id='||country_month_id INTO country_id, month_id;
    query_bit := query_bit || ' AND country_month_id_start IN (SELECT id FROM staging.country_month WHERE
  country_id IN (SELECT country_id_a FROM staging.country_spatial_lag WHERE country_id_b='||country_id||') AND
  month_id = '|| month_id ||')';
  --RAISE EXCEPTION 'QUERY is %', query_bit;
  END IF;
  EXECUTE query_bit INTO calculatedres;
  RETURN COALESCE(calculatedres,0)::integer;
  END;
  $$
  LANGUAGE 'plpgsql' IMMUTABLE;
