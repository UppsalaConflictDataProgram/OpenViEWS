# Script to impute missing variables from the FVP masterdata dataset

library("Amelia")
library("foreign")
library("methods")
library("parallel")

# Get data
df.full <- read.csv("MasterData.csv", header=T, sep=",")

# Select which variables to keep
vars.1960.2016 <- df.full[, (colnames(df.full) %in% 
                                 c("gwno",
                                   "year",
                                   "independence",
                                   "polity",
                                   "durable",
                                   "bdbest_tot",
                                   "conflict4",
                                   "TimeSincePreIndepWar",
                                   "conflict",
                                   "conflict0",
                                   "conflict1",
                                   "conflict2",
                                   "timeinstatus",
                                   "timeindep",
                                   "PKOs",
                                   "PKOmandate",
                                   "PKObudget",
                                   "PKOprotection",
                                   "PKOprevious",
                                   "YMHEPSSP1",
                                   "YMHEPSSP2",
                                   "YMHEPSSP3",
                                   "YMHEPSSP4",
                                   "YMHEPSSP5",
                                   "v2x_polyarchy",
                                   "v2x_liberal",
                                   "v2x_partip",
                                   "v2x_egal",
                                   "v2x_delib",
                                   "v2x_elecoff",
                                   "v2xel_frefair",
                                   "v2x_freexp_thick",
                                   "v2x_frassoc_thick",
                                   "v2x_suffr",
                                   "v2xcl_rol",
                                   "v2x_jucon",
                                   "v2xlg_legcon",
                                   "v2x_cspart",
                                   "v2xdd_dd",
                                   "locregelec",
                                   "FVP_electoral",
                                   "FVP_liberal",
                                   "FVP_participatory",
                                   "FVP_democracy",
                                   "FVP_demo",
                                   "FVP_semi",
                                   "FVP_auto",
                                   "FVP_regime3c",
                                   "regimechange",
                                   "TimeSinceRegimeChange",
                                   "lTimeSinceRegimeChange",
                                   "lntsrc",
                                   "Ross13_oil_production",
                                   "Ross13_oil_price",
                                   "Ross13_oil_value",
                                   "Ross13_net_oil_exports_valuePOP",
                                   "BX_KLT_DINV_WD_GD_ZS",
                                   "DT_ODA_ALLD_CD",
                                   "DT_ODA_ALLD_KD",
                                   "NE_EXP_GNFS_ZS",
                                   "NE_TRD_GNFS_ZS",
                                   "NV_AGR_TOTL_ZS",
                                   "NV_IND_MANF_ZS",
                                   "NV_IND_TOTL_ZS",
                                   "NV_SRV_TETC_ZS",
                                   "NY_GDP_DEFL_KD_ZG",
                                   "NY_GDP_DEFL_ZS",
                                   "NY_GDP_MKTP_CD",
                                   "NY_GDP_MKTP_KD",
                                   "NY_GDP_MKTP_PP_KD",
                                   "NY_GDP_PCAP_CD",
                                   "NY_GDP_PCAP_KD",
                                   "NY_GDP_PCAP_PP_KD",
                                   "SE_ADT_1524_LT_FE_ZS",
                                   "SE_ADT_1524_LT_FM_ZS",
                                   "SE_PRM_NENR",
                                   "SE_PRM_NENR_FE",
                                   "SE_PRM_NENR_MA",
                                   "SE_SEC_NENR",
                                   "SE_SEC_NENR_FE",
                                   "SE_SEC_NENR_MA",
                                   "SL_UEM_TOTL_ZS",
                                   "SP_DYN_IMRT_IN",
                                   "SP_DYN_TFRT_IN",
                                   "SP_POP_0014_TO_ZS",
                                   "SP_POP_DPND",
                                   "SP_POP_TOTL",
                                   "TX_VAL_FUEL_ZS_UN",
                                   "prop_dominant",
                                   "prop_excluded",
                                   "prop_powerless",
                                   "prop_discriminated",
                                   "prop_irrelevant",
                                   "prop_senpart",
                                   "prop_junpart",
                                   "prop_selfexclusion",
                                   "coup1",
                                   "coup2",
                                   "coup3",
                                   "coup4",
                                   "SSP1_GDP_PPP_OECD",
                                   "SSP2_GDP_PPP_OECD",
                                   "SSP3_GDP_PPP_OECD",
                                   "SSP4_GDP_PPP_OECD",
                                   "SSP5_GDP_PPP_OECD",
                                   "SSP1_GDP_PPP_IIASA",
                                   "SSP2_GDP_PPP_IIASA",
                                   "SSP3_GDP_PPP_IIASA",
                                   "SSP4_GDP_PPP_IIASA",
                                   "SSP5_GDP_PPP_IIASA",
                                   "SSP1_Pop_OECD",
                                   "SSP2_Pop_OECD",
                                   "SSP3_Pop_OECD",
                                   "SSP4_Pop_OECD",
                                   "SSP5_Pop_OECD",
                                   "SSP1_Pop_IIASA",
                                   "SSP2_Pop_IIASA",
                                   "SSP3_Pop_IIASA",
                                   "SSP4_Pop_IIASA",
                                   "SSP5_Pop_IIASA",
                                   "SSP1_Urban_Share_IIASA",
                                   "SSP2_Urban_Share_IIASA",
                                   "SSP3_Urban_Share_IIASA",
                                   "SSP4_Urban_Share_IIASA",
                                   "SSP5_Urban_Share_IIASA",
                                   "SSP1_YMHEP",
                                   "SSP2_YMHEP",
                                   "SSP3_YMHEP",
                                   "SSP4_YMHEP",
                                   "SSP5_YMHEP",
                                   "SSP1_GDPperCap_OECD",
                                   "SSP2_GDPperCap_OECD",
                                   "SSP3_GDPperCap_OECD",
                                   "SSP4_GDPperCap_OECD",
                                   "SSP5_GDPperCap_OECD",
                                   "SSP1_GDPperCap_IIASA",
                                   "SSP2_GDPperCap_IIASA",
                                   "SSP3_GDPperCap_IIASA",
                                   "SSP4_GDPperCap_IIASA",
                                   "SSP5_GDPperCap_IIASA",
                                   "lnGDP200",
                                   "lnGDPPerCapita200",
                                   "Population200",
                                   "lnpop200",
                                   "Oilrent",
                                   "TotOilrent",
                                   "OilUnitRent",
                                   "OilProdCost"))]

