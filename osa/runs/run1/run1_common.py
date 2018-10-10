import sys 

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, "../../..")
import views_utils.dbutils as dbutils
from nstep.wrapper_sm import SMLogit

uname    = "VIEWSADMIN"
prefix   = "postgresql"
db       = "views"
port     = "5432"
hostname = "VIEWSHOST"
connectstring = dbutils.make_connectstring(prefix, db, uname, hostname, port)

table_input = {
    'connectstring' : connectstring,
    'schema'    : 'launched',
    'table'     : 'ds_w_acled',
    'timevar'   : 'month_id',
    'groupvar'  : 'pg_id'}

share_zeros_full = 1
share_ones_full = 1
share_zeros_tenth = 0.1
steps = [1, 6, 12, 24, 36]

train_start_canon    = 121
train_start_acled    = 205
train_end_calib      = 372
train_end_test       = 408
forecast_start_test  = 409
forecast_start_calib = 373
forecast_end_test    = 444
forecast_end_calib   = 408


rf_500 =  RandomForestClassifier(n_estimators = 500)
scaler =  StandardScaler()
pipe_rf_500 = Pipeline([
    ('scaler', scaler),
    ('rf', rf_500)])


features_canon_sb = [
    "decay_12_cw_ged_dummy_sb_0", 
    "decay_12_cw_ged_dummy_ns_0", 
    "decay_12_cw_ged_dummy_os_0", 
    "l1_ged_dummy_sb", 
    "l2_ged_dummy_sb", 
    "l3_ged_dummy_sb", 
    "l4_ged_dummy_sb", 
    "l5_ged_dummy_sb", 
    "l6_ged_dummy_sb", 
    "l7_ged_dummy_sb", 
    "l8_ged_dummy_sb", 
    "l9_ged_dummy_sb", 
    "l10_ged_dummy_sb", 
    "l11_ged_dummy_sb", 
    "l12_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_os", 
    "q_1_1_l2_ged_dummy_sb", 
    "q_1_1_l3_ged_dummy_sb", 
    "ln_bdist3", 
    "ln_ttime", 
    "ln_capdist", 
    "ln_pop", 
    "ln_dist_diamsec", 
    "ln_dist_petroleum", 
    "gcp_li_mer", 
    "imr_mean", 
    "mountains_mean", 
    "urban_ih_li",  
    "excluded_dummy_li", 
    "agri_ih_li", 
    "barren_ih_li",  
    "forest_ih_li",  
    "savanna_ih_li",  
    "shrub_ih_li",  
    "pasture_ih_li"]

features_canon_ns = [
    "decay_12_cw_ged_dummy_sb_0", 
    "decay_12_cw_ged_dummy_ns_0", 
    "decay_12_cw_ged_dummy_os_0", 
    "l1_ged_dummy_ns", 
    "l2_ged_dummy_ns", 
    "l3_ged_dummy_ns", 
    "l4_ged_dummy_ns", 
    "l5_ged_dummy_ns", 
    "l6_ged_dummy_ns", 
    "l7_ged_dummy_ns", 
    "l8_ged_dummy_ns", 
    "l9_ged_dummy_ns", 
    "l10_ged_dummy_ns", 
    "l11_ged_dummy_ns", 
    "l12_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_os", 
    "q_1_1_l2_ged_dummy_ns", 
    "q_1_1_l3_ged_dummy_ns", 
    "ln_bdist3", 
    "ln_ttime", 
    "ln_capdist", 
    "ln_pop", 
    "ln_dist_diamsec", 
    "ln_dist_petroleum", 
    "gcp_li_mer", 
    "imr_mean", 
    "mountains_mean", 
    "urban_ih_li",  
    "excluded_dummy_li", 
    "agri_ih_li", 
    "barren_ih_li",  
    "forest_ih_li",  
    "savanna_ih_li",  
    "shrub_ih_li",  
    "pasture_ih_li"]

features_canon_os = [
    "decay_12_cw_ged_dummy_sb_0",
    "decay_12_cw_ged_dummy_ns_0",
    "decay_12_cw_ged_dummy_os_0",
    "l1_ged_dummy_os",
    "l2_ged_dummy_os",
    "l3_ged_dummy_os",
    "l4_ged_dummy_os",
    "l5_ged_dummy_os",
    "l6_ged_dummy_os",
    "l7_ged_dummy_os",
    "l8_ged_dummy_os",
    "l9_ged_dummy_os",
    "l10_ged_dummy_os",
    "l11_ged_dummy_os",
    "l12_ged_dummy_os",
    "q_1_1_l1_ged_dummy_sb",
    "q_1_1_l1_ged_dummy_ns",
    "q_1_1_l1_ged_dummy_os",
    "q_1_1_l2_ged_dummy_os",
    "q_1_1_l3_ged_dummy_os",
    "ln_bdist3",
    "ln_ttime",
    "ln_capdist",
    "ln_pop",
    "ln_dist_diamsec",
    "ln_dist_petroleum",
    "gcp_li_mer",
    "imr_mean",
    "mountains_mean",
    "urban_ih_li",
    "excluded_dummy_li",
    "agri_ih_li",
    "barren_ih_li",
    "forest_ih_li",
    "savanna_ih_li",
    "shrub_ih_li",
    "pasture_ih_li"]


