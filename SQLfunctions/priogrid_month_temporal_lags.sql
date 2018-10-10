CREATE OR REPLACE FUNCTION public.make_priogrid_month_temporal_lags(months int, make_columns bool, lower_month_bound int, higher_month_bound int)
RETURNS void AS
$$
DECLARE query text;
BEGIN

IF make_columns THEN

query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_sb_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_ns_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_os_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_sb_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_ns_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_os_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_sb_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_ns_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_os_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_sb_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_ns_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_os_lag1_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_sb_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_ns_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_os_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_sb_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_ns_lag2_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_os_lag2_tlag%s ;',months); EXECUTE(query);


query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os_lag1_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb_lag2_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns_lag2_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os_lag2_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb_lag2_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns_lag2_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os_lag2_tlag%s int;',months); EXECUTE(query);
END IF;

query:=format('UPDATE staging.priogrid_month SET
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
ged_count_os_lag1_tlag%1$s = a.ged_count_os_lag1,
ged_best_sb_lag2_tlag%1$s = a.ged_best_sb_lag2,
ged_best_ns_lag2_tlag%1$s = a.ged_best_ns_lag2,
ged_best_os_lag2_tlag%1$s = a.ged_best_os_lag2,
ged_count_sb_lag2_tlag%1$s = a.ged_count_sb_lag2,
ged_count_ns_lag2_tlag%1$s  = a.ged_count_ns_lag2,
ged_count_os_lag2_tlag%1$s = a.ged_count_os_lag2
FROM staging.priogrid_month a
WHERE
(
staging.priogrid_month.month_id = a.month_id+%1$s
AND
staging.priogrid_month.priogrid_gid = a.priogrid_gid
AND
staging.priogrid_month.month_id BETWEEN  %2$s AND %3$s
AND
a.month_id BETWEEN %2$s-12 AND %3$s);',months, lower_month_bound, higher_month_bound);
EXECUTE(query);
END;
$$
LANGUAGE 'plpgsql' VOLATILE;

              
CREATE function make_distance_temporal_lags(months integer, make_columns boolean, lower_month_bound integer, higher_month_bound integer) returns void
LANGUAGE plpgsql
AS $$
DECLARE query text;
BEGIN

IF make_columns THEN

query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS dist_ged_sb_event_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS dist_ged_ns_event_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS dist_ged_os_event_tlag%s ;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN dist_ged_sb_event_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN dist_ged_ns_event_tlag%s int;',months); EXECUTE(query);
query:=format('ALTER TABLE staging.priogrid_month ADD COLUMN dist_ged_os_event_tlag%s int;',months); EXECUTE(query);
END IF;

query:=format('UPDATE staging.priogrid_month SET
dist_ged_sb_event_tlag%1$s = a.dist_ged_sb_event,
dist_ged_ns_event_tlag%1$s = a.dist_ged_ns_event,
dist_ged_os_event_tlag%1$s = a.dist_ged_os_event
FROM staging.priogrid_month a
WHERE
(
staging.priogrid_month.month_id = a.month_id+%1$s
AND
staging.priogrid_month.priogrid_gid = a.priogrid_gid
AND
staging.priogrid_month.month_id BETWEEN  %2$s AND %3$s
AND
a.month_id BETWEEN %2$s-12 AND %3$s);',months, lower_month_bound, higher_month_bound);
EXECUTE(query);
END;
$$;
