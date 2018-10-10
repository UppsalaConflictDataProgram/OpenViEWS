import utils
import times as t
import varsets as v
import transforms as tr
from loa import loas


# cm_canon_escalation = utils.make_models(
# name="cm_canon_escalation", loa="cm",
#                                         vars_lhs=v.outcomes_escalation,
#                                         vars_rhs_specifics=v.specific_lags_escalation_nospatial,
#                                         rhs_common=v.endog_ts_escalation + v.exog_cm_all,
#                                         stage=1,
#                                         transforms=tr.transforms_all)

# pgm_canon_esc_nospat = utils.make_models(
# name="pgm_canon_escalationnospat",
#                                          loa="pgm",
#                                          vars_lhs=v.outcomes_escalation,
#                                          vars_rhs_specifics=v.specific_lags_escalation_nospatial,
#                                          rhs_common=v.endog_ts_escalation + v.exog_pgm_all + v.exog_cm_all,
#                                          stage=1,
#                                          transforms=tr.transforms_all)

# pgm_canon_esc_spat = utils.make_models(
# name="pgm_canon_escalationspat",
#                                        loa="pgm",
#                                        vars_lhs=v.outcomes_escalation,
#                                        vars_rhs_specifics=v.specific_lags_escalation_nospatial,
#                                        rhs_common=v.endog_ts_escalation + v.exog_pgm_all + v.exog_cm_all,
#                                        stage=1,
#                                        transforms=tr.transforms_all)


