#!/bin/bash
python GetFromFile.py \
    --uname VIEWSADMIN\
    --path_input /Users/VIEWSADMIN/Dropbox/CntData/Masterdata/MasterData.csv \
    --path_varlist varlist_masterdata.txt\
    --schema dataprep\
    --table fovp\
#    --force\