-- Dependencies: All functions from the functions directory MUST be installed.

-- STEP 1 : Attach staging month IDs to the data

CREATE TABLE preflight.ged_attached AS
  (
    WITH month_ged AS
    (
        SELECT
          *,
          EXTRACT(MONTH FROM date_start :: DATE) AS month_start,
          EXTRACT(MONTH FROM date_end :: DATE)   AS month_end
        FROM dataprep.ged
    ),
        month_ged_start AS
      (
          SELECT
            month_ged.*,
            staging.month.id AS month_id_start
          FROM month_ged, staging.month
          WHERE
            (month_ged.year :: INT = staging.month.year_id AND
             month_ged.month_start = staging.month.month)
      ),
        month_ged_full AS
      (
          SELECT
            month_ged_start.*,
            staging.month.id AS month_id_end
          FROM month_ged_start, staging.month
          WHERE
            (month_ged_start.year :: INT = staging.month.year_id AND
             month_ged_start.month_end = staging.month.month)
      )
    SELECT *
    FROM month_ged_full
  );

--SELECT public.aggregate_deaths_on_date_end(184046,144,False,False,0,1);
--SELECT * FROM preflight.ged_attached WHERE priogrid_gid=184046 and month_id_end=144;
--113 ms vs 4 ms

-- STEP 2 : Add ids and indexing

ALTER TABLE preflight.ged_attached ADD PRIMARY KEY (id);

ALTER TABLE preflight.ged_attached ADD COLUMN country_month_id_end bigint;
ALTER TABLE preflight.ged_attached ADD COLUMN country_month_id_start bigint;

-- SETP 2.1 : Geometrify

ALTER TABLE preflight.ged_attached DROP COLUMN geom;
ALTER TABLE preflight.ged_attached ADD COLUMN geom geometry (point,4326);
UPDATE preflight.ged_attached SET geom=st_setsrid(st_geometryfromtext(geom_wkt),4326);
CREATE INDEX ged_attached_gidx ON preflight.ged_attached USING GIST(geom);

-- STEP 3 : Add country-month ids from staging.country_month to the staging

with a as
(SELECT cm.*, c.gwcode FROM staging.country_month cm left join
      staging.country c on (cm.country_id=c.id))
UPDATE preflight.ged_attached SET country_month_id_end=a.id
FROM a
WHERE (a.gwcode = ged_attached.country_id AND a.month_id = ged_attached.month_id_end);

with a as
(SELECT cm.*, c.gwcode FROM staging.country_month cm left join
      staging.country c on (cm.country_id=c.id))
UPDATE preflight.ged_attached SET country_month_id_start=a.id
FROM a
WHERE (a.gwcode = ged_attached.country_id AND a.month_id = ged_attached.month_id_start);

-- Create a copy for PGM (only geoprec 1,2,3,5) and one for CM (all);

CREATE TABLE preflight.ged_attached_full AS SELECT * FROM preflight.ged_attached;
DELETE FROM preflight.ged_attached WHERE where_prec IN (4,6,7);
ALTER TABLE preflight.ged_attached_full ADD PRIMARY KEY (id);

-- Index tables for PGM

CREATE INDEX ged_attached_idx ON preflight.ged_attached(priogrid_gid, month_id_end, type_of_violence);
CREATE INDEX priogrid_month_idx ON staging.priogrid_month(priogrid_gid, month_id);

-- Compute variables for PGM

ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_sb;
ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_ns;
ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_best_os;
ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_sb;
ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_ns;
ALTER TABLE staging.priogrid_month DROP COLUMN IF EXISTS ged_count_os;

ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os INT;


VACUUM ANALYSE;


UPDATE staging.priogrid_month SET
  ged_best_sb = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 0, 1),
  ged_best_ns = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 0, 2),
  ged_best_os = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 0, 3),
  ged_count_sb = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 0, 1),
  ged_count_ns = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 0, 2),
  ged_count_os = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 0, 3)
