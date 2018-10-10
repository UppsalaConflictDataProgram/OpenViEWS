DROP TABLE IF EXISTS landed.ensemble_pgm_eval_test;
CREATE TABLE landed.ensemble_pgm_eval_test AS 
SELECT 
sb.pg_id,
sb.month_id,
ebma."ebma_sb",
sb."ds_pgm_canon_nocm_eval_test_sb_calibrated",
sb."ds_pgm_canon_wcm_eval_test_sb_calibrated",
sb."ds_pgm_acled_nocm_eval_test_sb_calibrated",
sb."ds_pgm_acled_wcm_eval_test_sb_calibrated",
sb."osa_pgm_acled_nocm_eval_test_logit_fullsample_sb_calibrated",
sb."osa_pgm_acled_nocm_eval_test_rf_downsampled_sb_calibrated",
sb."osa_pgm_acled_wcm_eval_test_logit_fullsample_sb_calibrated",
sb."osa_pgm_acled_wcm_eval_test_rf_downsampled_sb_calibrated",
sb."osa_pgm_canon_nocm_eval_test_logit_fullsample_sb_calibrated",
sb."osa_pgm_canon_nocm_eval_test_rf_downsampled_sb_calibrated",
sb."osa_pgm_canon_wcm_eval_test_logit_fullsample_sb_calibrated",
sb."osa_pgm_canon_wcm_eval_test_rf_downsampled_sb_calibrated",
sb."ds_cm_canon_base_eval_test_sb_calibrated",
sb."ds_cm_acled_base_eval_test_sb_calibrated",
sb."osa_cm_canon_base_eval_test_logit_fullsample_sb_calibrated",
sb."osa_cm_acled_base_eval_test_logit_fullsample_sb_calibrated",
sb."osa_cm_canon_base_eval_test_rf_downsampled_sb_calibrated",
sb."osa_cm_acled_base_eval_test_rf_downsampled_sb_calibrated",
sb."CL_ds_pgm_canon_nocm_eval_test_sb_calibrated" AS "cl_ds_pgm_canon_nocm_eval_test_sb_calibrated",
sb."CL_ds_pgm_acled_nocm_eval_test_sb_calibrated" AS "cl_ds_pgm_acled_nocm_eval_test_sb_calibrated",
sb."CL_osa_pgm_canon_nocm_eval_test_logit_fullsample_sb_calibrated" AS "cl_osa_pgm_canon_nocm_eval_test_logit_fullsample_sb_calibrated",
sb."CL_osa_pgm_acled_nocm_eval_test_logit_fullsample_sb_calibrated" AS "cl_osa_pgm_acled_nocm_eval_test_logit_fullsample_sb_calibrated",
sb."CL_osa_pgm_canon_nocm_eval_test_rf_downsampled_sb_calibrated" AS "cl_osa_pgm_canon_nocm_eval_test_rf_downsampled_sb_calibrated",
sb."CL_osa_pgm_acled_nocm_eval_test_rf_downsampled_sb_calibrated" AS "cl_osa_pgm_acled_nocm_eval_test_rf_downsampled_sb_calibrated",
sb."average_nocm_sb",
sb."average_wcm_sb",
sb."average_cl_sb",
sb."average_all_sb",
sb."average_select_sb",ebma."ebma_ns",
ns."ds_pgm_canon_nocm_eval_test_ns_calibrated",
ns."ds_pgm_canon_wcm_eval_test_ns_calibrated",
ns."ds_pgm_acled_nocm_eval_test_ns_calibrated",
ns."ds_pgm_acled_wcm_eval_test_ns_calibrated",
ns."osa_pgm_acled_nocm_eval_test_logit_fullsample_ns_calibrated",
ns."osa_pgm_acled_nocm_eval_test_rf_downsampled_ns_calibrated",
ns."osa_pgm_acled_wcm_eval_test_logit_fullsample_ns_calibrated",
ns."osa_pgm_acled_wcm_eval_test_rf_downsampled_ns_calibrated",
ns."osa_pgm_canon_nocm_eval_test_logit_fullsample_ns_calibrated",
ns."osa_pgm_canon_nocm_eval_test_rf_downsampled_ns_calibrated",
ns."osa_pgm_canon_wcm_eval_test_logit_fullsample_ns_calibrated",
ns."osa_pgm_canon_wcm_eval_test_rf_downsampled_ns_calibrated",
ns."ds_cm_canon_base_eval_test_ns_calibrated",
ns."ds_cm_acled_base_eval_test_ns_calibrated",
ns."osa_cm_canon_base_eval_test_logit_fullsample_ns_calibrated",
ns."osa_cm_acled_base_eval_test_logit_fullsample_ns_calibrated",
ns."osa_cm_canon_base_eval_test_rf_downsampled_ns_calibrated",
ns."osa_cm_acled_base_eval_test_rf_downsampled_ns_calibrated",
ns."CL_ds_pgm_canon_nocm_eval_test_ns_calibrated" AS "cl_ds_pgm_canon_nocm_eval_test_ns_calibrated",
ns."CL_ds_pgm_acled_nocm_eval_test_ns_calibrated" AS "cl_ds_pgm_acled_nocm_eval_test_ns_calibrated",
ns."CL_osa_pgm_canon_nocm_eval_test_logit_fullsample_ns_calibrated" AS "cl_osa_pgm_canon_nocm_eval_test_logit_fullsample_ns_calibrated",
ns."CL_osa_pgm_acled_nocm_eval_test_logit_fullsample_ns_calibrated" AS "cl_osa_pgm_acled_nocm_eval_test_logit_fullsample_ns_calibrated",
ns."CL_osa_pgm_canon_nocm_eval_test_rf_downsampled_ns_calibrated" AS "cl_osa_pgm_canon_nocm_eval_test_rf_downsampled_ns_calibrated",
ns."CL_osa_pgm_acled_nocm_eval_test_rf_downsampled_ns_calibrated" AS "cl_osa_pgm_acled_nocm_eval_test_rf_downsampled_ns_calibrated",
ns."average_nocm_ns",
ns."average_wcm_ns",
ns."average_cl_ns",
ns."average_all_ns",
ns."average_select_ns",ebma."ebma_os",
os."ds_pgm_canon_nocm_eval_test_os_calibrated",
os."ds_pgm_canon_wcm_eval_test_os_calibrated",
os."ds_pgm_acled_nocm_eval_test_os_calibrated",
os."ds_pgm_acled_wcm_eval_test_os_calibrated",
os."osa_pgm_acled_nocm_eval_test_logit_fullsample_os_calibrated",
os."osa_pgm_acled_nocm_eval_test_rf_downsampled_os_calibrated",
os."osa_pgm_acled_wcm_eval_test_logit_fullsample_os_calibrated",
os."osa_pgm_acled_wcm_eval_test_rf_downsampled_os_calibrated",
os."osa_pgm_canon_nocm_eval_test_logit_fullsample_os_calibrated",
os."osa_pgm_canon_nocm_eval_test_rf_downsampled_os_calibrated",
os."osa_pgm_canon_wcm_eval_test_logit_fullsample_os_calibrated",
os."osa_pgm_canon_wcm_eval_test_rf_downsampled_os_calibrated",
os."ds_cm_canon_base_eval_test_os_calibrated",
os."ds_cm_acled_base_eval_test_os_calibrated",
os."osa_cm_canon_base_eval_test_logit_fullsample_os_calibrated",
os."osa_cm_acled_base_eval_test_logit_fullsample_os_calibrated",
os."osa_cm_canon_base_eval_test_rf_downsampled_os_calibrated",
os."osa_cm_acled_base_eval_test_rf_downsampled_os_calibrated",
os."CL_ds_pgm_canon_nocm_eval_test_os_calibrated" AS "cl_ds_pgm_canon_nocm_eval_test_os_calibrated",
os."CL_ds_pgm_acled_nocm_eval_test_os_calibrated" AS "cl_ds_pgm_acled_nocm_eval_test_os_calibrated",
os."CL_osa_pgm_canon_nocm_eval_test_logit_fullsample_os_calibrated" AS "cl_osa_pgm_canon_nocm_eval_test_logit_fullsample_os_calibrated",
os."CL_osa_pgm_acled_nocm_eval_test_logit_fullsample_os_calibrated" AS "cl_osa_pgm_acled_nocm_eval_test_logit_fullsample_os_calibrated",
os."CL_osa_pgm_canon_nocm_eval_test_rf_downsampled_os_calibrated" AS "cl_osa_pgm_canon_nocm_eval_test_rf_downsampled_os_calibrated",
os."CL_osa_pgm_acled_nocm_eval_test_rf_downsampled_os_calibrated" AS "cl_osa_pgm_acled_nocm_eval_test_rf_downsampled_os_calibrated",
os."average_nocm_os",
os."average_wcm_os",
os."average_cl_os",
os."average_all_os",
os."average_select_os"
FROM
    landed.sb_ensemble_eval_pgm AS sb
INNER JOIN
    landed.ns_ensemble_eval_pgm AS ns
ON
    sb.pg_id=ns.pg_id
AND
    sb.month_id=ns.month_id
INNER JOIN
    landed.os_ensemble_eval_pgm AS os
ON
    sb.pg_id=os.pg_id
AND
    sb.month_id=os.month_id
INNER JOIN 
    landed.ebma_eval_pgm AS ebma
ON
    sb.pg_id=ebma.pg_id
AND
    sb.month_id=ebma.month_id
;