ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_bdbest_tot;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_conflict;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_prop_dominant;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_prop_excluded;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_prop_powerless;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_prop_discriminated;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_prop_irrelevant;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_lngdp200;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_lngdppercapita200;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_population200;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_oilunitrent;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_oilprodcost;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_oilprod;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_oilrent;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_polyarchy;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_api;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_mpi;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_libdem;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_liberal;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_partipdem;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_partip;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_delibdem;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xdl_delib;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_egaldem;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_egal;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_edcomp_thick;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_frassoc_thick;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_freexp_thick;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_freexp;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xme_altinf;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_suffr;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xel_frefair;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xcl_rol;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_jucon;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xlg_legcon;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_cspart;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xdd_dd;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xel_locelec;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xel_regelec;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xeg_eqprotec;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xeg_eqdr;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xcs_ccsi;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xps_party;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_gender;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_gencl;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_gencs;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_genpp;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_elecreg;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xex_elecreg;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xlg_elecreg;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xel_elecparl;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xlg_leginter;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2xel_elecpres;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_hosinter;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_corr;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_pubcorr;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_execorr;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_lgdivparctrl;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_feduni;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_civlib;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_clpriv;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_clpol;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS v2x_clphy;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_electoral;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_liberal;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_participatory;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_democracy;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_demo;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_auto;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_semi;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_regime3c;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_fmnyrsschool2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_fshlowersec2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_fshuppersec2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_mmnyrsschool2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_mnyrsschool2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_mshlowersec2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_mshnoedu2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_mshuppersec2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_low_sec_female_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_low_sec_male_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_post_sec_female_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_post_sec_male_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_prim_female_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_prim_male_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_upp_sec_female_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_compl_upp_sec_male_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_f_lowsec_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_f_uppsec_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_m_lowsec_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_m_uppsec_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_incompl_prim_female_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_uppsec_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_totshlowersec2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_totshnoedu2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_totshuppersec2024;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_ymhep;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_gdp_ppp_iiasa;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_gdp_ppp_oecd;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_gdppercap_iiasa;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_gdppercap_oecd;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_urban_share_iiasa;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_dep_ratio;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_non_workagepoptot;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_f_pop;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_lowsec_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_m_pop;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_noedu_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_pop;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_pop_15_19;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_pop_20_24;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_pop_above_65;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_tot_pop_below_15;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_workagepoptot;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_youth_bulges;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_durable;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_polity2;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_timesinceregimechange2;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_timesincepreindepwar;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_timeindep;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_indepyear;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_ltsc0;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_ltsc1;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS ssp2_ltsc2;

ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_durable;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_polity2;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_timesinceregimechange2;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_timesincepreindepwar;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_timeindep;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_indepyear;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_ltsc0;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_ltsc1;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS fvp_ltsc2;

ALTER TABLE staging.country_year DROP COLUMN IF EXISTS lnpop200;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS TimeSinceRegimeChange;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS grGDPcap_oilrent;
ALTER TABLE staging.country_year DROP COLUMN IF EXISTS grGDPcap_nonoilrent;


