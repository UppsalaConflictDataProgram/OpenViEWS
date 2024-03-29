SELECT
  pgm.pg_id,
  pgm.month_id,
  pgm.country_id,
  preflight_pgm.ged_dummy_sb_naive AS ged_dummy_sb,
  pgm.bdist3,
  pgm.ttime_mean,
  pgm.capdist_li,
  pgm.pop_li_gpw_sum,
  pgm.dist_diamsec_s_wgs,
  pgm.dist_petroleum_s_wgs,
  pgm.gcp_li_mer,
  pgm.imr_mean,
  pgm.mountains_mean,
  pgm.urban_ih_li,
  public.to_dummy(CAST(pgm.excluded_li AS INT)) AS excluded_dummy_li,
  pgm.agri_ih_li,
  pgm.barren_ih_li,
  pgm.forest_ih_li,
  pgm.savanna_ih_li,
  pgm.shrub_ih_li,
  pgm.pasture_ih_li,
  cm.fvp_lngdpcap_nonoilrent,
  cm.fvp_lngdpcap_oilrent,
  cm.fvp_population200,
  cm.fvp_grgdpcap_oilrent,
  cm.fvp_grgdpcap_nonoilrent,
  cm.fvp_timeindep,
  cm.fvp_timesincepreindepwar,
  cm.fvp_timesinceregimechange,
  cm.fvp_demo,
  cm.fvp_semi,
  cm.ssp2_edu_sec_15_24_prop,
  cm.fvp_prop_excluded,
  cm.ssp2_urban_share_iiasa
FROM
  launched.pgmimp1bnd as pgm
LEFT JOIN
  launched.cm_imp_1 as cm
  ON
    pgm.country_id=cm.country_id
  AND
    pgm.month_id=cm.month_id
LEFT JOIN
    left_imputation.pgm AS geoimp
  ON
    pgm.pg_id=geoimp.priogrid_gid
  AND
    pgm.month_id=geoimp.month_id
LEFT JOIN
    preflight.flight_pgm AS preflight_pgm
  ON
    preflight_pgm.pg_id=pgm.pg_id
  AND
    preflight_pgm.month_id=pgm.month_id;