
echo 'clearing output'
rm -r output/*

echo 'making dirstructure in .output'
mkdir output/ds
mkdir output/ds/runfiles
mkdir output/ds/paramfiles
mkdir output/ds/publishes
mkdir output/models
mkdir output/osa
mkdir output/osa/runfiles
mkdir output/osa/paramfiles
tree output

echo "Making all your models"
python modlist.py
python osa.py
python ds.py
python ds_transforms.py