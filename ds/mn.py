import numpy as np
import pandas as pd
import patsy
import statsmodels.api as sm
import h5py

#np.random.seed(0)


if __name__ == "__main__":
    # PARAMS
    n = 100
    nsim = 5
    y_vals = [25, 13, 1, -5, 19, 2, 7]
    weights = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08]
    weights.append(1-sum(weights))
    y_vals = [0, 1, 2]
    weights = [0.1, 0.1, 0.8]


    # Input vectors
    yvar = np.random.choice(y_vals, n, p=weights)
    x1 = yvar + np.random.uniform(0, 100, n)
    x2 = np.random.normal(0, 1, n)
    x3 = np.random.normal(0, 1, n)

    print(pd.Series(yvar).value_counts())


    # Input dataset
    df = pd.DataFrame({'conflict' : yvar, 'x1' : x1, 'x2' : x2, 'x3' : x3})

    # Models
    formula = "conflict ~ x1 + x2 + x3"

    y, X = patsy.dmatrices(formula, df, return_type='dataframe')
    model = sm.MNLogit(y, X).fit(disp=0)
    print(model.summary())


    # Check that both formulas give equal X_t
    #_, X_t = patsy.dmatrices(formula, df.loc[0:n-1])
    _, X_t = patsy.dmatrices(formula, df.loc[:])


    cov = model._results.cov_params()
    #print(f"cov_multi.shape:  {cov_multi.shape}")
    params = model.params
    params_simulated = np.random.multivariate_normal(np.ravel(params),
                                                     cov,
                                                     nsim)
    these_params_simulated = params_simulated[0]
    #print(f"params: {params}")
    #print(f"mean params: {these_params_simulated}")



    X_pred = np.dot(X_t, model.params)
    X_pred = np.dot(X_t, these_params_simulated.reshape(model.params.shape))
    predicted_probs = sm.MNLogit.cdf(None, X_pred)
    print(model.params)
    print(predicted_probs)
    print(model.predict(exog=X_t))
    print(predicted_probs.sum(axis=1))

    print(f"J: {model.model.J}")
    print(f"K: {model.model.K}")

    # The values of outcome that model found during training
    classes = list(model.model._ynames_map.values())
    # The values come out as strings, so cast them to float
    classes = list(map(float, classes))
    # The ordering is key, make sure it came out right
    assert classes == sorted(classes)

    def multinomial_predict(choices, probs):
        """ Return a random vector of predicted choices based on probs """

        # Cumulative prob that a category has been chosen
        cumulative_probs = probs.cumsum(axis=1)
        # Draw random thresholds from uniform [0, 1)
        thresholds = np.random.rand(len(cumulative_probs), 1)
        # The chosen is the last
        choice_idxs = (thresholds < cumulative_probs).argmax(axis=1)
        predictions = np.array(choices)[choice_idxs]
        return predictions

    predictions = multinomial_predict(choices=classes, probs=predicted_probs)
    print(predictions)
    print(predictions.mean())

def fix_summary_tex(summary):

    # Make tex tables less stupid with ugly hack
    summary = summary.replace("\_", "_")
    summary = summary.replace("_", "\_")
    return summary

def make_df_params(names, values):
    paramdict = {}
    for name, value in zip(names, values):
        paramdict.update({
            name : value})

    df_params = pd.DataFrame(paramdict, index=[0])
    return df_params


