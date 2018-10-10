ALTER TABLE staging.priogrid_month ADD COLUMN onset_months_sb int8;
ALTER TABLE staging.priogrid_month ADD COLUMN onset_months_os int8;
ALTER TABLE staging.priogrid_month ADD COLUMN onset_months_ns int8;

with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_sb'))
  UPDATE staging.priogrid_month SET onset_months_sb = a.onset_distance
  FROM a
  WHERE a.id=staging.priogrid_month.id;


with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_ns'))
  UPDATE staging.priogrid_month SET onset_months_ns = a.onset_distance
  FROM a
  WHERE a.id=staging.priogrid_month.id;


with a as (SELECT * FROM onset_months_table('staging','priogrid_month','ged_best_os'))
  UPDATE staging.priogrid_month SET onset_months_os = a.onset_distance
  FROM a
  WHERE a.id=staging.priogrid_month.id;

                                            
-- Added onset spatial lags (onset for PGM A is an onset no onset occured in PGM A or in any spatial lags order 1 and order 2
-- in n months.
                                            
ALTER TABLE staging.priogrid_month ADD COLUMN onset_month_sb_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN onset_month_sb_lag2 INT;

UPDATE staging.priogrid_month SET
  onset_month_sb_lag1 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 1,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_sb'::varchar),

  onset_month_sb_lag2 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 2,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_sb'::varchar)
WHERE onset_months_sb > 0;


ALTER TABLE staging.priogrid_month ADD COLUMN onset_month_ns_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN onset_month_ns_lag2 INT;

UPDATE staging.priogrid_month SET
  onset_month_ns_lag1 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 1,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_ns'::varchar),

  onset_month_ns_lag2 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 2,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_ns'::varchar)
WHERE onset_months_ns > 0;

                                            --
ALTER TABLE staging.priogrid_month ADD COLUMN onset_month_os_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN onset_month_os_lag2 INT;

UPDATE staging.priogrid_month SET
  onset_month_os_lag1 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 1,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_os'::varchar),

  onset_month_os_lag2 =
  onset_lags(
  priogrid := priogrid_gid,
  month_id := month_id,
  lags := 2,
  schema_name := 'staging'::varchar,
  table_name := 'priogrid_month'::varchar,
  column_name := 'ged_best_os'::varchar)
WHERE onset_months_os > 0;

                                            
                                            
ALTER TABLE staging.country_month ADD COLUMN onset_months_sb int8;
ALTER TABLE staging.country_month ADD COLUMN onset_months_os int8;
ALTER TABLE staging.country_month ADD COLUMN onset_months_ns int8;

with a as (SELECT * FROM onset_months_table('staging','country_month','ged_best_sb','country_id'))
  UPDATE staging.country_month SET onset_months_sb = a.onset_distance
  FROM a
  WHERE a.id=staging.country_month.id;

with a as (SELECT * FROM onset_months_table('staging','country_month','ged_best_ns','country_id'))
  UPDATE staging.country_month SET onset_months_ns = a.onset_distance
  FROM a
  WHERE a.id=staging.country_month.id;

with a as (SELECT * FROM onset_months_table('staging','country_month','ged_best_os','country_id'))
  UPDATE staging.country_month SET onset_months_os = a.onset_distance
  FROM a
  WHERE a.id=staging.country_month.id;
