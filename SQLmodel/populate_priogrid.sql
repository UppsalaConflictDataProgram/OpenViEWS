ALTER TABLE staging.priogrid ADD COLUMN cmr_max DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN cmr_mean DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN cmr_min DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN cmr_sd DOUBLE PRECISION;

ALTER TABLE staging.priogrid ADD COLUMN diamprim_s INT;
ALTER TABLE staging.priogrid ADD COLUMN diamsec_s INT;
ALTER TABLE staging.priogrid ADD COLUMN gem_s INT;
ALTER TABLE staging.priogrid ADD COLUMN goldplacer_s INT;
ALTER TABLE staging.priogrid ADD COLUMN goldvein_s INT;
ALTER TABLE staging.priogrid ADD COLUMN goldsurface_s INT;
ALTER TABLE staging.priogrid ADD COLUMN petroleum_s INT;

ALTER TABLE staging.priogrid ADD COLUMN maincrop INT;
ALTER TABLE staging.priogrid ADD COLUMN growstart INT;
ALTER TABLE staging.priogrid ADD COLUMN growend INT;
ALTER TABLE staging.priogrid ADD COLUMN rainseas INT;

ALTER TABLE staging.priogrid ADD COLUMN ttime_max INT;
ALTER TABLE staging.priogrid ADD COLUMN ttime_mean DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN ttime_min INT;
ALTER TABLE staging.priogrid ADD COLUMN ttime_sd DOUBLE PRECISION;

ALTER TABLE staging.priogrid ADD COLUMN imr_max DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN imr_mean DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN imr_min DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN imr_sd DOUBLE PRECISION;

ALTER TABLE staging.priogrid ADD COLUMN landarea DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN agri_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN aquaveg_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN barren_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN forest_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN shrub_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN urban_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN water_gc DOUBLE PRECISION;
ALTER TABLE staging.priogrid ADD COLUMN mountains_mean DOUBLE PRECISION;


UPDATE staging.priogrid SET
  cmr_max = dataprep.prio_static.cmr_max,
  cmr_mean = dataprep.prio_static.cmr_mean,
  cmr_min = dataprep.prio_static.cmr_min,
  cmr_sd = dataprep.prio_static.cmr_sd,

  diamprim_s = dataprep.prio_static.diamprim_s::int,
  diamsec_s = dataprep.prio_static.diamsec_s::int,
  gem_s = dataprep.prio_static.gem_s::int,
  goldplacer_s = dataprep.prio_static.goldplacer_s::int,
  goldvein_s = dataprep.prio_static.goldvein_s::int,
  goldsurface_s = dataprep.prio_static.goldsurface_s::int,
  petroleum_s = dataprep.prio_static.petroleum_s::int,

  maincrop = dataprep.prio_static.maincrop::int,
  growstart = dataprep.prio_static.growstart::int,
  growend = dataprep.prio_static.growend::int,
  rainseas = dataprep.prio_static.rainseas::int,

  ttime_max = dataprep.prio_static.ttime_max::int,
  ttime_min = dataprep.prio_static.ttime_min::int,
  ttime_mean = dataprep.prio_static.ttime_mean,
  ttime_sd = dataprep.prio_static.ttime_sd,

  imr_mean = dataprep.prio_static.imr_mean,
  imr_min = dataprep.prio_static.imr_min,
  imr_max = dataprep.prio_static.imr_max,
  imr_sd = dataprep.prio_static.imr_sd,

  landarea = dataprep.prio_static.landarea,
  agri_gc = dataprep.prio_static.agri_gc,
  aquaveg_gc = dataprep.prio_static.aquaveg_gc,
  barren_gc = dataprep.prio_static.barren_gc,
  forest_gc = dataprep.prio_static.forest_gc,
  shrub_gc = dataprep.prio_static.shrub_gc,
  urban_gc = dataprep.prio_static.urban_gc,
  water_gc = dataprep.prio_static.water_gc,
  mountains_mean = dataprep.prio_static.mountains_mean

FROM
dataprep.prio_static
WHERE staging.priogrid.gid=dataprep.prio_static.gid;

VACUUM ANALYZE;
