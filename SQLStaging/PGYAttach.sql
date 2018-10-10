CREATE TABLE dataprep.prio_yearly_li AS
    SELECT
      priogrid_gid,
      year_id,
      public.interpolate_priogrid_year('dataprep', 'prio_yearly', 'gcp_ppp', priogrid_gid, year_id) as gcp_li_ppp,
      public.interpolate_priogrid_year('dataprep', 'prio_yearly', 'gcp_mer', priogrid_gid, year_id) as gcp_li_mer,
      public.interpolate_priogrid_year('dataprep', 'prio_yearly', 'pop_gpw_sum', priogrid_gid, year_id) as pop_li_gpw_sum
    FROM staging.priogrid_year WHERE year_id<=2030;

ALTER TABLE dataprep.prio_yearly_li ADD PRIMARY KEY (priogrid_gid,year_id);
CREATE INDEX prio_yearly_li_dix ON dataprep.prio_yearly_li (priogrid_gid,year_id);


ALTER TABLE staging.priogrid_year ADD COLUMN gcp_li_ppp DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN gcp_li_mer DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN pop_li_gpw_sum DOUBLE PRECISION;

UPDATE staging.priogrid_year SET
    gcp_li_mer=dataprep.prio_yearly_li.gcp_li_mer,
    gcp_li_ppp=dataprep.prio_yearly_li.gcp_li_ppp,
    pop_li_gpw_sum=dataprep.prio_yearly_li.pop_li_gpw_sum
FROM dataprep.prio_yearly_li
WHERE (staging.priogrid_year.year_id = dataprep.prio_yearly_li.year_id AND
       staging.priogrid_year.priogrid_gid = dataprep.prio_yearly_li.priogrid_gid)

DROP TABLE dataprep.prio_yearly_li;
VACUUM ANALYSE;

-- compute priogrid_year

ALTER TABLE staging.priogrid_year ADD COLUMN agri_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN barren_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN forest_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN grass_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN savanna_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN pasture_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN shrub_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN urban_ih DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN water_ih DOUBLE PRECISION;


ALTER TABLE staging.priogrid_year ADD COLUMN diamsec_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN diamprim_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN drug_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN gem_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN goldplacer_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN goldvein_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN goldsurface_y DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN petroleum_y DOUBLE PRECISION;


ALTER TABLE staging.priogrid_year ADD COLUMN droughtcrop_speibase DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtcrop_speigdm DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtcrop_spi DOUBLE PRECISION;

ALTER TABLE staging.priogrid_year ADD COLUMN droughtstart_speibase DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtstart_speigdm DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtstart_spi DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtend_speibase DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtend_speigdm DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtend_spi DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtyr_speibase DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtyr_speigdm DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN droughtyr_spi DOUBLE PRECISION;

ALTER TABLE staging.priogrid_year ADD COLUMN excluded DOUBLE PRECISION;

ALTER TABLE staging.priogrid_year ADD COLUMN irrig_sum DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN irrig_li_sum DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN irrig_sd DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN irrig_li_sd DOUBLE PRECISION;

ALTER TABLE staging.priogrid_year ADD COLUMN pop_hyd_li_sum DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN pop_hyd_sum DOUBLE PRECISION;

ALTER TABLE staging.priogrid_year ADD COLUMN nlights_mean DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN nlights_min DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN nlights_max DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN nlights_sd DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN nlights_calib_mean DOUBLE PRECISION;



UPDATE staging.priogrid_year SET
    pop_hyd_li_sum = public.interpolate_priogrid_year('dataprep', 'prio_yearly', 'pop_hyd_sum', priogrid_gid::bigint, year_id::BIGINT),
    irrig_li_sum = public.interpolate_priogrid_year('dataprep', 'prio_yearly', 'irrig_sum', priogrid_gid::bigint, year_id::BIGINT),
    irrig_li_sd = public.interpolate_priogrid_year('dataprep', 'prio_yearly', 'irrig_sd', priogrid_gid::bigint, year_id::BIGINT)
  FROM dataprep.prio_yearly WHERE year_id BETWEEN 1980 AND 2020;


UPDATE staging.priogrid_year SET
agri_ih = a.agri_ih, barren_ih = a.barren_ih, forest_ih=a.forest_ih,
grass_ih = a.grass_ih, savanna_ih = a.savanna_ih, pasture_ih=a.pasture_ih,
shrub_ih = a.shrub_ih, urban_ih = a.urban_ih, water_ih = a.water_ih,
diamsec_y = a.diamsec_y, diamprim_y = a.diamprim_y, drug_y = a.drug_y,
gem_y = a.gem_y, goldplacer_y = a.goldplacer_y, goldvein_y = a.goldvein_y,
goldsurface_y = a.goldsurface_y, petroleum_y=a.petroleum_y,
droughtcrop_speibase = a.droughtcrop_speibase,
droughtcrop_speigdm = a.droughtcrop_speigdm, droughtcrop_spi = a.droughtcrop_spi,
droughtstart_speibase = a.droughtstart_speibase, droughtstart_speigdm = a.droughtstart_speigdm,
droughtstart_spi = a.droughtstart_spi, droughtend_speibase = a.droughtend_speibase,
droughtend_speigdm = a.droughtend_speigdm, droughtend_spi = a.droughtend_spi,
droughtyr_speibase = a.droughtyr_speibase, droughtyr_speigdm = a.droughtyr_speigdm,
droughtyr_spi = a.droughtyr_spi, excluded = a.excluded, irrig_sum = a.irrig_sum,
irrig_sd = a.irrig_sd, pop_hyd_sum=a.pop_hyd_sum,
nlights_mean = a.nlights_mean, nlights_min = a.nlights_min,
nlights_max = a.nlights_max, nlights_sd = a.nlights_sd,
nlights_calib_mean = a.nlights_calib_mean
FROM
dataprep.prio_yearly AS a
WHERE a.year = year_id AND a.gid = priogrid_gid;

ALTER TABLE staging.priogrid_year ADD COLUMN capdist double precison;

UPDATE staging.priogrid_year SET capdist = a.capdist 
FROM dataprep.prio_yearly as a WHERE a.year = year_id AND a.gid = priogrid_gid;