ALTER TABLE staging.country_year ADD COLUMN fvp_bdbest_tot FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_conflict FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_prop_dominant FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_prop_excluded FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_prop_powerless FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_prop_discriminated FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_prop_irrelevant FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_lngdp200 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_lngdppercapita200 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_population200 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_oilunitrent FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_oilprodcost FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_oilprod FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_oilrent FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_polyarchy FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_api FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_mpi FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_libdem FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_liberal FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_partipdem FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_partip FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_delibdem FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xdl_delib FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_egaldem FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_egal FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_edcomp_thick FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_frassoc_thick FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_freexp_thick FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_freexp FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xme_altinf FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_suffr FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xel_frefair FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xcl_rol FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_jucon FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xlg_legcon FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_cspart FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xdd_dd FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xel_locelec FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xel_regelec FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xeg_eqprotec FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xeg_eqdr FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xcs_ccsi FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xps_party FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_gender FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_gencl FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_gencs FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_genpp FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_elecreg FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xex_elecreg FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xlg_elecreg FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xel_elecparl FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xlg_leginter FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2xel_elecpres FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_hosinter FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_corr FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_pubcorr FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_execorr FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_lgdivparctrl FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_feduni FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_civlib FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_clpriv FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_clpol FLOAT;
ALTER TABLE staging.country_year ADD COLUMN v2x_clphy FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_electoral FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_liberal FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_participatory FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_democracy FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_demo FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_auto FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_semi FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_regime3c FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_fmnyrsschool2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_fshlowersec2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_fshuppersec2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_mmnyrsschool2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_mnyrsschool2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_mshlowersec2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_mshnoedu2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_mshuppersec2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_low_sec_female_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_low_sec_male_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_post_sec_female_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_post_sec_male_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_prim_female_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_prim_male_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_upp_sec_female_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_compl_upp_sec_male_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_f_lowsec_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_f_uppsec_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_m_lowsec_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_m_uppsec_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_incompl_prim_female_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_uppsec_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_totshlowersec2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_totshnoedu2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_totshuppersec2024 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_ymhep FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_gdp_ppp_iiasa FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_gdp_ppp_oecd FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_gdppercap_iiasa FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_gdppercap_oecd FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_urban_share_iiasa FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_dep_ratio FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_non_workagepoptot FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_f_pop FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_lowsec_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_m_pop FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_noedu_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_pop FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_pop_15_19 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_pop_20_24 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_pop_above_65 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_tot_pop_below_15 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_workagepoptot FLOAT;
ALTER TABLE staging.country_year ADD COLUMN ssp2_youth_bulges FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_durable FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_polity2 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_timesinceregimechange2 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_timesincepreindepwar FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_timeindep FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_indepyear FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_ltsc0 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_ltsc1 FLOAT;
ALTER TABLE staging.country_year ADD COLUMN fvp_ltsc2 FLOAT;

ALTER TABLE staging.country_year ADD COLUMN fvp_lnpop200;
ALTER TABLE staging.country_year ADD COLUMN fvp_timesinceregimechange;
ALTER TABLE staging.country_year ADD COLUMN fvp_grgdpcap_oilrent;
ALTER TABLE staging.country_year ADD COLUMN fvp_grgdpcap_nonoilrent;

