-- interpolate cy variables
-- use a special table so we can index (for speed) AND use interpolate_priogrid_year (and not need another function).
-- Author: Mihai Croicu
-- Date 2017-09-07

DROP TABLE IF EXISTS dataprep.cy_interp;

CREATE TABLE dataprep.cy_interp AS
SELECT
   country_id as gid,
   year_id as year,
   fvp_ltsc0,
   fvp_population200,
   v2x_polyarchy,
   fvp_lngdp200,
   v2x_libdem
FROM staging.country_year;

CREATE INDEX cy_interp_idx ON dataprep.cy_interp(gid,year);

ALTER TABLE dataprep.cy_interp ADD COLUMN v2x_polyarchy_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN fvp_lngdp200_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN fvp_lngdppercapita200_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN fvp_ltsc0_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN fvp_population200_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN v2x_libdem_li DOUBLE PRECISION;

UPDATE dataprep.cy_interp SET
v2x_polyarchy_li        = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'v2x_polyarchy', gid, year),
fvp_lngdp200_li         = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'fvp_lngdp200', gid, year),
fvp_lngdppercapita200_li= public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'fvp_lngdppercapita200', gid, year),
fvp_population200_li    = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'fvp_population200', gid, year),
fvp_ltsc0_li            = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'fvp_ltsc0', gid, year),
v2x_libdem_li           = public.interpolate_priogrid_year('dataprep', 'cy_interp', 'v2x_libdem', gid, year)
WHERE year between 1980 and 2030;

ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_polyarchy_li;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_lngdp200_li;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_lngdppercapita200_li;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_ltsc0_li;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_population200_li;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_libdem_li;


ALTER TABLE staging.country_year ADD COLUMN v2x_polyarchy_li DOUBLE PRECISION;
ALTER TABLE staging.country_year ADD COLUMN fvp_lngdp200_li DOUBLE PRECISION;
ALTER TABLE staging.country_year ADD COLUMN fvp_lngdppercapita200_li DOUBLE PRECISION;
ALTER TABLE staging.country_year ADD COLUMN fvp_ltsc0_li DOUBLE PRECISION;
ALTER TABLE staging.country_year ADD COLUMN fvp_population200_li DOUBLE PRECISION;
ALTER TABLE staging.country_year ADD COLUMN v2x_libdem_li DOUBLE PRECISION;


UPDATE staging.country_year SET
 v2x_polyarchy_li = c.v2x_polyarchy_li,
 fvp_lngdp200_li = c.fvp_lngdp200_li,
 fvp_lngdppercapita200_li = c.fvp_lngdppercapita200_li,
 fvp_ltsc0_li = c.fvp_ltsc0_li,
 fvp_population200_li = c.fvp_population200_li,
 v2x_libdem_li = c.v2x_libdem_li
FROM dataprep.cy_interp as c
WHERE c.gid = country_id AND c.year=year_id;


SELECT DISTINCT year_id, country_id,
  v2x_polyarchy, v2x_polyarchy_li,
  fvp_population200, fvp_population200_li, v2x_libdem_li
FROM staging.country_year
order by country_id, year_id;

DROP TABLE IF EXISTS dataprep.cy_interp;


-- pgy variables

DROP TABLE IF EXISTS dataprep.pgy_interp;

--grid-level lnpop
--grid-level gcp_li_mer
--grid-level imr
--grid-level lnttime
--grid-level mountains_mean
--grid-level urban_ih
--grid-level lnbdist1
--grid-level lncapdist
--grid-level excluded

DROP TABLE IF EXISTS dataprep.cy_interp;

-- interpolate pgy's. Use the same structure as above for speed.

CREATE TABLE dataprep.cy_interp AS
SELECT
   priogrid_gid as gid,
   year_id as year,
   urban_ih,savanna_ih,agri_ih,barren_ih,forest_ih,grass_ih,pasture_ih,shrub_ih,water_ih,
   bdist1,
   capdist,
   excluded
FROM staging.priogrid_year;

CREATE INDEX pgy_interp_idx ON dataprep.cy_interp(gid,year);

ALTER TABLE dataprep.cy_interp ADD COLUMN savanna_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN agri_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN barren_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN forest_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN grass_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN pasture_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN shrub_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN water_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN bdist1_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN capdist_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN excluded_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN urban_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN savanna_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN agri_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN barren_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN forest_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN grass_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN pasture_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN shrub_ih_li DOUBLE PRECISION;
ALTER TABLE dataprep.cy_interp ADD COLUMN water_ih_li DOUBLE PRECISION;

UPDATE dataprep.cy_interp SET
savanna_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'savanna_ih', gid, year),
agri_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'agri_ih', gid, year),
barren_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'barren_ih', gid, year),
forest_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'forest_ih', gid, year),
grass_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'grass_ih', gid, year),
pasture_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'pasture_ih', gid, year),
shrub_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'shrub_ih', gid, year),
water_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'water_ih', gid, year)
urban_ih_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'urban_ih', gid, year),
bdist1_li   = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'bdist1', gid, year),
capdist_li  = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'capdist', gid, year),
excluded_li = public.interpolate_priogrid_year('dataprep', 'cy_interp' , 'excluded', gid, year)
WHERE year between 1980 and 2030;

ALTER TABLE staging.priogrid_year ADD COLUMN savanna_ih_li DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN agri_ih_li DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN barren_ih_li DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN forest_ih_li DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN pasture_ih_li DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN shrub_ih_li DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN water_ih_li DOUBLE PRECISION;

UPDATE staging.priogrid_year SET
 savanna_ih_li = c.savanna_ih_li,
 agri_ih_li = c.agri_ih_li,
 grass_ih_li = c.grass_ih_li
 barren_ih_li = c.barren_ih_li,
 forest_ih_li = c.forest_ih_li,
 pasture_ih_li = c.pasture_ih_li,
 shrub_ih_li = c.shrub_ih_li,
 water_ih_li =  c.water_ih_li
FROM dataprep.cy_interp as c
WHERE c.gid = priogrid_gid AND c.year=year_id;

DROP TABLE dataprep.cy_interp;

--carry forward bdists

with carry AS
(
    SELECT
      priogrid_gid as pgid,
      bdist1,
      bdist2,
      bdist3
    FROM staging.priogrid_year
    WHERE year_id = 2013
)
UPDATE staging.priogrid_year SET
  bdist1=carry.bdist1,
  bdist2=carry.bdist2,
  bdist3=carry.bdist3
FROM carry
WHERE
  year_id BETWEEN 2015 AND 2030
  AND
 priogrid_gid=pgid;
