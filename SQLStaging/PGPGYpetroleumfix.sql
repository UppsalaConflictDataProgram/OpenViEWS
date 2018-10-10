ALTER TABLE staging.priogrid ADD COLUMN petroleum_merged INT;
UPDATE staging.priogrid SET petroleum_merged=1 WHERE petroleum_s=1;
UPDATE staging.priogrid SET petroleum_merged=1 WHERE gid IN
        (SELECT gid FROM dataprep.prio_yearly WHERE petroleum_y=1);
UPDATE staging.priogrid SET petroleum_merged=0 WHERE petroleum_merged IS NULL;


ALTER TABLE staging.priogrid_year ADD COLUMN petroleum_merged_yearly INT;
UPDATE staging.priogrid_year SET petroleum_merged_yearly=1 WHERE petroleum_y=1;
UPDATE staging.priogrid_year SET petroleum_merged_yearly=1 WHERE priogrid_gid IN
(SELECT gid FROM staging.priogrid WHERE petroleum_s=1);
UPDATE staging.priogrid_year SET petroleum_merged_yearly=0 WHERE petroleum_merged_yearly IS NULL;
