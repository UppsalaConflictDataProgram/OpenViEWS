from __future__ import print_function
from __future__ import division


import os
import pandas as pd
import numpy as np
import h5py

from utils import inv_logit, vdecide

from numpy import log

import statsmodels.api as sm
import patsy

def load_model(job, from_file=True):
    if job['modtype'] == "SMLogit":
        model = SMLogit(job)
    elif job['modtype'] == "SMIdentity":
        model = SMIdentity(job)
    elif job['modtype'] == "SMMNLogit":
        model = SMMNLogit(job)
    else:
        print("Modtype", job['modtype'], "not recognized")
        raise NotImplementedError

    if from_file:
        model.from_file()
    else:
        model.from_description()
    return model

def make_df_params(names, values):
    paramdict = {}
    for name, value in zip(names, values):
        paramdict.update({
            name : value})

    df_params = pd.DataFrame(paramdict, index=[0])
    return df_params

class SMIdentity(object):
    def __init__(self, model_description):
        self.name = model_description['name']
        self.filepath = model_description['path_output']
        self.filepath_txt = self.filepath.replace(".hdf5", ".txt")
        self.filepath_tex = self.filepath.replace(".hdf5", ".tex")
        self.model_description = model_description


        self.betas = None
        self.formula = None
        self.lhsvar = None
        self.model = None
        self.outputvars = None
        self.populated = False
        self.trained = False

        self.df_params = None
        self.filepath_params = self.filepath.replace(".hdf5", "_params.csv")

        self.var_residuals = None


    def from_description(self):
        self.formula = self.model_description['formula']

    def from_file(self):
        #print("loading model", self.name, "from", self.filepath)
        path = self.filepath
        with  h5py.File(path,'r') as h5f:

            self.betas = h5f['betas'][:]

            # outputvars is a list of strings but hdf5 stores it as a numpy array
            # we need to recast it to a list so
            self.outputvars = h5f['outputvars'][:]
            self.outputvars = list(self.outputvars)
            # encode outputvars to regular strings as they are stored as bytes
            self.outputvars = [str(v, 'utf-8') for v in self.outputvars]

            self.lhsvar = h5f.attrs['lhsvar']
            self.formula = h5f.attrs['formula']
            self.var_residuals = h5f.attrs['var_residuals']

            self.trained = True
            self.populated = True

            # print("LHSVAR AND FORMULA")
            # print(self.lhsvar)
            # print(self.formula)
            # print("outputvars: ", self.outputvars)
            # print("type outputvars: ")
            # print(type(self.outputvars))

    def save(self):
        self.outputvars = [s.encode('ascii') for s in self.outputvars]
        print("saving", self.name, "to ", self.filepath)
        path = self.filepath
        with h5py.File(path, 'w') as h5f:
            h5f.create_dataset('betas', data=self.betas)
            h5f.create_dataset('outputvars', data=self.outputvars)
            h5f.attrs['lhsvar'] = self.lhsvar
            h5f.attrs['formula'] = self.formula
            h5f.attrs['summary'] = self.summary
            h5f.attrs['var_residuals'] = self.var_residuals
            h5f.create_dataset('predictions_training', data=self.predictions_training)
        del self.predictions_training

        with open(self.filepath_txt, 'w') as f:
            f.write(self.summary)
        with open(self.filepath_tex, 'w') as f:
            f.write(self.summary_tex)
        self.df_params.to_csv(self.filepath_params, index=False)

    def train(self, df):
        print("Training model", self.name)
        y, X = patsy.dmatrices(self.formula, df)
        self.model = sm.OLS(y, X).fit()

        #df_model is model degrees of freedom
        self.var_residuals = np.var(self.model.resid, ddof=self.model.df_model)
        print("var_residuals:", self.var_residuals)


        print(self.model.summary())
        self.summary = str(self.model.summary())
        summary_tex = str(self.model.summary().as_latex())

        # Make tex tables less stupid with ugly hack
        summary_tex = summary_tex.replace("\_", "_")
        summary_tex = summary_tex.replace("_", "\_")

        self.summary_tex = summary_tex

        params_names = X.design_info.column_names
        params_values = self.model.params
        self.df_params = make_df_params(params_names, params_values)

        # Store predicted probabilities for training data
        self.predictions_training = self.model.predict()
        self.model.remove_data()




        self.trained = True

    def populate(self, nsim):
        self.nsim = nsim
        def draw_betas(self):
            return (np.random.multivariate_normal(self.model.params,
                                                      self.model.cov_params(),
                                                      self.nsim))

        def populate_outputvars(self):
            self.outputvars = []
            self.outputvars.append(self.lhsvar)

        self.betas = draw_betas(self)
        self.lhsvar = self.formula.split("~")[0].strip()
        populate_outputvars(self)
        self.populated = True

    def predict(self, sim, data):
        beta = self.betas[sim].T
        y, X = patsy.dmatrices(self.formula, data)

        varnames = []
        varnames.append(self.lhsvar)

        outputs = []

        # predicted residuals have mean 0
        # np.random.normal takes a standard deviation so we take sqrt(var)
        n_predictions = len(y)
        predicted_residual = np.random.normal(0,
            np.sqrt(self.var_residuals),
            n_predictions)

        # prediction with residual
        outcome = X.dot(beta) + predicted_residual
        #outcome = X.dot(beta)

        outputs.append(outcome)

        return outputs, varnames