WITH a AS
(
    SELECT
      staging.country_year.id,
      staging.country_year.year_id,
      staging.country_year.country_id,
      staging.country.gwcode
    FROM staging.country_year
      LEFT JOIN staging.country
        ON staging.country_year.country_id = staging.country.id
),
b AS (
      SELECT
lnpop200 AS fvp_lnpop200,
TimeSinceRegimeChange AS fvp_timesinceregimechange,
grGDPcap_oilrent AS fvp_grgdpcap_oilrent,
grGDPcap_nonoilrent AS fvp_grgdpcap_nonoilrent,
bdbest_tot AS fvp_bdbest_tot,
conflict AS fvp_conflict,
prop_dominant AS fvp_prop_dominant,
prop_excluded AS fvp_prop_excluded,
prop_powerless AS fvp_prop_powerless,
prop_discriminated AS fvp_prop_discriminated,
prop_irrelevant AS fvp_prop_irrelevant,
lngdp200 AS fvp_lngdp200,
lngdppercapita200 AS fvp_lngdppercapita200,
population200 AS fvp_population200,
oilunitrent AS fvp_oilunitrent,
oilprodcost AS fvp_oilprodcost,
oilprod AS fvp_oilprod,
oilrent AS fvp_oilrent,
v2x_polyarchy,
v2x_api,
v2x_mpi,
v2x_libdem,
v2x_liberal,
v2x_partipdem,
v2x_partip,
v2x_delibdem,
v2xdl_delib,
v2x_egaldem,
v2x_egal,
v2x_edcomp_thick,
v2x_frassoc_thick,
v2x_freexp_thick,
v2x_freexp,
v2xme_altinf,
v2x_suffr,
v2xel_frefair,
v2xcl_rol,
v2x_jucon,
v2xlg_legcon,
v2x_cspart,
v2xdd_dd,
v2xel_locelec,
v2xel_regelec,
v2xeg_eqprotec,
v2xeg_eqdr,
v2xcs_ccsi,
v2xps_party,
v2x_gender,
v2x_gencl,
v2x_gencs,
v2x_genpp,
v2x_elecreg,
v2xex_elecreg,
v2xlg_elecreg,
v2xel_elecparl,
v2xlg_leginter,
v2xel_elecpres,
v2x_hosinter,
v2x_corr,
v2x_pubcorr,
v2x_execorr,
v2x_lgdivparctrl,
v2x_feduni,
v2x_civlib,
v2x_clpriv,
v2x_clpol,
v2x_clphy,
fvp_electoral,
fvp_liberal,
fvp_participatory,
fvp_democracy,
fvp_demo,
fvp_auto,
fvp_semi,
fvp_regime3c,
fmnyrsschool2024ssp2 AS ssp2_fmnyrsschool2024,
fshlowersec2024ssp2 AS ssp2_fshlowersec2024,
fshuppersec2024ssp2 AS ssp2_fshuppersec2024,
mmnyrsschool2024ssp2 AS ssp2_mmnyrsschool2024,
mnyrsschool2024ssp2 AS ssp2_mnyrsschool2024,
mshlowersec2024ssp2 AS ssp2_mshlowersec2024,
mshnoedu2024ssp2 AS ssp2_mshnoedu2024,
mshuppersec2024ssp2 AS ssp2_mshuppersec2024,
ssp2compl_low_sec_female_20_24 AS ssp2_compl_low_sec_female_20_24,
ssp2compl_low_sec_male_20_24 AS ssp2_compl_low_sec_male_20_24,
ssp2compl_post_sec_female_20_24 AS ssp2_compl_post_sec_female_20_24,
ssp2compl_post_sec_male_20_24 AS ssp2_compl_post_sec_male_20_24,
ssp2compl_prim_female_20_24 AS ssp2_compl_prim_female_20_24,
ssp2compl_prim_male_20_24 AS ssp2_compl_prim_male_20_24,
ssp2compl_upp_sec_female_20_24 AS ssp2_compl_upp_sec_female_20_24,
ssp2compl_upp_sec_male_20_24 AS ssp2_compl_upp_sec_male_20_24,
ssp2f_lowsec_20_24 AS ssp2_f_lowsec_20_24,
ssp2f_uppsec_20_24 AS ssp2_f_uppsec_20_24,
ssp2m_lowsec_20_24 AS ssp2_m_lowsec_20_24,
ssp2m_uppsec_20_24 AS ssp2_m_uppsec_20_24,
ssp2incompl_prim_female_20_24 AS ssp2_incompl_prim_female_20_24,
ssp2tot_uppsec_20_24 AS ssp2_tot_uppsec_20_24,
totshlowersec2024ssp2 AS ssp2_totshlowersec2024,
totshnoedu2024ssp2 AS ssp2_totshnoedu2024,
totshuppersec2024ssp2 AS ssp2_totshuppersec2024,
ymhepssp2 AS ssp2_ymhep,
ssp2_gdp_ppp_iiasa,
ssp2_gdp_ppp_oecd,
ssp2_gdppercap_iiasa,
ssp2_gdppercap_oecd,
ssp2_urban_share_iiasa,
ssp2dep_ratio AS ssp2_dep_ratio,
ssp2non_workagepoptot AS ssp2_non_workagepoptot,
ssp2tot_f_pop AS ssp2_tot_f_pop,
ssp2tot_lowsec_20_24 AS ssp2_tot_lowsec_20_24,
ssp2tot_m_pop AS ssp2_tot_m_pop,
ssp2tot_noedu_20_24 AS ssp2_tot_noedu_20_24,
ssp2tot_pop AS ssp2_tot_pop,
ssp2tot_pop_15_19 AS ssp2_tot_pop_15_19,
ssp2tot_pop_20_24 AS ssp2_tot_pop_20_24,
ssp2tot_pop_above_65 AS ssp2_tot_pop_above_65,
ssp2tot_pop_below_15 AS ssp2_tot_pop_below_15,
ssp2workagepoptot AS ssp2_workagepoptot,
ssp2youth_bulges AS ssp2_youth_bulges,
durable AS fvp_durable,
polity2 AS fvp_polity2,
timesinceregimechange2 AS fvp_timesinceregimechange2,
timesincepreindepwar AS fvp_timesincepreindepwar,
timeindep AS fvp_timeindep,
indepyear AS fvp_indepyear,
ltsc0 AS fvp_ltsc0,
ltsc1 AS fvp_ltsc1,
ltsc2 AS fvp_ltsc2,
gwno,
year,
a.country_id,
a.year_id
      
FROM dataprep.fovp, a
WHERE
(a.year_id = dataprep.fovp.year AND a.gwcode = dataprep.fovp.gwno)
)
UPDATE staging.country_year SET

