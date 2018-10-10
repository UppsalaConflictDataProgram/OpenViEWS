-- we have to decide how we interpolate and what we do with the other variables.

ALTER TABLE staging.priogrid_year ADD COLUMN bdist1 DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN bdist2 DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN bdist3 DOUBLE PRECISION;
ALTER TABLE staging.priogrid_year ADD COLUMN gwarea DOUBLE PRECISION;

with py_ext AS
(
    SELECT
      gid,
      bdist1,
      bdist2,
      bdist3,
      gwarea,
      year :: INT                            AS year,
      gwno :: INT                            AS gwno
    FROM
      dataprep.prio_yearly
),
c_ext AS
  (
  SELECT
    country_year.id as country_year_id,
    country_year.year_id, country.gwcode
  FROM
  staging.country, staging.country_year
  WHERE
    country.id=country_year.country_id
  ),
py_prep AS
(
SELECT
  py_ext.*,
  c_ext.country_year_id
FROM
  py_ext, c_ext
WHERE
  py_ext.year=c_ext.year_id AND py_ext.gwno=c_ext.gwcode
)
UPDATE staging.priogrid_year SET
  bdist1 = py_prep.bdist1,
  bdist2 = py_prep.bdist2,
  bdist3 = py_prep.bdist3,
  gwarea = py_prep.gwarea,
  country_year_id = py_prep.country_year_id
FROM py_prep
WHERE priogrid_gid=py_prep.gid AND year_id=py_prep.year;

-- Extrapolate the country for each PGY to 2030:

WITH
    a AS (SELECT
            priogrid_gid,
            country_year_id
          FROM staging.priogrid_year
          WHERE year_id = 2014),
    tojoin AS (SELECT
                 id AS pgy_id,
                 priogrid_gid,
                 year_id
               FROM staging.priogrid_year
               WHERE year_id BETWEEN 2015 AND 2030),
    c2pg AS
  (
      SELECT
        a.priogrid_gid,
        staging.country_year.country_id
      FROM a, staging.country_year
      WHERE a.country_year_id = staging.country_year.id
  ),
    pg2c AS
  (
      SELECT
        tojoin.*,
        c2pg.country_id
      FROM tojoin, c2pg
      WHERE tojoin.priogrid_gid = c2pg.priogrid_gid
  ),
    toupdate AS
  (
      SELECT
        pg2c.*,
        cy.id AS cy_id
      FROM pg2c, staging.country_year AS cy
      WHERE (cy.country_id = pg2c.country_id AND cy.year_id = pg2c.year_id)
  )
UPDATE staging.priogrid_year
SET
  country_year_id = toupdate.cy_id
FROM toupdate
WHERE
  pgy_id = staging.priogrid_year.id;

VACUUM ANALYZE;
