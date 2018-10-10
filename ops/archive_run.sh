source config.sh

if [ ! -d "$DIR_ARCHIVE" ]; then
    echo "$DIR_ARCHIVE does not exist. Starting archiving there"
    mkdir -p $DIR_ARCHIVE
    rsync -avz $DIR_THIS_RUN/ $DIR_ARCHIVE/
else
    echo "ARCHIVE FAILED! $DIR_ARCHIVE already exists."
fi
