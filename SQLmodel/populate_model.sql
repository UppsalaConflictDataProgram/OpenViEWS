-- Minimally populate the tables:

-- Populate priogrid gid

INSERT INTO staging.priogrid
(
gid
)
  (
      SELECT gid FROM dataprep.prio_static
  );
  
-- populate priogrid with values

with transport as
(
    SELECT
      priogrid,
      row,
      col,
      xcoord :: NUMERIC(6, 2) AS longitude,
      ycoord :: NUMERIC(6, 2) AS latitude,
      public.ST_GeometryN(
          public.st_geomfromewkt(geom), 1
      ) as g
    FROM dataprep.prio_geom
)
UPDATE staging.priogrid SET
latitude=transport.latitude,
longitude=transport.longitude,
col=transport.col,
row=transport.row, 
geom=transport.g
FROM transport
WHERE (gid=transport.priogrid);

-- Populate years

INSERT INTO staging.year
(
  year
)
  (
     SELECT generate_series(1980,2100)
  );


INSERT INTO staging.month
(
  year_id,
  month)
  (
    SELECT
      staging.year.year,
      generate_series(1, 12)
    FROM staging.year
  );


-- POPULATE Priogrid_year

INSERT INTO staging.priogrid_year
(
  priogrid_gid,
  year_id
)
SELECT
  staging.priogrid.gid,
  staging.year.year
FROM staging.year CROSS JOIN staging.priogrid;



-- POPULATE Priogrid_month

INSERT INTO staging.priogrid_month
(
  priogrid_gid,
  month_id
)
SELECT
  staging.priogrid.gid,
  staging.month.id
FROM staging.month CROSS JOIN staging.priogrid;


-- ADD COUNTRY

ALTER TABLE "staging"."country_month" DROP CONSTRAINT IF EXISTS "country_id_fk";
ALTER TABLE "staging"."country_year" DROP CONSTRAINT IF EXISTS "country_id_fk";
DROP TABLE IF EXISTS "staging"."country";
CREATE TABLE "staging"."country" AS
  (SELECT
     gid        AS id,
     cntry_name AS name,
     area       AS area,
     capname,
     caplong,
     caplat,
     gwcode,
     gwsyear,
     gwsmonth,
     gwsday,
     gweyear,
     gwemonth,
     gweday,
     isoname,
     iso1num    AS isonum,
     iso1al3    AS isoab,
     geom
   FROM dataprep.cshapes);

ALTER TABLE staging.country ADD PRIMARY KEY (id);
ALTER TABLE "staging"."country_month" ADD CONSTRAINT "country_id_fk" FOREIGN KEY ("country_id") REFERENCES "staging"."country" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "staging"."country_year" ADD CONSTRAINT "country_id_fk" FOREIGN KEY ("country_id") REFERENCES "staging"."country" ("id") ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

-- POPULATE country-year

INSERT INTO staging.country_year (country_id, year_id)
  (
    WITH crossyear AS (
        SELECT
          staging.country.id,
          staging.country.gwsyear,
          staging.country.gweyear,
          staging.year.year
        FROM staging.country
          CROSS JOIN staging.year
    )
    SELECT id, year
    FROM crossyear
    WHERE (gwsyear <= year) AND (gweyear >= year OR gweyear = (SELECT max(gweyear)
                                                               FROM crossyear))
    ORDER BY id, year
  );

-- POPULATE country-month

-- This works like this:
-- Calculates the validity interval for each country
-- Extrapolates all end-dates that in cshapes go to the maximum of the cshape to 2100-31-12
-- Calculates the span of a month
-- Inserts into country_month only those country_months that overlap the cshape country_months.

INSERT INTO staging.country_month
(country_id, month_id)
  (
    WITH country_extracted AS
    (
        SELECT
          id                       AS country_id,
          TO_DATE(TO_CHAR(staging.country.gwsyear, '9999') || TO_CHAR(staging.country.gwsmonth, 'FM00') || '01',
                  'YYYYMMDD')      AS validity_start,
          public.last_day_month(
              TO_DATE(TO_CHAR(staging.country.gweyear, '9999') || TO_CHAR(staging.country.gwemonth, 'FM00') || '01',
                      'YYYYMMDD')) AS validity_end
        FROM staging.country
        WHERE staging.country.gweyear > 0
    ),
        month_extracted AS
      (
          SELECT
            id                       AS month_id,
            TO_DATE(TO_CHAR(staging.month.year_id, '9999') || TO_CHAR(staging.month.month, 'FM00') || '01',
                    'YYYYMMDD')      AS month_start,
            public.last_day_month(
                TO_DATE(TO_CHAR(staging.month.year_id, '9999') || TO_CHAR(staging.month.month, 'FM00') || '01',
                        'YYYYMMDD')) AS month_end
          FROM staging.month
      ),
        country_prolonged AS
      (
          SELECT
            country_id,
            validity_start,
            CASE WHEN validity_end = (SELECT max(validity_end)
                                      FROM country_extracted)
              THEN '2100-12-31' :: DATE
            ELSE validity_end
            END AS validity_end
          FROM country_extracted),
        cross_month AS
      (
          SELECT
            country_prolonged.*,
            month_extracted.*
          FROM country_prolonged
            CROSS JOIN month_extracted
      )
    SELECT
      country_id,
      month_id
    FROM cross_month
    WHERE (validity_start, validity_end) OVERLAPS (month_start, month_end)
  )


-- Populate country-month. This takes ~7h to run on our machines with everything properly indexed. Without, probably takes a lifetime, don't try
-- Currently only populates priogrid-month with a link to priogrid-year.

ALTER TABLE staging.priogrid_month ADD COLUMN priogrid_year_id int8;

CREATE INDEX priogrid_year_idx ON views.staging.priogrid_year(year_id,priogrid_gid);
CREATE INDEX month_idx ON views.staging.month(id);
CREATE INDEX priogrid_month_idx ON views.staging.priogrid_month(id);

WITH a AS (SELECT
             priogrid_month.id AS pm_id,
             priogrid_gid,
             month.year_id,
             month.month
           FROM staging.priogrid_month, staging.month
           WHERE priogrid_month.month_id = month.id),
    b AS (SELECT
            a.*,
            priogrid_year.id AS py_id
          FROM a, staging.priogrid_year
          WHERE a.priogrid_gid = priogrid_year.priogrid_gid AND a.year_id = priogrid_year.year_id)
UPDATE staging.priogrid_month
SET
  priogrid_year_id = b.py_id
FROM b
WHERE priogrid_month.id = b.pm_id;

VACUUM ANALYZE;

ALTER TABLE "staging"."priogrid_month" ADD CONSTRAINT "priogrid_year_id_fk"
FOREIGN KEY ("priogrid_year_id") REFERENCES "staging"."priogrid_year" ("id")
ON DELETE RESTRICT ON UPDATE RESTRICT DEFERRABLE INITIALLY DEFERRED;

-- since I'm still populating the database, and this isn't the production flow, drop indexes.
DROP INDEX IF EXISTS staging.priogrid_year_idx;
DROP INDEX IF EXISTS staging.month_idx;
DROP INDEX IF EXISTS staging.priogrid_month_idx;