features_acled_sb = [
    "decay_12_cw_acled_count_pr_0", 
    "q_1_1_l1_acled_count_pr", 
    "q_1_1_l2_acled_count_pr", 
    "q_1_1_l3_acled_count_pr", 
    "l1_acled_count_pr", 
    "l2_acled_count_pr", 
    "l3_acled_count_pr", 
    "l4_acled_count_pr", 
    "l5_acled_count_pr", 
    "l6_acled_count_pr", 
    "l7_acled_count_pr", 
    "l8_acled_count_pr", 
    "l9_acled_count_pr", 
    "l10_acled_count_pr", 
    "l11_acled_count_pr", 
    "l12_acled_count_pr", 
    "decay_12_cw_ged_dummy_sb_0", 
    "decay_12_cw_ged_dummy_ns_0", 
    "decay_12_cw_ged_dummy_os_0", 
    "l1_ged_dummy_sb", 
    "l2_ged_dummy_sb", 
    "l3_ged_dummy_sb", 
    "l4_ged_dummy_sb", 
    "l5_ged_dummy_sb", 
    "l6_ged_dummy_sb", 
    "l7_ged_dummy_sb", 
    "l8_ged_dummy_sb", 
    "l9_ged_dummy_sb", 
    "l10_ged_dummy_sb", 
    "l11_ged_dummy_sb", 
    "l12_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_os", 
    "q_1_1_l2_ged_dummy_sb", 
    "q_1_1_l3_ged_dummy_sb", 
    "ln_bdist3", 
    "ln_ttime", 
    "ln_capdist", 
    "ln_pop", 
    "ln_dist_diamsec", 
    "ln_dist_petroleum", 
    "gcp_li_mer", 
    "imr_mean", 
    "mountains_mean", 
    "urban_ih_li",  
    "excluded_dummy_li", 
    "agri_ih_li", 
    "barren_ih_li",  
    "forest_ih_li",  
    "savanna_ih_li",  
    "shrub_ih_li",  
    "pasture_ih_li"]

features_acled_ns = [
    "decay_12_cw_acled_count_pr_0", 
    "q_1_1_l1_acled_count_pr", 
    "q_1_1_l2_acled_count_pr", 
    "q_1_1_l3_acled_count_pr", 
    "l1_acled_count_pr", 
    "l2_acled_count_pr", 
    "l3_acled_count_pr", 
    "l4_acled_count_pr", 
    "l5_acled_count_pr", 
    "l6_acled_count_pr", 
    "l7_acled_count_pr", 
    "l8_acled_count_pr", 
    "l9_acled_count_pr", 
    "l10_acled_count_pr", 
    "l11_acled_count_pr", 
    "l12_acled_count_pr", 
    "decay_12_cw_ged_dummy_sb_0", 
    "decay_12_cw_ged_dummy_ns_0", 
    "decay_12_cw_ged_dummy_os_0", 
    "l1_ged_dummy_ns", 
    "l2_ged_dummy_ns", 
    "l3_ged_dummy_ns", 
    "l4_ged_dummy_ns", 
    "l5_ged_dummy_ns", 
    "l6_ged_dummy_ns", 
    "l7_ged_dummy_ns", 
    "l8_ged_dummy_ns", 
    "l9_ged_dummy_ns", 
    "l10_ged_dummy_ns", 
    "l11_ged_dummy_ns", 
    "l12_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_os", 
    "q_1_1_l2_ged_dummy_ns", 
    "q_1_1_l3_ged_dummy_ns", 
    "ln_bdist3", 
    "ln_ttime", 
    "ln_capdist", 
    "ln_pop", 
    "ln_dist_diamsec", 
    "ln_dist_petroleum", 
    "gcp_li_mer", 
    "imr_mean", 
    "mountains_mean", 
    "urban_ih_li",  
    "excluded_dummy_li", 
    "agri_ih_li", 
    "barren_ih_li",  
    "forest_ih_li",  
    "savanna_ih_li",  
    "shrub_ih_li",  
    "pasture_ih_li"]

