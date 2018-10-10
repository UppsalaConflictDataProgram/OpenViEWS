source config.sh
TASK="cd $DIR_GITHUB/ops && bash submit_jobs_rackham.sh"
ssh rackham "$TASK"