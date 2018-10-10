ALTER TABLE staging.priogrid ADD COLUMN dist_diamsec_s_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.diamsec_s IS NOT NULL),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_diamsec_s_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;

ALTER TABLE staging.priogrid ADD COLUMN dist_petroleum_merged_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.petroleum_merged=1),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_petroleum_merged_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;

ALTER TABLE staging.priogrid ADD COLUMN dist_petroleum_s_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.petroleum_s IS NOT NULL),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_petroleum_s_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;



ALTER TABLE staging.priogrid ADD COLUMN dist_goldsurface_s_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.goldsurface_s IS NOT NULL),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_goldsurface_s_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;

ALTER TABLE staging.priogrid ADD COLUMN dist_goldplace_s_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.goldplacer_s IS NOT NULL),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_goldplace_s_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;

ALTER TABLE staging.priogrid ADD COLUMN dist_goldvein_s_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.goldvein_s IS NOT NULL),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_goldvein_s_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;


ALTER TABLE staging.priogrid ADD COLUMN dist_gem_s_wgs float;

with b AS (SELECT geom FROM staging.priogrid WHERE priogrid.gem_s IS NOT NULL),
toupdate AS (SELECT a.gid, min(st_distance(a.geom, b.geom)) as distance FROM staging.priogrid a, b GROUP BY a.gid)
UPDATE staging.priogrid
SET dist_gem_s_wgs = toupdate.distance
FROM toupdate
WHERE toupdate.gid=priogrid.gid;
