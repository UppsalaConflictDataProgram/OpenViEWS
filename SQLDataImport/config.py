# This is the import pipeline configuration file

#What DB do you want updated?
#Only one DB at a time!
db = 'postgresql://VIEWSADMIN@VIEWSHOST:5432/views'

#
#What do you want updated?
#All at once works perfectly fine.
#Set do_ged to True if GED is to be updated and False if not
#Set do_acled to True if ACLED is to be updated as well
do_ged = True
do_acled = True

#Set preflight_when_done to True if you want the data both STAGED and PREFLIGHTED
#WARNING: Make 100% sure that the branch you are running this from is MASTER
#WARNING: Make 100% sure that you have a current version checked out locally.
#WARNING: This DOES NOT check out in real time. This RUNS on the checked out branch.
preflight_when_done=True

#Do you want the validate routines to check the load at the end?
validate_load=True

# You will need to specify a UCDP GED API version for the update
# The API must have 12 months of data preceding the startmonth for the geographic imputation to work
api_version = '18.0.2'

# And a start and end for update period.
# Supply this EITHER as ISO date (eg. 2017-09-01) or as VIEWS month_id (e.g. 389).
# To rebuild the whole DB, you can set the startmonth to '1989-01-01'.
# Note that startmonth will automatically set itself to 1997-01-01 for ACLED if startmonth is below
startmonth = '2018-01-01'
endmonth = '2018-02-28'
