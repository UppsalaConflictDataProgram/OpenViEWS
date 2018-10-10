#Geoimputation Evaluation
This dir contains the scripts used to make the dynasim runs for geoimputation 
evaluation.

Three runs will be made

* geoimp
* noimp
* naive

* All runs will have pgm_imp_1 as RHS
* geoimp will have 5 input datasets with outcome from geoimputation.pgm 1-5
* noimp will have 1 input dataset with outcome from preflight.flight_pgm
* naive will have 1 input dataset with ooutcome ged_dummy_naive_sb from 
preflight.flight_pgm


* STORE TRANSFORMATIONS FOR EACH DATASET