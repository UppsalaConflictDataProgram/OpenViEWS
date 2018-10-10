CREATE OR REPLACE FUNCTION public.aggregate_cm_acled (country_month_id BIGINT, count bool, lags int, type_of_violence integer)
  RETURNS INTEGER AS
  $$
  DECLARE query_bit text := 'SELECT ';
  DECLARE calculatedres integer;
  DECLARE country_id INTEGER;
  DECLARE month_id BIGINT;
  BEGIN
  IF count THEN query_bit := query_bit || 'count(*)::integer';
  ELSE query_bit := query_bit || 'sum(fatalities::integer)::integer';
  END IF;
  query_bit := query_bit || ' FROM preflight.acled_full WHERE type_of_violence='||type_of_violence;
  IF lags=0 THEN
    query_bit := query_bit || ' AND country_month_id = ' || country_month_id;
  END IF;
  IF lags=1 THEN
    EXECUTE 'SELECT country_id, month_id FROM staging.country_month WHERE id='||country_month_id INTO country_id, month_id;
    query_bit := query_bit || ' AND country_month_id IN (SELECT id FROM staging.country_month WHERE
  country_id IN (SELECT country_id_a FROM staging.country_spatial_lag WHERE country_id_b='||country_id||') AND
  month_id = '|| month_id ||')';
  --RAISE EXCEPTION 'QUERY is %', query_bit;
  END IF;
  EXECUTE query_bit INTO calculatedres;
  RETURN COALESCE(calculatedres,0)::integer;
  END;
  $$
  LANGUAGE 'plpgsql' IMMUTABLE;




CREATE OR REPLACE FUNCTION public.make_country_month_acled_temporal_lags(months int, make_columns bool, lower_month_bound int, higher_month_bound int)
RETURNS void AS
$$
DECLARE query text;
BEGIN

IF make_columns THEN
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_sb_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_ns_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_os_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_pr_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_sb_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_ns_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_os_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN acled_count_pr_lag1_tlag%s int;',months); EXECUTE(query);
END IF;

query:=format('UPDATE staging.country_month SET
acled_count_sb_tlag%1$s = a.acled_count_sb,
acled_count_ns_tlag%1$s = a.acled_count_ns,
acled_count_os_tlag%1$s = a.acled_count_os,
acled_count_pr_tlag%1$s = a.acled_count_pr,
acled_count_sb_lag1_tlag%1$s = a.acled_count_sb_lag1,
acled_count_ns_lag1_tlag%1$s = a.acled_count_ns_lag1,
acled_count_os_lag1_tlag%1$s = a.acled_count_os_lag1,
acled_count_pr_lag1_tlag%1$s = a.acled_count_pr_lag1
FROM staging.country_month a
WHERE
(
staging.country_month.month_id = a.month_id+%1$s
AND
staging.country_month.country_id = a.country_id
AND
staging.country_month.month_id BETWEEN  %2$s AND %3$s
AND
a.month_id BETWEEN %2$s AND %3$s);',months, lower_month_bound, higher_month_bound);
EXECUTE(query);
END;
$$
LANGUAGE 'plpgsql' VOLATILE;