WHERE
  month_id >= (SELECT min(month_id_end) FROM preflight.ged_attached) AND
  month_id <= (SELECT max(month_id_end) FROM preflight.ged_attached);
 
 -- this takes ~12 hours on linus

 
 
 VACUUM ANALYSE;
 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb_start INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns_start INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os_start INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb_start INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns_start INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os_start INT;  
 
 
 UPDATE staging.priogrid_month SET   
 ged_best_sb_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, FALSE, FALSE, 0, 1),   
 ged_best_ns_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, FALSE, FALSE, 0, 2),   
 ged_best_os_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, FALSE, FALSE, 0, 3),   
 ged_count_sb_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, TRUE, FALSE, 0, 1),   
 ged_count_ns_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, TRUE, FALSE, 0, 2),   
 ged_count_os_start = aggregate_deaths_on_date_start(priogrid_gid,month_id, TRUE, FALSE, 0, 3) WHERE   
 month_id >= (SELECT min(month_id_start) FROM preflight.ged_attached) AND   
 month_id <= (SELECT max(month_id_start) FROM preflight.ged_attached);
 
 -- this takes ~12 hours on linus

 VACUUM ANALYSE;
 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb_lag1 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns_lag1 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os_lag1 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb_lag1 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns_lag1 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os_lag1 INT;  
 
 
  
 UPDATE staging.priogrid_month SET   
 ged_best_sb_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 1, 1),   
 ged_best_ns_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 1, 2),   
 ged_best_os_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 1, 3),   
 ged_count_sb_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 1, 1),   
 ged_count_ns_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 1, 2),   
 ged_count_os_lag1 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 1, 3) 
 WHERE   
 month_id >= (SELECT min(month_id_end) FROM preflight.ged_attached) AND   
 month_id <= (SELECT max(month_id_end) FROM preflight.ged_attached);
 
 -- this takes ~12 hours on linus

VACUUM ANALYSE;
 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_sb_lag2 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_ns_lag2 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_best_os_lag2 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_sb_lag2 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_ns_lag2 INT; 
 ALTER TABLE staging.priogrid_month ADD COLUMN ged_count_os_lag2 INT;  
 
UPDATE staging.priogrid_month SET   
 ged_best_sb_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 2, 1),   
 ged_best_ns_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 2, 2),   
 ged_best_os_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, FALSE, FALSE, 2, 3),   
 ged_count_sb_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 2, 1),   
 ged_count_ns_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 2, 2),   
 ged_count_os_lag2 = aggregate_deaths_on_date_end(priogrid_gid,month_id, TRUE, FALSE, 2, 3) 
WHERE   
 month_id >= (SELECT min(month_id_end) FROM preflight.ged_attached) AND   
 month_id <= (SELECT max(month_id_end) FROM preflight.ged_attached);

 -- this takes ~20 hours on linus

VACUUM ANALYSE;

--COMPUTE temporal lags from 1..12. Each takes about 1 hour on linus, about 13 in total.
--While this is a SELECT, the function actually does add columns and populate them INSIDE the function
--Check the function file for how it works

