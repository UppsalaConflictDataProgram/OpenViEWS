# ViEWS changelog

## r.2018.10.01

* Set latest month of rolling data to 2018-08 (month_id=464).
* Groupvar-level means bug fixed now in OSA also, consider r.2018.09.02 OSA
  results that include the groupvar-level mean with great suspicion

### Added thematic CM models

* cm_canon_mean
* cm_canon_demog
* cm_canon_eco
* cm_canon_hist
* cm_canon_inst
* cm_canon_meandemog
* cm_canon_meaneco
* cm_canon_meanhist
* cm_canon_meaninst
* cm_canon_meanhistdemog
* cm_canon_meanhisteco
* cm_canon_meanhistinst
* cm_acled_meandemogecohistinst


## r.2018.09.02

* Set latest month of final data to 2017-12 (month_id=456),
    thereby moving the evaluation window one year ahead.

* Fixed bug in DS where groupvar-level means in certain models would
  include values from the "future" in that models perspective.

### Added thematic PGM models

* pgm_nsonly_wcm
* pgm_osonly_wcm
* pgm_pronly_wcm
* pgm_acled_nat
* pgm_acled_soc
* pgm_acled_socnat
* pgm_acled_sochist
* pgm_acled_nathist
* pgm_acled_mean
* pgm_acled_meanhist
* pgm_acled_meannat
* pgm_acled_meansoc
* pgm_acled_meansocnat
* pgm_acled_meansocnathist
* pgm_acled_meansocnathistcm

## r.2018.09.01

* Set latest month of rolling data to 2018-07 (month_id=463).

## r.2018.08.01

* Set latest month of rolling data to 2018-06 (month_id=462)

## r.2018.07.01

* Set latest month of rolling data to 2018-05 (month_id=461)
* Added One Step Ahead estimator output storage