features_acled_os = [
    "decay_12_cw_acled_count_pr_0", 
    "q_1_1_l1_acled_count_pr", 
    "q_1_1_l2_acled_count_pr", 
    "q_1_1_l3_acled_count_pr", 
    "l1_acled_count_pr", 
    "l2_acled_count_pr", 
    "l3_acled_count_pr", 
    "l4_acled_count_pr", 
    "l5_acled_count_pr", 
    "l6_acled_count_pr", 
    "l7_acled_count_pr", 
    "l8_acled_count_pr", 
    "l9_acled_count_pr", 
    "l10_acled_count_pr", 
    "l11_acled_count_pr", 
    "l12_acled_count_pr", 
    "decay_12_cw_ged_dummy_sb_0", 
    "decay_12_cw_ged_dummy_ns_0", 
    "decay_12_cw_ged_dummy_os_0", 
    "l1_ged_dummy_os", 
    "l2_ged_dummy_os", 
    "l3_ged_dummy_os", 
    "l4_ged_dummy_os", 
    "l5_ged_dummy_os", 
    "l6_ged_dummy_os", 
    "l7_ged_dummy_os", 
    "l8_ged_dummy_os", 
    "l9_ged_dummy_os", 
    "l10_ged_dummy_os", 
    "l11_ged_dummy_os", 
    "l12_ged_dummy_os", 
    "q_1_1_l1_ged_dummy_sb", 
    "q_1_1_l1_ged_dummy_ns", 
    "q_1_1_l1_ged_dummy_os", 
    "q_1_1_l2_ged_dummy_os", 
    "q_1_1_l3_ged_dummy_os", 
    "ln_bdist3", 
    "ln_ttime", 
    "ln_capdist", 
    "ln_pop", 
    "ln_dist_diamsec", 
    "ln_dist_petroleum", 
    "gcp_li_mer", 
    "imr_mean", 
    "mountains_mean", 
    "urban_ih_li",  
    "excluded_dummy_li", 
    "agri_ih_li", 
    "barren_ih_li",  
    "forest_ih_li",  
    "savanna_ih_li",  
    "shrub_ih_li",  
    "pasture_ih_li"]



logit_canon_full_calib_sb = {
    'name' : 'logit_canon_full_calib_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_canon_full_calib_ns = {
    'name' : 'logit_canon_full_calib_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_canon_full_calib_os = {
    'name' : 'logit_canon_full_calib_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_canon_full_test_sb = {
    'name' : 'logit_canon_full_test_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_canon_full_test_ns = {
    'name' : 'logit_canon_full_test_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_canon_full_test_os = {
    'name' : 'logit_canon_full_test_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_acled_full_calib_sb = {
    'name' : 'logit_acled_full_calib_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_acled_full_calib_ns = {
    'name' : 'logit_acled_full_calib_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_acled_full_calib_os = {
    'name' : 'logit_acled_full_calib_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_acled_full_test_sb = {
    'name' : 'logit_acled_full_test_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_acled_full_test_ns = {
    'name' : 'logit_acled_full_test_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_acled_full_test_os = {
    'name' : 'logit_acled_full_test_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_full,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_canon_ones_calib_sb = {
    'name' : 'logit_canon_ones_calib_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_canon_ones_calib_ns = {
    'name' : 'logit_canon_ones_calib_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_canon_ones_calib_os = {
    'name' : 'logit_canon_ones_calib_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_canon_ones_test_sb = {
    'name' : 'logit_canon_ones_test_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_canon_ones_test_ns = {
    'name' : 'logit_canon_ones_test_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_canon_ones_test_os = {
    'name' : 'logit_canon_ones_test_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_acled_ones_calib_sb = {
    'name' : 'logit_acled_ones_calib_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_acled_ones_calib_ns = {
    'name' : 'logit_acled_ones_calib_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_acled_ones_calib_os = {
    'name' : 'logit_acled_ones_calib_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

logit_acled_ones_test_sb = {
    'name' : 'logit_acled_ones_test_sb',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_acled_ones_test_ns = {
    'name' : 'logit_acled_ones_test_ns',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

logit_acled_ones_test_os = {
    'name' : 'logit_acled_ones_test_os',
    'estimator' : SMLogit(),
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}



rf_canon_ones_calib_sb = {
    'name' : 'rf_canon_ones_calib_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

rf_canon_ones_calib_ns = {
    'name' : 'rf_canon_ones_calib_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

rf_canon_ones_calib_os = {
    'name' : 'rf_canon_ones_calib_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

rf_canon_ones_test_sb = {
    'name' : 'rf_canon_ones_test_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_canon_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

rf_canon_ones_test_ns = {
    'name' : 'rf_canon_ones_test_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_canon_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

rf_canon_ones_test_os = {
    'name' : 'rf_canon_ones_test_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_canon_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_canon,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

rf_acled_ones_calib_sb = {
    'name' : 'rf_acled_ones_calib_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

rf_acled_ones_calib_ns = {
    'name' : 'rf_acled_ones_calib_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

rf_acled_ones_calib_os = {
    'name' : 'rf_acled_ones_calib_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_calib,
    'forecast_start' :  forecast_start_calib,
    'forecast_end' :  forecast_end_calib,
    'table' : table_input}

rf_acled_ones_test_sb = {
    'name' : 'rf_acled_ones_test_sb',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_sb',
    'features' : features_acled_sb,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

rf_acled_ones_test_ns = {
    'name' : 'rf_acled_ones_test_ns',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_ns',
    'features' : features_acled_ns,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}

rf_acled_ones_test_os = {
    'name' : 'rf_acled_ones_test_os',
    'estimator' : pipe_rf_500,
    'outcome' : 'ged_dummy_os',
    'features' : features_acled_os,
    'steps' : steps,
    'share_zeros_keep' : share_zeros_tenth,
    'share_ones_keep' : share_ones_full,
    'train_start' :  train_start_acled,
    'train_end' :  train_end_test,
    'forecast_start' :  forecast_start_test,
    'forecast_end' :  forecast_end_test,
    'table' : table_input}


