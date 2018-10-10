source config.sh

echo "Running crosslevel models"
cd $DIR_GITHUB/ensemble
python -u crosslevel.py

echo "Running calibration"
cd $DIR_GITHUB/calibrate
python -u calibrate.py

echo "Running ensembles"
cd $DIR_GITHUB/ensemble
python -u ensemble.py

echo "Finished"