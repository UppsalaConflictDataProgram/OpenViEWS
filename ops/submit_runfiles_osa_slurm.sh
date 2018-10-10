source config.sh
DIR_RUNFILES=$DIR_GITHUB/models/output/osa/runfiles/*
echo "Submitting all files in $DIR_RUNFILES to slurm"
for runfile in $DIR_RUNFILES; do
    sbatch $runfile
done