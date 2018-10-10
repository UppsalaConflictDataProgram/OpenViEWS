"""Statsmodels wrapper for N-step script

This module provides a wrapper around the Statsmodels SMLogit class for 
compatibility with Scikit learn syntax. 

"""
import pandas as pd
import numpy as np
import sys
import statsmodels.api as sm

sys.path.insert(0, "..")
from ds.utils import inv_logit


class SMLogit(object):
    def add_intercept(self, X):
        # add a vector of ones to use as intercept. 
        df = pd.DataFrame(X)
        df['intercept'] = np.ones(len(df))
        X = np.asarray(df)
        return X


    def __init__(self):
        self.model = None

    def __str__(self):
        return "SMLogit object"

    def fit(self, X, y):
        # Check that input labels are binary
        assert len(np.unique(y)) == 2, "y does not contain 2 unique elements"
        
        X = self.add_intercept(X)

        self.model = sm.Logit(y, X).fit()
        print(self.model.summary())

    def predict(self, X, threshold = 0.5):
        """ Predict method that returns binary labels

        Predict from sm.Logit() returns probabilities by default."""
        X = self.add_intercept(X)
        # predict returns probabilities
        pred = self.model.predict(exog=X)
        # cast to bools
        pred = pred>threshold
        # cast to ints
        pred = pred.astype(int)
        return pred

    def predict_proba(self, X):
        """ Return rank 2 array of probs for labels """
        X = self.add_intercept(X)
        pred_1 = self.model.predict(exog=X)
        pred_0 = 1 - pred_1
        probas = np.array([pred_0, pred_1])
        return probas.T

