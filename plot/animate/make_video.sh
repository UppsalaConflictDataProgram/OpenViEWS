DIR_OUTPUT=/storage/runs/current/video
mkdir -p $DIR_OUTPUT

glob_ensemble_fcast='/storage/runs/current/maps/landed/ensemble_pgm_fcast_test/average_select_sb/*.png'
glob_ds_fcast='/storage/runs/current/maps/landed/ensemble_pgm_fcast_test/ds_pgm_acled_wcm_fcast_test_sb_calibrated/*.png'
glob_osa_fcast='/storage/runs/current/maps/landed/ensemble_pgm_fcast_test/osa_pgm_canon_wcm_fcast_test_rf_downsampled_sb_calibrated/*.png'
glob_ensemble_eval='/storage/runs/current/maps/landed/ensemble_pgm_eval_test/average_select_sb/*.png'
glob_ds_eval='/storage/runs/current/maps/landed/ensemble_pgm_eval_test/ds_pgm_acled_wcm_eval_test_sb_calibrated/*.png'
glob_osa_eval='/storage/runs/current/maps/landed/ensemble_pgm_eval_test/osa_pgm_canon_wcm_eval_test_rf_downsampled_sb_calibrated/*.png'


ffmpeg -y -r 6 -pattern_type glob -i "$glob_ensemble_fcast" $DIR_OUTPUT/ensemble_fcast.mp4
ffmpeg -y -r 6 -pattern_type glob -i "$glob_ds_fcast" $DIR_OUTPUT/ds_fcast.mp4
ffmpeg -y -r 6 -pattern_type glob -i "$glob_osa_fcast" $DIR_OUTPUT/osa_fcast.mp4

ffmpeg -y -r 6 -pattern_type glob -i "$glob_ensemble_eval" $DIR_OUTPUT/ensemble_eval.mp4
ffmpeg -y -r 6 -pattern_type glob -i "$glob_ds_eval" $DIR_OUTPUT/ds_eval.mp4
ffmpeg -y -r 6 -pattern_type glob -i "$glob_osa_eval" $DIR_OUTPUT/osa_eval.mp4