fvp_lnpop200 = b.fvp_lnpop200
fvp_timesinceregimechange = b.fvp_timesinceregimechange
fvp_grgdpcap_oilrent = b.fvp_grgdpcap_oilrent
fvp_grgdpcap_nonoilrent = b.fvp_grgdpcap_nonoilrent

fvp_bdbest_tot  = b.fvp_bdbest_tot,
fvp_conflict  = b.fvp_conflict,
fvp_prop_dominant  = b.fvp_prop_dominant,
fvp_prop_excluded  = b.fvp_prop_excluded,
fvp_prop_powerless  = b.fvp_prop_powerless,
fvp_prop_discriminated  = b.fvp_prop_discriminated,
fvp_prop_irrelevant  = b.fvp_prop_irrelevant,
fvp_lngdp200  = b.fvp_lngdp200,
fvp_lngdppercapita200  = b.fvp_lngdppercapita200,
fvp_population200  = b.fvp_population200,
fvp_oilunitrent  = b.fvp_oilunitrent,
fvp_oilprodcost  = b.fvp_oilprodcost,
fvp_oilprod  = b.fvp_oilprod,
fvp_oilrent  = b.fvp_oilrent,
v2x_polyarchy  = b.v2x_polyarchy,
v2x_api  = b.v2x_api,
v2x_mpi  = b.v2x_mpi,
v2x_libdem  = b.v2x_libdem,
v2x_liberal  = b.v2x_liberal,
v2x_partipdem  = b.v2x_partipdem,
v2x_partip  = b.v2x_partip,
v2x_delibdem  = b.v2x_delibdem,
v2xdl_delib  = b.v2xdl_delib,
v2x_egaldem  = b.v2x_egaldem,
v2x_egal  = b.v2x_egal,
v2x_edcomp_thick  = b.v2x_edcomp_thick,
v2x_frassoc_thick  = b.v2x_frassoc_thick,
v2x_freexp_thick  = b.v2x_freexp_thick,
v2x_freexp  = b.v2x_freexp,
v2xme_altinf  = b.v2xme_altinf,
v2x_suffr  = b.v2x_suffr,
v2xel_frefair  = b.v2xel_frefair,
v2xcl_rol  = b.v2xcl_rol,
v2x_jucon  = b.v2x_jucon,
v2xlg_legcon  = b.v2xlg_legcon,
v2x_cspart  = b.v2x_cspart,
v2xdd_dd  = b.v2xdd_dd,
v2xel_locelec  = b.v2xel_locelec,
v2xel_regelec  = b.v2xel_regelec,
v2xeg_eqprotec  = b.v2xeg_eqprotec,
v2xeg_eqdr  = b.v2xeg_eqdr,
v2xcs_ccsi  = b.v2xcs_ccsi,
v2xps_party  = b.v2xps_party,
v2x_gender  = b.v2x_gender,
v2x_gencl  = b.v2x_gencl,
v2x_gencs  = b.v2x_gencs,
v2x_genpp  = b.v2x_genpp,
v2x_elecreg  = b.v2x_elecreg,
v2xex_elecreg  = b.v2xex_elecreg,
v2xlg_elecreg  = b.v2xlg_elecreg,
v2xel_elecparl  = b.v2xel_elecparl,
v2xlg_leginter  = b.v2xlg_leginter,
v2xel_elecpres  = b.v2xel_elecpres,
v2x_hosinter  = b.v2x_hosinter,
v2x_corr  = b.v2x_corr,
v2x_pubcorr  = b.v2x_pubcorr,
v2x_execorr  = b.v2x_execorr,
v2x_lgdivparctrl  = b.v2x_lgdivparctrl,
v2x_feduni  = b.v2x_feduni,
v2x_civlib  = b.v2x_civlib,
v2x_clpriv  = b.v2x_clpriv,
v2x_clpol  = b.v2x_clpol,
v2x_clphy  = b.v2x_clphy,
fvp_electoral  = b.fvp_electoral,
fvp_liberal  = b.fvp_liberal,
fvp_participatory  = b.fvp_participatory,
fvp_democracy  = b.fvp_democracy,
fvp_demo  = b.fvp_demo,
fvp_auto  = b.fvp_auto,
fvp_semi  = b.fvp_semi,
fvp_regime3c  = b.fvp_regime3c,
ssp2_fmnyrsschool2024  = b.ssp2_fmnyrsschool2024,
ssp2_fshlowersec2024  = b.ssp2_fshlowersec2024,
ssp2_fshuppersec2024  = b.ssp2_fshuppersec2024,
ssp2_mmnyrsschool2024  = b.ssp2_mmnyrsschool2024,
ssp2_mnyrsschool2024  = b.ssp2_mnyrsschool2024,
ssp2_mshlowersec2024  = b.ssp2_mshlowersec2024,
ssp2_mshnoedu2024  = b.ssp2_mshnoedu2024,
ssp2_mshuppersec2024  = b.ssp2_mshuppersec2024,
ssp2_compl_low_sec_female_20_24  = b.ssp2_compl_low_sec_female_20_24,
ssp2_compl_low_sec_male_20_24  = b.ssp2_compl_low_sec_male_20_24,
ssp2_compl_post_sec_female_20_24  = b.ssp2_compl_post_sec_female_20_24,
ssp2_compl_post_sec_male_20_24  = b.ssp2_compl_post_sec_male_20_24,
ssp2_compl_prim_female_20_24  = b.ssp2_compl_prim_female_20_24,
ssp2_compl_prim_male_20_24  = b.ssp2_compl_prim_male_20_24,
ssp2_compl_upp_sec_female_20_24  = b.ssp2_compl_upp_sec_female_20_24,
ssp2_compl_upp_sec_male_20_24  = b.ssp2_compl_upp_sec_male_20_24,
ssp2_f_lowsec_20_24  = b.ssp2_f_lowsec_20_24,
ssp2_f_uppsec_20_24  = b.ssp2_f_uppsec_20_24,
ssp2_m_lowsec_20_24  = b.ssp2_m_lowsec_20_24,
ssp2_m_uppsec_20_24  = b.ssp2_m_uppsec_20_24,
ssp2_incompl_prim_female_20_24  = b.ssp2_incompl_prim_female_20_24,
ssp2_tot_uppsec_20_24  = b.ssp2_tot_uppsec_20_24,
ssp2_totshlowersec2024  = b.ssp2_totshlowersec2024,
ssp2_totshnoedu2024  = b.ssp2_totshnoedu2024,
ssp2_totshuppersec2024  = b.ssp2_totshuppersec2024,
ssp2_ymhep  = b.ssp2_ymhep,
ssp2_gdp_ppp_iiasa  = b.ssp2_gdp_ppp_iiasa,
ssp2_gdp_ppp_oecd  = b.ssp2_gdp_ppp_oecd,
ssp2_gdppercap_iiasa  = b.ssp2_gdppercap_iiasa,
ssp2_gdppercap_oecd  = b.ssp2_gdppercap_oecd,
ssp2_urban_share_iiasa  = b.ssp2_urban_share_iiasa,
ssp2_dep_ratio  = b.ssp2_dep_ratio,
ssp2_non_workagepoptot  = b.ssp2_non_workagepoptot,
ssp2_tot_f_pop  = b.ssp2_tot_f_pop,
ssp2_tot_lowsec_20_24  = b.ssp2_tot_lowsec_20_24,
ssp2_tot_m_pop  = b.ssp2_tot_m_pop,
ssp2_tot_noedu_20_24  = b.ssp2_tot_noedu_20_24,
ssp2_tot_pop  = b.ssp2_tot_pop,
ssp2_tot_pop_15_19  = b.ssp2_tot_pop_15_19,
ssp2_tot_pop_20_24  = b.ssp2_tot_pop_20_24,
ssp2_tot_pop_above_65  = b.ssp2_tot_pop_above_65,
ssp2_tot_pop_below_15  = b.ssp2_tot_pop_below_15,
ssp2_workagepoptot  = b.ssp2_workagepoptot,
ssp2_youth_bulges  = b.ssp2_youth_bulges,
fvp_durable  = b.fvp_durable,
fvp_polity2  = b.fvp_polity2,
fvp_timesinceregimechange2  = b.fvp_timesinceregimechange2,
fvp_timesincepreindepwar  = b.fvp_timesincepreindepwar,
fvp_timeindep  = b.fvp_timeindep,
fvp_indepyear  = b.fvp_indepyear,
fvp_ltsc0  = b.fvp_ltsc0,
fvp_ltsc1  = b.fvp_ltsc1,
fvp_ltsc2  = b.fvp_ltsc2

FROM b
WHERE b.country_id = staging.country_year.country_id
AND b.year_id = staging.country_year.year_id;




