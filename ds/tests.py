import unittest
import tempfile
import os

import numpy as np
import pandas as pd
import patsy
import statsmodels


from mn import SMMNLogit

class TestSMMNLogit(unittest.TestCase):

    def setUp(self):

        self.n = 1000
        self.choices = [0, 1, 2, 3, 4, 5]
        self.weights_choices = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]

        # Input vectors
        yvar = np.random.choice(self.choices, self.n, p=self.weights_choices)
        x1 = yvar + np.random.uniform(0, 10, self.n)
        x2 = np.random.normal(0, 1, self.n)
        x3 = np.random.normal(0, 1, self.n)
        x4 = np.random.normal(0, 1, self.n)

        # Input dataset
        self.df = pd.DataFrame({'conflict' : yvar,
                                'x1' : x1, 'x2' : x2, 'x3' : x3, 'x4' : x4})

        # Models
        self.formula = "conflict ~ x1 + x2 + x3 + x4"

        # Number of variables, 3 + 1 for intercept
        # 1 + x1 + x2 + x3 + x4
        self.K = 4 + 1
        # Number of choices
        self.J = (len(self.choices))
        # Number of params is number of choices - 1 (for base case)
        # times the number of variables
        self.n_params = (self.J - 1) * self.K
        self.params_shape = (self.K, self.J-1)


        self.model_description = {
            'name' : 'smnlogit_test',
            'formula' : self.formula,
            'path_output' : "/some/path"
        }

        self.nsim = 10

    def test_private_train_returns_model(self):
        """ Test that the private train method returns a results wrapper """

        wanted = statsmodels.discrete.discrete_model.MultinomialResultsWrapper
        modobj = SMMNLogit(self.model_description)
        returned = modobj._train_model(self.df, self.formula)

        self.assertIsInstance(returned, wanted)

    def test_private_predict_single(self):
        """ Test that _predict returns correct single predictions """
        #

        probs_flat_0 = np.array([[1.0, 0., 0.]])
        predicted_0 = SMMNLogit._predict(self.choices, probs_flat_0)

        probs_flat_1 = np.array([[0.0, 0., 1.]])
        predicted_1 = SMMNLogit._predict(self.choices, probs_flat_1)


        self.assertEqual(predicted_0, 0)
        self.assertEqual(predicted_1, 2)

    def test_private_predict_multi(self):
        """ Test that _predict returns correct single predictions """


        # should give [0, 1, 2] as predictions because we give each case
        # 100% prob for each of the 3 rows
        probs = np.array([
                         [1., 0., 0.],
                         [0., 1., 0.],
                         [0., 0., 1.]])

        predicted = SMMNLogit._predict(self.choices, probs)
        wanted = [0, 1, 2]

        self.assertTrue(np.array_equal(predicted, wanted))


        # should give [0, 1, 2] as predictions because we give each case
        # 100% prob for each of the 3 rows
        probs = np.array([
                         [0., 0., 1.],
                         [0., 1., 0.],
                         [1., 0., 0.]])

        predicted = SMMNLogit._predict(self.choices, probs)
        wanted = [2, 1, 0]

        self.assertTrue(np.array_equal(predicted, wanted))


    def test_private_predict_returns_shape(self):
        """ Test that _predict gives one prediction per row in probs """

        probs_flat = np.array([[1.0, 0., 0.]])
        probs_deep = np.array([[0., 0., 1.],
                               [0., 1., 0.],
                               [1., 0., 0.],
                               [1., 0., 0.]])


        predicted_flat = SMMNLogit._predict(self.choices, probs_flat)
        predicted_deep = SMMNLogit._predict(self.choices, probs_deep)
        self.assertEqual(predicted_flat.shape[0], probs_flat.shape[0])
        self.assertEqual(predicted_deep.shape[0], probs_deep.shape[0])
        self.assertEqual(predicted_flat.shape[0], 1)

    def test_private_draw_betas_shape(self):
        """ Test that drawn betas have correct shape """

        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)

        betas_100 = SMMNLogit._draw_betas(modobj.model, 100)
        betas_1 = SMMNLogit._draw_betas(modobj.model, 1)

        self.assertEqual((100, self.n_params), betas_100.shape)
        self.assertEqual((1, self.n_params), betas_1.shape)

    def test_model_params_shape(self):
        """ Test that I've understood n_params properly """

        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)

        # ravel (flatten) the parameters to get their number
        self.assertEqual(self.n_params, len(np.ravel(modobj.model.params)))
        self.assertEqual(self.params_shape, modobj.model.params.shape)

    def test_model_jk(self):
        """ Test that I've understood J and K correctly """

        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)

        self.assertEqual(self.J, modobj.model.model.J)
        self.assertEqual(self.K, modobj.model.model.K)

    def test_populate_shape(self):

        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)
        modobj.populate(self.nsim)

        self.assertEqual(self.params_shape, modobj.params_shape)

    def test_private_extract_classes_from_model(self):

        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)
        model = modobj.model

        classes_from_func = SMMNLogit._extract_classes_from_model(model)

        classes_from_data = self.df['conflict'].unique()

        for c in classes_from_data:
            self.assertIn(c, classes_from_func)

    def test_train_sets_summary(self):
        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)

        self.assertIsInstance(modobj.summary, str)

    def test_populate_sets_lhsvar(self):
        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)
        modobj.populate(self.nsim)

        self.assertEqual(modobj.lhsvar, "conflict")


    def test_predict_returns_tuple(self):
        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)
        modobj.populate(self.nsim)
        prediction = modobj.predict(sim=0, data=self.df.loc[5])
        self.assertIsInstance(prediction, tuple)

    def test_predict_insert_into_df(self):

        ts = 0
        te = self.n-1

        modobj = SMMNLogit(self.model_description)
        modobj.train(self.df)
        modobj.populate(self.nsim)
        prediction, varname = modobj.predict(sim=0, data=self.df.loc[ts:te])

        self.df[varname] = 0
        self.df.loc[ts:te, varname] = prediction[0]

    def test_save_load(self):

        with tempfile.TemporaryDirectory() as tempdir:
            fname = "smnlogit_testing.hdf5"
            path = os.path.join(tempdir, fname)

            # Set the descriptions path_output to this temp dir
            this_desc = self.model_description.copy()
            this_desc['path_output'] = path

            modobj_saving = SMMNLogit(this_desc)
            modobj_saving.train(df=self.df)
            modobj_saving.populate(nsim=self.nsim)
            modobj_saving.save()

            modobj_loaded = SMMNLogit(this_desc)
            modobj_loaded.from_file()

            same_beta = np.array_equal(modobj_saving.betas, modobj_loaded.betas)
            self.assertTrue(same_beta)
            self.assertEqual(modobj_saving.lhsvar, modobj_loaded.lhsvar)
            self.assertEqual(modobj_saving.formula, modobj_loaded.formula)












if __name__ == "__main__":
    unittest.main()