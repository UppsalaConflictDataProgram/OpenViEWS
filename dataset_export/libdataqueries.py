data_queries = {
'ucdp_month_country':'''
SELECT 
id,
gwcode,
month_id,
year_id as year,
month,
ged_dummy_sb,
ged_count_sb,
ged_best_sb,
ged_dummy_ns,
ged_count_ns,
ged_best_ns,
ged_dummy_os,
ged_count_os,
ged_best_os,
ged_count_sb_lag1,
ged_count_ns_lag1,
ged_count_os_lag1,
ged_best_sb_lag1,
ged_best_ns_lag1,
ged_best_os_lag1
FROM preflight.flight_cm WHERE month_id BETWEEN :s AND :e AND 
(gwcode BETWEEN 400 and 627 OR gwcode=651) 
''',
'ucdp_month_priogrid':'''SELECT
  id,
  pg_id,
  month_id,
  year_id as year,
  CASE WHEN month_id%12=0 THEN 12 ELSE month_id%12 END as month,
  gwcode,
  ged_dummy_sb,
  ged_count_sb,
  ged_best_sb,
  ged_dummy_ns,
  ged_count_ns,
  ged_best_ns,
  ged_dummy_os,
  ged_count_os,
  ged_best_os
FROM preflight.flight_pgm WHERE month_id BETWEEN :s AND :e ORDER BY month_id,pg_id''',
  'imputted_priogrid':''' SELECT
*
FROM left_imputation.pgm WHERE month_id BETWEEN :s AND :e
'''}
