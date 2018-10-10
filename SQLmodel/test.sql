INSERT INTO staging.priogrid_month
(
  priogrid_gid,
  month_id
)
SELECT
  staging.priogrid.gid,
  staging.month.id
FROM staging.month CROSS JOIN staging.priogrid;


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
