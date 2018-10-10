# N-STEP

This directory contains two important files:

## example.py

This file contains an example use of the N-step ahead forecasting module.
It specifies all the necessary parameters for a complete run that ends
up in the database. 
Make a copy and change whatever you want. 


## utils.py

This is where the magic happens.
This can be imported from other scripts or notebooks. 
The main function is forecast() which is called with a model dictionary as
its only parameter and it returns a dataframe of forecasted values. 
For example dictionaries see example.py
These forecasts are predicted labels, raw predicted probabilities, and their 
linear interpolations. 
Actual outcomes are also included for evaluation purposes. 


