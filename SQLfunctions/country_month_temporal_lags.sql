CREATE OR REPLACE FUNCTION public.make_country_month_temporal_lags(months int, make_columns bool, lower_month_bound int, higher_month_bound int)
RETURNS void AS
$$
DECLARE query text;
BEGIN

IF make_columns THEN
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_best_sb_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_best_ns_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_best_os_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_count_sb_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_count_ns_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_count_os_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_best_sb_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_best_ns_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_best_os_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_count_sb_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_count_ns_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.country_month ADD COLUMN ged_count_os_lag1_tlag%s int;',months); EXECUTE(query);
END IF;

query:=format('UPDATE staging.country_month SET
ged_best_sb_tlag%1$s = a.ged_best_sb,
ged_best_ns_tlag%1$s = a.ged_best_ns,
ged_best_os_tlag%1$s = a.ged_best_os,
ged_count_sb_tlag%1$s = a.ged_count_sb,
ged_count_ns_tlag%1$s = a.ged_count_ns,
ged_count_os_tlag%1$s = a.ged_count_os,
ged_best_sb_lag1_tlag%1$s = a.ged_best_sb_lag1,
ged_best_ns_lag1_tlag%1$s = a.ged_best_ns_lag1,
ged_best_os_lag1_tlag%1$s = a.ged_best_os_lag1,
ged_count_sb_lag1_tlag%1$s = a.ged_count_sb_lag1,
ged_count_ns_lag1_tlag%1$s  = a.ged_count_ns_lag1,
ged_count_os_lag1_tlag%1$s = a.ged_count_os_lag1
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

--usage: SELECT make_country_month_temporal_lags(number_of_months int, make_new_columns bool, first month to compute lags, last month to compute bounds);
--e.g. SELECT make_country_month_temporal_lags(12,TRUE,108,433); --one year lags, make new columns (1989-2015)
--e.g. SELECT make_country_month_temporal_lags(1,FALSE,108,433); --one month lags, update into existing columns.