class SMLogit(object):
    def __init__(self, model_description):
        self.name = model_description['name']
        self.filepath = model_description['path_output']
        self.filepath_txt = self.filepath.replace(".hdf5", ".txt")
        self.filepath_tex = self.filepath.replace(".hdf5", ".tex")

        self.model_description = model_description

        self.betas = None
        self.formula = None
        self.lhsvar = None
        self.model = None
        self.options = None
        self.outputvars = None
        self.summary = None
        self.summary_tex = None

        self.predictions_training = None

        self.trained = False
        self.populated = False

        self.df_params = None
        self.filepath_params = self.filepath.replace(".hdf5", "_params.csv")


    def from_description(self):
        self.formula = self.model_description['formula']

    def list_items():
        """Don't use only for illustration of hdf5 files"""
        with h5py.File(path, 'r') as h5f:
            # get as list
            itemlist = h5f.items
            # or iterate
            for name, item in h5f.iteritems():
                print(name)
                print(item)
            # for attributes
            attrs_itemlist = h5f.attrs.items
            for name, item in h5f.attrs.iteritems():
                print(name)
                print(item)

    def from_file(self):
        #print("loading model", self.name, "from", self.filepath)
        path = self.filepath
        with  h5py.File(path,'r') as h5f:

            self.betas = h5f['betas'][:]

            # outputvars is a list of strings but hdf5 stores it as a numpy array
            # we need to recast it to a list so
            self.outputvars = h5f['outputvars'][:]
            self.outputvars = list(self.outputvars)
            self.outputvars = [str(v, 'utf-8') for v in self.outputvars]


            #self.predictions_training = h5f['predictions_training'][:]

            self.lhsvar = h5f.attrs['lhsvar']
            self.formula = h5f.attrs['formula']
            self.summary = h5f.attrs['summary']
            self.trained = True
            self.populated = True

            # print("LHSVAR AND FORMULA")
            # print(self.lhsvar)
            # print(self.formula)
            # print("outputvars: ", self.outputvars)
            # print("type outputvars: ")
            # print(type(self.outputvars))

    def save(self):
        self.outputvars = [s.encode('ascii') for s in self.outputvars]
        print("saving", self.name, "to ", self.filepath)
        path = self.filepath
        with h5py.File(path, 'w') as h5f:
            h5f.create_dataset('betas', data=self.betas)
            h5f.create_dataset('outputvars', data=self.outputvars)
            h5f.attrs['lhsvar'] = self.lhsvar
            h5f.attrs['formula'] = self.formula
            h5f.attrs['summary'] = self.summary
            # @TODO: Make this switchable
            h5f.create_dataset('predictions_training', data=self.predictions_training)
        del self.predictions_training

        with open(self.filepath_txt, 'w') as f:
            f.write(self.summary)
        with open(self.filepath_tex, 'w') as f:
            f.write(self.summary_tex)
        self.df_params.to_csv(self.filepath_params, index=False)



    def train(self, df):
        print("Training model", self.name)
        y, X = patsy.dmatrices(self.formula, df)
        self.model = sm.Logit(y, X).fit()
        print(self.model.summary())
        self.summary = str(self.model.summary())
        summary_tex = str(self.model.summary().as_latex())

        # Make tex tables less stupid with ugly hack
        summary_tex = summary_tex.replace("\_", "_")
        summary_tex = summary_tex.replace("_", "\_")

        self.summary_tex = summary_tex


        # Store predicted probabilities for training data
        self.predictions_training = self.model.predict()
        self.model.remove_data()

        params_names = X.design_info.column_names
        params_values = self.model.params
        self.df_params = make_df_params(params_names, params_values)


    def populate(self, nsim):
        self.nsim = nsim
        def draw_betas(self):
            return (np.random.multivariate_normal(self.model.params,
                                                  self.model.cov_params(),
                                                  self.nsim))

        # @TODO: This is somewhat redundant, we are creating the p_ variables both
        # here and in predict
        def populate_outputvars(self):
            self.outputvars = []
            self.outputvars.append(self.lhsvar)
            name = 'p_' + self.lhsvar
            self.outputvars.append(name)


        self.betas = draw_betas(self)
        self.lhsvar = self.formula.split("~")[0].strip()
        populate_outputvars(self)


    def predict(self, sim, data):
        # Select beta for this sim
        beta = self.betas[sim].T

        # Get matrix of predictors for data
        y, X = patsy.dmatrices(self.formula, data)

        # varnames lists the names of all variables to be returned
        varnames = []
        varnames.append(self.lhsvar)
        outputs = []

        nobs = X.shape[0]
        # Calculate predicted probabilities
        probs = inv_logit(X.dot(beta))

        # Realize outcome
        nature = np.random.uniform(size=(nobs))
        outcome = vdecide(nature, probs)
        #print("sm probs shape", probs.shape)
        #print("sm outcome shape", outcome.shape)
        outputs.append(outcome)

        # Add predicted probabilities to outputs
        pname = 'p_' + self.lhsvar
        varnames.append(pname)
        outputs.append(probs)
        #for output in outputs:
        #    print(output.shape)
        return outputs, varnames



