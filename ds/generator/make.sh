rm output/paramfiles/*
rm output/runfiles/*
rm output/publishes/*

python make_paramfiles.py
python make_runfiles.py
python make_publishes.py
