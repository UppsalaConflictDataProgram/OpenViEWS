DROP TABLE IF EXISTS landed.ensemble_cm_eval_test;
CREATE TABLE landed.ensemble_cm_eval_test AS 
SELECT 
sb.country_id,
sb.month_id,
sb.ds_cm_canon_base_eval_test_sb_calibrated,
sb.ds_cm_acled_base_eval_test_sb_calibrated,
sb.osa_cm_acled_base_eval_test_logit_fullsample_sb_calibrated,
sb.osa_cm_acled_base_eval_test_rf_downsampled_sb_calibrated,
sb.osa_cm_canon_base_eval_test_logit_fullsample_sb_calibrated,
sb.osa_cm_canon_base_eval_test_rf_downsampled_sb_calibrated,
sb.average_sb,
sb.ebma_sb,
ns.ds_cm_canon_base_eval_test_ns_calibrated,
ns.ds_cm_acled_base_eval_test_ns_calibrated,
ns.osa_cm_acled_base_eval_test_logit_fullsample_ns_calibrated,
ns.osa_cm_acled_base_eval_test_rf_downsampled_ns_calibrated,
ns.osa_cm_canon_base_eval_test_logit_fullsample_ns_calibrated,
ns.osa_cm_canon_base_eval_test_rf_downsampled_ns_calibrated,
ns.average_ns,
ns.ebma_ns,
os.ds_cm_canon_base_eval_test_os_calibrated,
os.ds_cm_acled_base_eval_test_os_calibrated,
os.osa_cm_acled_base_eval_test_logit_fullsample_os_calibrated,
os.osa_cm_acled_base_eval_test_rf_downsampled_os_calibrated,
os.osa_cm_canon_base_eval_test_logit_fullsample_os_calibrated,
os.osa_cm_canon_base_eval_test_rf_downsampled_os_calibrated,
os.average_os,
os.ebma_os
FROM
    landed.sb_ensemble_eval_cm AS sb
INNER JOIN
    landed.ns_ensemble_eval_cm AS ns
ON
    sb.country_id=ns.country_id
AND
    sb.month_id=ns.month_id
INNER JOIN
    landed.os_ensemble_eval_cm AS os
ON
    sb.country_id=os.country_id
AND
    sb.month_id=os.month_id;