class SMMNLogit():

    def __init__(self, model_description):

        self.model_description = model_description

        self.name = model_description['name']
        self.formula = model_description['formula']

        self.filepath = model_description['path_output']
        self.filepath_txt = self.filepath.replace(".hdf5", ".txt")
        self.filepath_tex = self.filepath.replace(".hdf5", ".tex")


        self.betas = None
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


    @staticmethod
    def _predict(choices, probs):
        # @TODO: Document shapes
        """ Return a random vector of predicted choices based on probs

        Args:
            choices: List of possible choices
            probs: Probabilities matching each choice
        Returns:
             """

        # Cumulative prob that a category has been chosen
        cumulative_probs = probs.cumsum(axis=1)
        # Draw random thresholds from uniform [0, 1)
        thresholds = np.random.rand(len(cumulative_probs), 1)
        # The chosen is the last
        choice_idxs = (thresholds < cumulative_probs).argmax(axis=1)
        predictions = np.array(choices)[choice_idxs]
        return predictions

    @staticmethod
    def _draw_betas(model, nsim):
        """ Draw nsim parameter matrices (betas) from an MNLogit model """

        params = np.ravel(model.params)
        cov = model._results.cov_params()
        betas = np.random.multivariate_normal(params,
                                              cov,
                                              nsim)
        return betas

    @staticmethod
    def _extract_classes_from_model(model):
        """ Get the response variable classes of the MNLogit model as floats

        Args:
            model: An instance of a trained statsmodels MNLogit model

        Returns:
            classes: A list of floats corresponding to model response classes

        """

        # The classes are stored as a dict with incrementing integer indices
        # We cast it to a list of floats
        classes = list(model.model._ynames_map.values())
        classes = list(map(float,classes))

        # Make sure my assumptions of sorting hold
        message = "Class ordering assumption doesnt hodl"
        assert classes == sorted(classes), message

        return classes

    @staticmethod
    def _train_model(df, formula):

        y, X = patsy.dmatrices(formula, df, return_type='dataframe')
        model = sm.MNLogit(y, X).fit(disp=0)

        return model

    def from_description(self):
        # We already set the formula from the description in init
        pass

    def save(self):
        self.outputvars = [s.encode('ascii') for s in self.outputvars]
        path = self.filepath
        with h5py.File(path, 'w') as h5f:
            h5f.create_dataset('betas', data=self.betas)
            h5f.create_dataset('outputvars', data=self.outputvars)
            h5f.attrs['lhsvar'] = self.lhsvar
            h5f.attrs['formula'] = self.formula
            h5f.attrs['summary'] = self.summary
            h5f.create_dataset('predictions_training', data=self.predictions_training)
        del self.predictions_training

        with open(self.filepath_txt, 'w') as f:
            f.write(self.summary)
        with open(self.filepath_tex, 'w') as f:
            f.write(self.summary_tex)
        self.df_params.to_csv(self.filepath_params, index=False)

    def from_file(self):

        with h5py.File(self.filepath, 'r') as h5f:
            self.betas = h5f['betas'][:]
            self.outputvars = h5f['outputvars'][:]
            self.outputvars = list(self.outputvars)
            self.outputvars = [str(v, 'utf-8') for v in self.outputvars]
            self.lhsvar = h5f.attrs['lhsvar']
            self.formula = h5f.attrs['formula']
            self.summary = h5f.attrs['summary']
            self.trained = True
            self.populated = True


    def populate(self, nsim):

        self.nsim = nsim
        self.betas = self._draw_betas(self.model, self.nsim)
        self.params_shape = self.model.params.shape
        self.lhsvar = self.formula.split("~")[0].strip()
        self.outputvars=[self.lhsvar]



    def train(self, df):

        self.model = self._train_model(df, self.formula)
        self.classes = self._extract_classes_from_model(self.model)

        self.summary = str(self.model.summary())
        self.summary_tex = fix_summary_tex(self.model.summary().as_latex())

        self.df_params = pd.DataFrame(self.model.params).T

        self.predictions_training = self.model.predict()
        self.model.remove_data()


    def predict(self, sim, data):

        # Build feature matrix from formula and data
        _, X_t = patsy.dmatrices(self.formula, data)

        beta = self.betas[sim]
        # betas are stored as flat vectors in a matrix
        # reshape to give matrix of per-class vectors
        beta = beta.reshape(self.params_shape)

        X_t_dot_beta = np.dot(X_t, beta)
        # sm.MNLogit.cdf takes self as first parameter but doesn't use it
        # so pass in None. Second argument is array of predictors
        # predicted_probs is now a matrix with len(self.classes) probs per row
        # in X_t
        predicted_probs = sm.MNLogit.cdf(None, X_t_dot_beta)
        predicted_labels = self._predict(self.classes, predicted_probs)

        outputs = [predicted_labels]
        varnames = [self.lhsvar]

        return outputs, varnames









