-- This is all that is needed to stage ACLED
-- Run ./updateACLED.py --start 1997-01-01 --e 2016-05-01 to stage it completely if you need to redo the staging.

ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_sb INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_ns INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_os INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pr INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_sb INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_ns INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_os INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pr INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_sb_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_ns_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_os_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pr_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_sb_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_ns_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_os_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pr_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_sb_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_ns_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_os_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_count_pr_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_sb_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_ns_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_os_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN acled_fat_pr_lag2 INT;


ALTER TABLE preflight.acled_full ADD COLUMN country_month_id INT;

with a as
(SELECT cm.*, c.gwcode FROM staging.country_month cm left join
      staging.country c on (cm.country_id=c.id))
UPDATE preflight.acled_full SET country_month_id=a.id
FROM a
WHERE (a.gwcode::int = acled_full.gwno::int AND a.month_id = acled_full.month_id);

CREATE INDEX acled_full_cm_idx ON preflight.acled_full(country_month_id, type_of_violence);

ALTER TABLE staging.country_month ADD COLUMN acled_count_sb INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_ns INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_os INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_pr INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_sb_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_ns_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_os_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN acled_count_pr_lag1 INT;

UPDATE staging.country_month SET
  acled_count_sb = public.aggregate_cm_acled(id,TRUE,0,1),
  acled_count_ns = public.aggregate_cm_acled(id,TRUE,0,2),
  acled_count_os = public.aggregate_cm_acled(id,TRUE,0,3),
  acled_count_pr = public.aggregate_cm_acled(id,TRUE,0,4),
  acled_count_sb_lag1 = public.aggregate_cm_acled(id,TRUE,1,1),
  acled_count_ns_lag1 = public.aggregate_cm_acled(id,TRUE,1,2),
  acled_count_os_lag1 = public.aggregate_cm_acled(id,TRUE,1,3),
  acled_count_pr_lag1 = public.aggregate_cm_acled(id,TRUE,1,4)
WHERE month_id BETWEEN 205 AND 448;

ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_sb INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_ns INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_os INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_pr INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_sb_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_ns_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_os_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN acled_months_since_last_pr_lag1 INT;


UPDATE staging.country_month SET
acled_months_since_last_sb = public.cm_months_since_last_event('acled_count_sb', country_id, month_id),
acled_months_since_last_ns = public.cm_months_since_last_event('acled_count_ns', country_id, month_id),
acled_months_since_last_os = public.cm_months_since_last_event('acled_count_os', country_id, month_id),
acled_months_since_last_pr = public.cm_months_since_last_event('acled_count_pr', country_id, month_id),
acled_months_since_last_sb_lag1 = public.cm_months_since_last_event('acled_count_sb_lag1', country_id, month_id),
acled_months_since_last_ns_lag1 = public.cm_months_since_last_event('acled_count_ns_lag1', country_id, month_id),
acled_months_since_last_os_lag1 = public.cm_months_since_last_event('acled_count_os_lag1', country_id, month_id),
acled_months_since_last_pr_lag1 = public.cm_months_since_last_event('acled_count_pr_lag1', country_id, month_id)
WHERE month_id BETWEEN 205 AND 448;


SELECT make_country_month_acled_temporal_lags(1, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(2, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(3, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(4, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(5, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(6, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(7, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(8, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(9, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(10, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(11, TRUE, 205, 448);
SELECT make_country_month_acled_temporal_lags(12, TRUE, 205, 448);