# Create subsets of FVP data that are to be imputed. One 1900-1959, 
# another 1960-2016. 
# Only for a subset of the variables for 00-59  
vars.1900.1959 <- vars.1960.2016[, (colnames(vars.1960.2016) %in% 
                                    c( "gwno",
                                       "year",
                                       "timeinstatus",
                                       "timeindep",
                                       "independence",
                                       "v2x_polyarchy",
                                       "v2x_liberal",
                                       "v2x_partip",
                                       "v2x_egal",
                                       "v2x_delib",
                                       "v2x_elecoff",
                                       "v2xel_frefair",
                                       "v2x_freexp_thick",
                                       "v2x_frassoc_thick",
                                       "v2x_suffr",
                                       "v2xcl_rol",
                                       "v2x_jucon",
                                       "v2xlg_legcon",
                                       "v2x_cspart",
                                       "v2xdd_dd",
                                       "locregelec",
                                       "FVP_electoral",
                                       "FVP_liberal",
                                       "FVP_participatory",
                                       "FVP_democracy",
                                       "FVP_demo",
                                       "FVP_semi",
                                       "FVP_auto",
                                       "FVP_regime3c",
                                       "regimechange",
                                       "TimeSinceRegimeChange",
                                       "lTimeSinceRegimeChange",
                                       "lntsrc",
                                       "Ross13_oil_production",
                                       "Ross13_oil_price",
                                       "Ross13_oil_value",
                                       "lnGDP200",
                                       "lnGDPPerCapita200",
                                       "Population200",
                                       "lnpop200"))]

# Early subset for impution
df.1900.1959 <- subset(vars.1900.1959, year >= 1900 & year <=1959)

#Later subset for impution
df.1960.2016 <- subset(vars.1960.2016, year >= 1960 & year <=2016)

################### Start with first subset ######################
summary(df.1900.1959)

# Specify nariable numbers
varnr <- c(3:39)
varnr

# Fetch upper and lower boundaries for each variable 
lower <- c()
upper <- c()
for (i in 1:length(df.1900.1959)) {
  print(i)
  lower <- c(lower, min(df.1900.1959[,i], na.rm=T))    
  upper <- c(upper, max(df.1900.1959[,i], na.rm=T))    
}

lower <- lower[varnr]
upper <- upper[varnr]

bds <- matrix(cbind(varnr,lower,upper),37)
bds

#Start
date.start <- Sys.time()

Imputed <- amelia(df.1900.1959, m = 10, ts = "year", cs = "gwno",
                  p2s=2, polytime = 2, intercs = TRUE, 
                  empri = .1*nrow(df.1900.1959),
                  bounds = bds, max.resample = 1000, 
                  noms = c( "FVP_demo", "FVP_semi", "FVP_auto", 
                            "FVP_regime3c", "regimechange"),
                  parallel="multicore", ncpus=10)

print("Impute finished")

#End
date.end <- Sys.time()

#Saving the imputed data sets in .dta format
write.amelia(obj=Imputed,
             file.stem = "fvp_imp_1900_1959", format = "dta")

print("Saved dataset")

save.image(file = "fvp_imp_1900_1959.RData")

print("Saved R image")

#Total time of imputation
date.end - date.start

################### Second subset ######################
summary(df.1960.2016)

# Specify nariable numbers
varnr <- c(4:146)
varnr

# Fetch upper and lower boundaries for each variable 
lower <- c()
upper <- c()
for (i in 1:length(df.1960.2016)) {
  print(i)
  lower <- c(lower, min(df.1960.2016[,i], na.rm=T))    
  upper <- c(upper, max(df.1960.2016[,i], na.rm=T))    
}

lower <- lower[varnr]
upper <- upper[varnr]

bds <- matrix(cbind(varnr,lower,upper),143)
bds

#Start
date.start <- Sys.time()

Imputed <- amelia(df.1960.2016, m = 10, ts = "year", cs = "gwno",
                  p2s=2, polytime = 2, 
                  intercs = TRUE, empri = .1*nrow(df.1960.2016),
                  bounds = bds, max.resample = 1000, 
                  noms = c(    "conflict", "conflict0", "conflict1",
                               "conflict2", "conflict4", 
                               "PKOprotection", "PKOprevious", "PKOs", 
                               "PKOmandate", 
                               "coup1", "coup2", "coup3", "coup4", 
                               "FVP_demo", "FVP_semi", "FVP_auto", 
                               "FVP_regime3c", "regimechange"),
                  parallel="multicore", ncpus=2)

print("Impute finished")

#End
date.end <- Sys.time()

#Saving the imputed data sets in .dta format
write.amelia(obj=Imputed,
             file.stem = "fvp_imp_1960_2016", format = "dta")

print("Saved dataset")

save.image(file = "fvp_imp_1960_2016.RData")

print("Saved R image")

#Total time of imputation
date.end - date.start