pgm_acled_wcm = utils.make_models(
    name="pgm_acled_wcm", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all,
    rhs_common=v.endog_sts_all + v.exog_pgm_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_nocm = utils.make_models(
    name="pgm_acled_nocm", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all,
    rhs_common=v.endog_sts_all + v.exog_pgm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_canon_wcm = utils.make_models(
    name="pgm_canon_wcm", loa="pgm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged,
    rhs_common=v.endog_sts_ged + v.exog_pgm_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)
pgm_canon_nocm = utils.make_models(
    name="pgm_canon_nocm", loa="pgm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged,
    rhs_common=v.endog_sts_ged + v.exog_pgm_all,
    stage=1,
    transforms=tr.transforms_all)

cm_acled_base = utils.make_models(
    name="cm_acled_base", loa="cm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all_nospatial,
    rhs_common=v.endog_ts_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_base = utils.make_models(
    name="cm_canon_base", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged_nospatial,
    rhs_common=v.endog_ts_ged + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)


# THEMATIC PGM

pgm_acled_histonly = utils.make_models(
    name="pgm_acled_histonly", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all,
    rhs_common=v.endog_sts_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_canon_histonly = utils.make_models(
    name="pgm_canon_histonly", loa="pgm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged,
    rhs_common=v.endog_sts_ged,
    stage=1,
    transforms=tr.transforms_all)

pgm_sbonly_wcm = utils.make_models(
    name="pgm_sbonly_wcm", loa="pgm",
    vars_lhs=v.outcome_sb,
    vars_rhs_specifics=v.specific_lags_sb,
    rhs_common=v.endog_sts_sb + v.exog_pgm_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_nsonly_wcm = utils.make_models(
    name="pgm_nsonly_wcm", loa="pgm",
    vars_lhs=v.outcome_ns,
    vars_rhs_specifics=v.specific_lags_ns,
    rhs_common=v.endog_sts_ns + v.exog_pgm_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_osonly_wcm = utils.make_models(
    name="pgm_osonly_wcm", loa="pgm",
    vars_lhs=v.outcome_os,
    vars_rhs_specifics=v.specific_lags_os,
    rhs_common=v.endog_sts_os + v.exog_pgm_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_pronly_wcm = utils.make_models(
    name="pgm_pronly_wcm", loa="pgm",
    vars_lhs=v.outcome_pr,
    vars_rhs_specifics=v.specific_lags_pr,
    rhs_common=v.endog_sts_pr + v.exog_pgm_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_nat = utils.make_models(
    name="pgm_acled_nat", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_empty_4,
    rhs_common=v.exog_pgm_natural,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_soc = utils.make_models(
    name="pgm_acled_soc", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_empty_4,
    rhs_common=v.exog_pgm_social,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_socnat = utils.make_models(
    name="pgm_acled_socnat", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_empty_4,
    rhs_common=v.exog_pgm_social + v.exog_pgm_natural,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_sochist = utils.make_models(
    name="pgm_acled_sochist", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all,
    rhs_common=v.exog_pgm_social + v.endog_sts_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_nathist = utils.make_models(
    name="pgm_acled_nathist", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all,
    rhs_common=v.exog_pgm_natural + v.endog_sts_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_mean = utils.make_models(
    name="pgm_acled_mean", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.mean_outcome_all,
    rhs_common=[],
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meanhist = utils.make_models(
    name="pgm_acled_meanhist", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all_w_mean,
    rhs_common=v.endog_sts_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meannat = utils.make_models(
    name="pgm_acled_meannat", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.mean_outcome_all,
    rhs_common=v.exog_pgm_natural,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meansoc = utils.make_models(
    name="pgm_acled_meansoc", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.mean_outcome_all,
    rhs_common=v.exog_pgm_social,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meansocnat = utils.make_models(
    name="pgm_acled_meansocnat", loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.mean_outcome_all,
    rhs_common=v.exog_pgm_social + v.exog_pgm_natural,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meansocnathist = utils.make_models(
    name="pgm_acled_meansocnathist",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all_w_mean,
    rhs_common=v.exog_pgm_social + v.exog_pgm_natural + v.endog_sts_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meansocnathistcm = utils.make_models(
    name="pgm_acled_meansocnathistcm",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all_w_mean,
    rhs_common=v.exog_pgm_social + v.exog_pgm_natural +
    v.endog_sts_all + v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_cm = utils.make_models(
    name="pgm_acled_cm",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_empty_4,
    rhs_common=v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meancm = utils.make_models(
    name="pgm_acled_meancm",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.mean_outcome_all,
    rhs_common=v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meancmhist = utils.make_models(
    name="pgm_acled_meancmhist",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all_w_mean,
    rhs_common=v.exog_cm_all + v.endog_sts_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_protest = utils.make_models(
    name="pgm_acled_protest",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_protestonly,
    rhs_common=v.endog_sts_pr,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meanprotest = utils.make_models(
    name="pgm_acled_meanprotest",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_protestonly_w_mean,
    rhs_common=v.endog_sts_pr,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_cm = utils.make_models(
    name="pgm_acled_cm",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_empty_4,
    rhs_common=v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)

pgm_acled_meancm = utils.make_models(
    name="pgm_acled_meancm",
    loa="pgm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.mean_outcome_all,
    rhs_common=v.exog_cm_all,
    stage=1,
    transforms=tr.transforms_all)




# THEMATIC CM

cm_canon_mean = utils.make_models(
    name="cm_canon_mean", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.mean_outcome_ged,
    rhs_common=[],
    stage=1,
    transforms=tr.transforms_all)

cm_canon_demog = utils.make_models(
    name="cm_canon_demog", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_empty_3,
    rhs_common=v.exog_cm_demog,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_eco = utils.make_models(
    name="cm_canon_eco", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_empty_3,
    rhs_common=v.exog_cm_eco,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_hist = utils.make_models(
    name="cm_canon_hist", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged_nospatial,
    rhs_common=v.endog_ts_ged,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_inst = utils.make_models(
    name="cm_canon_inst", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_empty_3,
    rhs_common=v.exog_cm_inst,
    stage=1,
    transforms=tr.transforms_all)


cm_canon_meandemog = utils.make_models(
    name="cm_canon_meandemog", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.mean_outcome_ged,
    rhs_common=v.exog_cm_demog,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_meaneco = utils.make_models(
    name="cm_canon_meaneco", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.mean_outcome_ged,
    rhs_common=v.exog_cm_eco,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_meanhist = utils.make_models(
    name="cm_canon_meanhist", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged_nospatial_w_mean,
    rhs_common=v.endog_ts_ged,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_meaninst = utils.make_models(
    name="cm_canon_meaninst", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.mean_outcome_ged,
    rhs_common=v.exog_cm_inst,
    stage=1,
    transforms=tr.transforms_all)


cm_canon_meanhistdemog = utils.make_models(
    name="cm_canon_meanhistdemog", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged_nospatial_w_mean,
    rhs_common=v.exog_cm_demog,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_meanhisteco = utils.make_models(
    name="cm_canon_meanhisteco", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged_nospatial_w_mean,
    rhs_common=v.exog_cm_eco,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_meanhistinst = utils.make_models(
    name="cm_canon_meanhistinst", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_ged_nospatial_w_mean,
    rhs_common=v.exog_cm_inst,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_mndmgecohstnst = utils.make_models(
    name="cm_canon_mndmgecohstnst", loa="cm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_ged_nospatial_w_mean,
    rhs_common=v.exog_cm_demog+v.exog_cm_eco+v.exog_cm_inst,
    stage=1,
    transforms=tr.transforms_all)


cm_acled_mndmgecohstnst = utils.make_models(
    name="cm_acled_mndmgecohstnst", loa="cm",
    vars_lhs=v.outcomes_all,
    vars_rhs_specifics=v.specific_lags_all_nospatial_w_mean,
    rhs_common=v.exog_cm_demog+v.exog_cm_eco+v.exog_cm_inst,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_protest = utils.make_models(
    name="cm_canon_protest", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_protestonly_nospat,
    rhs_common=v.endog_ts_pr,
    stage=1,
    transforms=tr.transforms_all)

cm_canon_meanprotest = utils.make_models(
    name="cm_canon_meanprotest", loa="cm",
    vars_lhs=v.outcomes_ged,
    vars_rhs_specifics=v.specific_lags_protestonly_w_mean_nospat,
    rhs_common=v.endog_ts_pr,
    stage=1,
    transforms=tr.transforms_all)





# These contain one model per outcome
models_root = [
    cm_acled_base,
    cm_canon_mndmgecohstnst,
    cm_acled_mndmgecohstnst,
    cm_canon_base,
    cm_canon_demog,
    cm_canon_eco,
    cm_canon_hist,
    cm_canon_inst,
    cm_canon_meandemog,
    cm_canon_meaneco,
    cm_canon_mean,
    cm_canon_meanhistdemog,
    cm_canon_meanhisteco,
    cm_canon_meanhist,
    cm_canon_meanhistinst,
    cm_canon_meaninst,
    cm_canon_protest,
    cm_canon_meanprotest,
    pgm_acled_histonly,
    pgm_acled_mean,
    pgm_acled_meanhist,
    pgm_acled_meannat,
    pgm_acled_meansoc,
    pgm_acled_meansocnat,
    pgm_acled_meansocnathistcm,
    pgm_acled_meansocnathist,
    pgm_acled_nat,
    pgm_acled_nathist,
    pgm_acled_nocm,
    pgm_acled_soc,
    pgm_acled_sochist,
    pgm_acled_socnat,
    pgm_acled_wcm,
    pgm_canon_histonly,
    pgm_canon_nocm,
    pgm_canon_wcm,
    pgm_nsonly_wcm,
    pgm_osonly_wcm,
    pgm_pronly_wcm,
    pgm_sbonly_wcm,
    pgm_acled_cm,
    pgm_acled_meancm,
    pgm_acled_meancmhist,
    pgm_acled_protest,
    pgm_acled_meanprotest,
    pgm_acled_cm,
    pgm_acled_meancm,]

runtypes = ["eval", "fcast"]
periods = ["calib", "test"]
times = t.times_nested

for model_root in models_root:
    for model_root_var in model_root:
        models_root_var_times = utils.demux_times(model_root_var, runtypes,
                                                  periods, times)
        for model_root_var_times in models_root_var_times:
            utils.store_model(model_root_var_times, "./output/models/")