SELECT public.make_priogrid_month_temporal_lags(1,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(2,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(3,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(4,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(5,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(6,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(7,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(8,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(9,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(10,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(11,TRUE,109,432);
SELECT public.make_priogrid_month_temporal_lags(12,TRUE,109,432);

VACUUM ANALYSE;

--add months since last event for each PGM entry.
--See the function file for how it works

ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_sb INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_ns INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_os INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_sb_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_ns_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_os_lag1 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_sb_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_ns_lag2 INT;
ALTER TABLE staging.priogrid_month ADD COLUMN ged_months_since_last_os_lag2 INT;

UPDATE staging.priogrid_month SET
ged_months_since_last_sb = public.months_since_last_event('ged_count_sb', priogrid_gid, month_id),
ged_months_since_last_ns = public.months_since_last_event('ged_count_ns', priogrid_gid, month_id),
ged_months_since_last_os = public.months_since_last_event('ged_count_os', priogrid_gid, month_id),
ged_months_since_last_sb_lag1 = public.months_since_last_event('ged_count_sb_lag1', priogrid_gid, month_id),
ged_months_since_last_ns_lag1 = public.months_since_last_event('ged_count_ns_lag1', priogrid_gid, month_id),
ged_months_since_last_os_lag1 = public.months_since_last_event('ged_count_os_lag1', priogrid_gid, month_id),
ged_months_since_last_sb_lag2 = public.months_since_last_event('ged_count_sb_lag2', priogrid_gid, month_id),
ged_months_since_last_ns_lag2 = public.months_since_last_event('ged_count_ns_lag2', priogrid_gid, month_id),
ged_months_since_last_os_lag2 = public.months_since_last_event('ged_count_os_lag2', priogrid_gid, month_id)
WHERE month_id BETWEEN 109 AND 432;
--The above took 21 hours on Linus.

VACUUM ANALYSE;

-- Compute variables for CM
-- index columns properly 
CREATE INDEX ged_attached_country_month_end_idx ON
  preflight.ged_attached_full(country_month_id_end, type_of_violence);

CREATE INDEX ged_attached_country_month_start_idx ON
  preflight.ged_attached_full(country_month_id_start, type_of_violence);
  
  
CREATE INDEX country_spatial_lag_idx ON staging.country_spatial_lag(country_id_b);
CREATE INDEX country_month_cid_mid_idx ON staging.country_month(country_id,month_id);

-- COMPUTE CM variables 
ALTER TABLE staging.country_month ADD COLUMN ged_best_sb INT;
ALTER TABLE staging.country_month ADD COLUMN ged_best_ns INT;
ALTER TABLE staging.country_month ADD COLUMN ged_best_os INT;
ALTER TABLE staging.country_month ADD COLUMN ged_count_sb INT;
ALTER TABLE staging.country_month ADD COLUMN ged_count_ns INT;
ALTER TABLE staging.country_month ADD COLUMN ged_count_os INT;
ALTER TABLE staging.country_month ADD COLUMN ged_best_sb_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_best_ns_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_best_os_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_count_sb_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_count_ns_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_count_os_lag1 INT;

UPDATE staging.country_month SET
  ged_best_sb = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,0,1),
  ged_best_ns = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,0,2),
  ged_best_os = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,0,3),
  ged_count_sb = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,0,1),
  ged_count_ns = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,0,2),
  ged_count_os = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,0,3),
  ged_best_sb_lag1 = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,1,1),
  ged_best_ns_lag1 = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,1,2),
  ged_best_os_lag1 = public.aggregate_cm_deaths_on_date_end(id,FALSE,FALSE,1,3),
  ged_count_sb_lag1 = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,1,1),
  ged_count_ns_lag1 = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,1,2),
  ged_count_os_lag1 = public.aggregate_cm_deaths_on_date_end(id,TRUE,FALSE,1,3)
WHERE month_id BETWEEN 108 AND 433;
-- this takes 2 minutes on linus.

-- Create temporal lags

SELECT public.make_country_month_temporal_lags(1,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(2,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(3,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(4,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(5,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(6,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(7,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(8,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(9,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(10,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(11,TRUE,109,432);
SELECT public.make_country_month_temporal_lags(12,TRUE,109,432);

-- this takes under 2 seconds

ALTER TABLE staging.country_month ADD COLUMN ged_months_since_last_sb INT;
ALTER TABLE staging.country_month ADD COLUMN ged_months_since_last_ns INT;
ALTER TABLE staging.country_month ADD COLUMN ged_months_since_last_os INT;
ALTER TABLE staging.country_month ADD COLUMN ged_months_since_last_sb_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_months_since_last_ns_lag1 INT;
ALTER TABLE staging.country_month ADD COLUMN ged_months_since_last_os_lag1 INT;


UPDATE staging.country_month SET
ged_months_since_last_sb = public.cm_months_since_last_event('ged_count_sb', country_id, month_id),
ged_months_since_last_ns = public.cm_months_since_last_event('ged_count_ns', country_id, month_id),
ged_months_since_last_os = public.cm_months_since_last_event('ged_count_os', country_id, month_id),
ged_months_since_last_sb_lag1 = public.cm_months_since_last_event('ged_count_sb_lag1', country_id, month_id),
ged_months_since_last_ns_lag1 = public.cm_months_since_last_event('ged_count_ns_lag1', country_id, month_id),
ged_months_since_last_os_lag1 = public.cm_months_since_last_event('ged_count_os_lag1', country_id, month_id)
WHERE month_id BETWEEN 109 AND 432;

