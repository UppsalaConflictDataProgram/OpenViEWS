# Models
This directory contains automatic model generation scripts for DS and OSA.

## How?

### Update or add models
Poke around in modlist.py and varsets.py

### Add estimators to OSA
Add them to osa.py

### Change times
in times.py

## Why though?

* 4 time periods
* 4 outcomes
* 2 levels of analysis
* with or without ACLED
* different sets of predictors
* Multiple estimation techniques in OSA

These all multiply and create a LOT of models, and they aren't getting any 
fewer.
At the time of writing these scripts create 14316 lines of ds paramfiles and 
22136 lines of osa paramfiles. 

## The good
* PENDING: it works (?)
* Easy updates for each month
* Write model specification once, use in both OSA and DS, for each time, etc.
* output/models/ contains the exact spec of each model for easier documentation
* Time periods adminstered through one file (times.py), just update it each run
* Each paramfile that goes into production is very verbose and contains no
references to external feature sets, they are complete.


## The bad (and ugly)
The code itself. It's very much a rough draft.


## TODO:
Probably a complete rewrite so other people can actually read and improve it