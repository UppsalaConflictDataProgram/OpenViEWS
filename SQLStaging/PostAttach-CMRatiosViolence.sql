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
