""" Incomplete test suite for calibration. """
import unittest

import itertools

import pandas as pd
import numpy as np

import calibrate


class TestCalibration(unittest.TestCase):

    def setUp(self):
        """ Setup method for calibration tests.

        * Setup df1 and df2 as dataframes with different time limts
        * Generate probs as vector with values between 0-1"""

        def make_probs(n):
            """ Generate vector of normal probabilities with length n"""

            def scale_to_0_1(y):
                y = (y - np.min(y)) / (np.max(y) - np.min(y))
                return y

            y = np.random.normal(0, 1, n)
            y = scale_to_0_1(y)

            return y



        self.timevar = "time"
        self.groupvar = "group"

        times_1 = list(range(100, 201))
        times_2 = list(range(100, 202))
        groups = list(range(10))

        idx_1 = list(itertools.product(times_1, groups))
        idx_2 = list(itertools.product(times_2, groups))

        idx_1 = pd.MultiIndex.from_tuples(idx_1, names=(self.timevar,
                                                        self.groupvar))
        idx_2 = pd.MultiIndex.from_tuples(idx_2, names=(self.timevar,
                                                        self.groupvar))


        data_1 = np.random.random(len(idx_1))
        data_2 = np.random.random(len(idx_2))

        self.df1 = pd.DataFrame(data_1, index=idx_1)
        self.df2 = pd.DataFrame(data_2, index=idx_2)

        self.probs = make_probs(10)
        print(self.probs)



    def test_assert_equal_times(self):

        with self.assertRaises(AssertionError) as cm:
            calibrate.assert_equal_times(self.df1, self.df2, self.timevar)


if __name__ == "__main__":
    unittest.main()
