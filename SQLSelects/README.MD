These are sql statements for combining the imputed tables in the database. 
The naming convention is lhs_rhs_N.sql, 
so noimp_imp_5.sql is :
non-imputed left hand side, 
imputed right hand side, 
imputation number 5

The rhs variables are the three ged_dummy_sb, ged_dummy_ns, ged_dummy_os.

The guiding idea between inner and outer joins is to let the right hand side decide the scope of the data. 
imp_noimp uses outer joins, as the imputed lhs (from geoimputation.pgm) don't cover all the time we want (future).
noimp_imp uses inner joins, because the full non-imputed tables preflight.flight_pgm are only used here for lhs. 
An outer join here would give a bunch of values for the lhs with all rhs missing.