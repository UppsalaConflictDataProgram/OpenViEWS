crosslevels = {
    "cl_ds_pgm_canon_nocm_RUNTYPE_PERIOD_OUTCOME": [
        "ds_pgm_canon_nocm_RUNTYPE_PERIOD_OUTCOME",
        "ds_cm_canon_base_RUNTYPE_PERIOD_OUTCOME"
    ],
    "cl_osa_pgm_acled_nocm_RUNTYPE_PERIOD_logit_fullsample_OUTCOME": [
        "osa_pgm_acled_nocm_RUNTYPE_PERIOD_logit_fullsample_OUTCOME",
        "osa_cm_acled_base_RUNTYPE_PERIOD_logit_fullsample_OUTCOME"
    ],
    "cl_osa_pgm_canon_nocm_RUNTYPE_PERIOD_rf_downsampled_OUTCOME": [
        "osa_pgm_canon_nocm_RUNTYPE_PERIOD_rf_downsampled_OUTCOME",
        "osa_cm_canon_base_RUNTYPE_PERIOD_rf_downsampled_OUTCOME"
    ],
    "cl_ds_pgm_acled_nocm_RUNTYPE_PERIOD_OUTCOME": [
        "ds_pgm_acled_nocm_RUNTYPE_PERIOD_OUTCOME",
        "ds_cm_acled_base_RUNTYPE_PERIOD_OUTCOME"
    ],
    "cl_osa_pgm_acled_nocm_RUNTYPE_PERIOD_rf_downsampled_OUTCOME": [
        "osa_pgm_acled_nocm_RUNTYPE_PERIOD_rf_downsampled_OUTCOME",
        "osa_cm_acled_base_RUNTYPE_PERIOD_rf_downsampled_OUTCOME"
    ],
    "cl_osa_pgm_canon_nocm_RUNTYPE_PERIOD_logit_fullsample_OUTCOME": [
        "osa_pgm_canon_nocm_RUNTYPE_PERIOD_logit_fullsample_OUTCOME",
        "osa_cm_canon_base_RUNTYPE_PERIOD_logit_fullsample_OUTCOME"
    ]
}

with open("crosslevels.json", 'w') as f:
    f.write(json.dumps(crosslevels, indent=4))