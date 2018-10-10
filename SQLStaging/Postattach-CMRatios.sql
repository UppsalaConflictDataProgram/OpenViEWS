-- Compute the ratio of all cells with events / ratio of total cells for each type of violence
-- Conveniently, the sum of all cells with events is the sum of all dummified event counts (since it reduces >=1 to 1).

DROP TABLE IF EXISTS cm_ratios;
CREATE TABLE cm_ratios AS
SELECT
  country_month_id as cm_id,
  sum(to_dummy(ged_count_os)) as os_cells,
  sum(to_dummy(ged_count_ns)) as ns_cells,
  sum(to_dummy(ged_count_sb)) as sb_cells,
  sum(to_dummy(acled_count_pr)) as pr_cells,
  count(*) as total_cells
FROM staging.priogrid_month
GROUP BY country_month_id;



ALTER TABLE staging.country_month ADD COLUMN pgm_ratio_sb FLOAT;
ALTER TABLE staging.country_month ADD COLUMN pgm_ratio_ns FLOAT;
ALTER TABLE staging.country_month ADD COLUMN pgm_ratio_os FLOAT;
ALTER TABLE staging.country_month ADD COLUMN pgm_ratio_pr FLOAT;

UPDATE staging.country_month
    SET
      pgm_ratio_sb = c.sb_cells::float/total_cells::float,
      pgm_ratio_ns = c.ns_cells::float/total_cells::float,
      pgm_ratio_os = c.os_cells::float/total_cells::float,
      pgm_ratio_pr = c.pr_cells::float/total_cells::float
    FROM
    cm_ratios as c
WHERE c.cm_id = id;


-- Exclude fringe countries captured with only 1-2 cells in our Africa Dataset, e.g. Israel or Spain.

UPDATE staging.country_month SET
  pgm_ratio_sb = NULL,
  pgm_ratio_ns = NULL,
  pgm_ratio_os = NULL,
  pgm_ratio_pr = NULL
WHERE
country_id_to_gwno(country_id::int) NOT BETWEEN 400 AND 627
AND
country_id_to_gwno(country_id::int)<>651;
