""" test suite for calibration. """
import sys
import os

import unittest
import itertools
import string
import tempfile
import json

import pandas as pd
import numpy as np

from crosslevel import Crosslevel

sys.path.append("..")
from views_utils import dbutils
from views_utils import pyutils


class TestCrosslevel(unittest.TestCase):
    """Tests for Crosslevel module"""

    def setUp(self):
        """ Setup method for Crosslevel tests.

        Builds three dataframes:

        * self.df_h: high resolution probs
        * self.df_l: low resolution probs
        * self.df_h_links: links between high and low level probs"""

        def make_run_db():

            name = "cl_cm_fcast_test"
            job_1 = _make_jobdict(name="cl_colaresi_ds_sb",
                                 method="colaresi",
                                 col_h="ds_pgm_sb",
                                 col_l="ds_cm_sb")
            job_2 = _make_jobdict(name="cl_colaresi_mixed_sb",
                                  method="colaresi",
                                  col_h="osa_pgm_sb",
                                  col_l="ds_cm_sb")
            jobs = [job_1, job_2]


            run = {
                'name' : name,
                'jobs' : jobs,
                'table_h' : "landed_test.collected_pgm_fcast_test",
                'table_l' : "landed_test.collected_cm_fcast_test",
                'groupvar_h' : "pg_id",
                'groupvar_l' : "country_id",
                'timevar' : "month_id"
            }

            return run

        def make_local_settings(connectstring):

            local_settings = {
                'connectstring' : connectstring
            }

            return local_settings

        def _make_jobdict(name, method, col_h, col_l):

            job = {
                'name' : name,
                'method' : method,
                'col_h' : col_h,
                'col_l' : col_l,
            }

            return job


        def make_jobdict_colaresi():
            """ Make a job dictionary for a colaresian product """

            name = "colaresi_bc"
            method = "colaresi"

            col_h = "h_b"
            col_l = "l_c"

            job = _make_jobdict(name, method, col_h, col_l)

            return job

        def make_jobdict_product():
            """ Make a job dictionary for a simple product """

            name = "product_bc"
            method = "product"

            col_h = "h_b"
            col_l = "l_c"

            job = _make_jobdict(name, method, col_h, col_l)

            return job


        def make_probs(n, seed):
            """ Generate vector of normal probabilities with length n"""

            def scale_to_0_1(y):
                """ Scale a vector to have values in range 0-1 """
                y = (y - np.min(y)) / (np.max(y) - np.min(y))
                return y

            np.random.seed(seed)
            y = np.random.normal(0, 1, n)
            y = scale_to_0_1(y)

            return y

        def flatten_list(nested_list):
            """ Return a flat list if given a list of lists"""

            l_flat = list(itertools.chain(*nested_list))
            return l_flat

        def make_links(groups_h, groups_l):
            """ Return one random value of groups_l for each element in
            groups_h. The random value corresponds to a lower resolution id
            being assigned to a higher resolution id """

            np.random.seed(1)

            groups_links = []

            # make probabilities for each low level group
            groups_l_probs = make_probs(n=len(groups_l), seed=10)
            groups_l_probs = groups_l_probs / sum(groups_l_probs)

            for _ in groups_h:
                group_l = np.random.choice(groups_l, p=groups_l_probs)
                groups_links.append(group_l)

            groups_links = itertools.repeat(groups_links, len(times))
            groups_links = pyutils.flatten_list(list(groups_links))

            return groups_links

        def make_idx(times, groups, timevar, groupvar):
            """ Create named Multiindex """
            idx_tuples = list(itertools.product(times, groups))
            idx = pd.MultiIndex.from_tuples(idx_tuples, names=(timevar,
                                                               groupvar))
            return idx

        def make_df_with_probs(times, groups, timevar, groupvar, ncols, prefix):
            """ Make a df of probabilities"""
            idx = make_idx(times=times, groups=groups,
                           timevar=timevar, groupvar=groupvar)

            datadict = {}
            for i, letter in zip(range(ncols), string.ascii_lowercase):
                probs = make_probs(n=len(idx), seed=(i * len(idx)))
                name = "{}_{}".format(prefix, letter)
                datadict.update({name : probs})

            df = pd.DataFrame(datadict, index=idx)

            return df

        def make_df_links(times, timevar,
                          groups_h, groups_l,
                          groupvar_h, groupvar_l):
            """ Make df with links between groups_h and groups_l """
            idx = make_idx(times=times, groups=groups_h,
                           timevar=timevar, groupvar=groupvar_h)

            datadict_links = {
                groupvar_l : make_links(groups_h, groups_l)
            }

            df = pd.DataFrame(datadict_links, index=idx)
            return df




        self.timevar = "time"
        self.groupvar_h = "pg_id"
        self.groupvar_l = "country_id"
        self.connectstring = "postgresql://VIEWSADMIN@VIEWSHOST:5432/views"

        t_start = 1
        t_end = 5
        n_groups_h = 10  # high resolution groups (pg_ids)
        n_groups_l = 3  # low resolution groups (country_ids)

        groups_h = list(range(n_groups_h))
        groups_l = list(range(n_groups_l))
        times = list(range(t_start, t_end + 1))

        self.run_db = make_run_db()
        self.local_settings = make_local_settings(self.connectstring)
        self.job_colaresi = make_jobdict_colaresi()
        self.job_product = make_jobdict_product()

        self.df_h = make_df_with_probs(times=times, groups=groups_h,
                                       timevar=self.timevar,
                                       groupvar=self.groupvar_h,
                                       ncols=3, prefix="h")
        self.df_l = make_df_with_probs(times=times, groups=groups_l,
                                       timevar=self.timevar,
                                       groupvar=self.groupvar_l,
                                       ncols=3, prefix="l")

        self.df_links = make_df_links(times, self.timevar,
                                      groups_h, groups_l,
                                      self.groupvar_h, self.groupvar_l)

    def tearDown(self):
        pass


    def test_merge_levels_len(self):
        """ Test that merged df has same number of rows as high res df"""
        df = Crosslevel.merge_levels(self.df_h, self.df_l, self.df_links)
        self.assertEqual(len(df), len(self.df_h))

    def test_merge_levels_cols(self):
        """ Test that  all cols from low res df are included in merged df"""

        df = Crosslevel.merge_levels(self.df_h, self.df_l, self.df_links)

        cols_merged = sorted(list(df.columns))
        cols_h = sorted(list(self.df_h.columns))
        cols_l = sorted(list(self.df_l.columns))

        cols_wanted = cols_h + cols_l + [self.groupvar_l]
        cols_wanted = sorted(cols_wanted)

        self.assertEqual(cols_merged, cols_wanted)

    def test_merge_asserts_timevar_l(self):
        """ Test that merge_levels checks input df_l timevar """

        df_l_wrong_timevar = self.df_l.copy()
        df_l_wrong_timevar.index.rename(["wrong_timevar", self.groupvar_l],
                                        inplace=True)

        with self.assertRaises(AssertionError) as _:
            Crosslevel.merge_levels(self.df_h, df_l_wrong_timevar,
                                    self.df_links)

    def test_merge_asserts_timevar_links(self):
        """ Test that merge_levels checks input df_links timevar """

        df_links_wrong_timevar = self.df_links.copy()
        df_links_wrong_timevar.index.rename(["wrong_timevar", self.groupvar_l],
                                            inplace=True)

        with self.assertRaises(AssertionError) as _:
            Crosslevel.merge_levels(self.df_h, self.df_l,
                                    df_links_wrong_timevar)

    def test_compute_product(self):
        """ Test compute_product() """
        df = Crosslevel.merge_levels(self.df_h, self.df_l, self.df_links)
        first_col = df.columns[0]
        second_col = df.columns[1]
        product_1 = Crosslevel.compute_product(df, first_col, second_col)

        product_2 = df[first_col] * df[second_col]

        pd.testing.assert_series_equal(product_1, product_2)

    def test_compute_colaresi(self):
        """ Test compute_colaresi() """
        df = Crosslevel.merge_levels(self.df_h, self.df_l, self.df_links)

        col_h = self.df_h.columns[0]
        col_l = self.df_l.columns[0]

        sum_h_by_l = df.groupby([self.timevar,
                                self.groupvar_l])[col_h].transform('sum')

        p_h = df[col_h]
        p_l = df[col_l]

        joint_1 = p_l * (p_h / sum_h_by_l)

        joint_2 = Crosslevel.compute_colaresi(df, col_h, col_l,
                                              self.timevar, self.groupvar_l)



        pd.testing.assert_series_equal(joint_1, joint_2)

    def test_worker_colaresi(self):
        """ Test colaresi worker chain """

        # Compute colaresian product by calling static worker directly
        df_merged = Crosslevel.merge_levels(self.df_h, self.df_l,
                                            self.df_links)
        job = self.job_colaresi
        result_1 = Crosslevel.compute_colaresi(df=df_merged,
                                                    col_h = job['col_h'],
                                                    col_l = job['col_l'],
                                                    timevar=self.timevar,
                                                    groupvar_l=self.groupvar_l)

        # Compute by calling the worker chain

        this_cl = Crosslevel()
        this_cl._setup_state(self.df_h, self.df_l,
                            self.df_links,
                            self.timevar,
                            self.groupvar_h, self.groupvar_l)

        result_2 = this_cl.worker(self.local_settings, job)

        pd.testing.assert_series_equal(result_1, result_2)

    def test_worker_product(self):
        """ Test simple product worker chain """

        # Compute colaresian product by calling static worker directly
        df_merged = Crosslevel.merge_levels(self.df_h, self.df_l,
                                            self.df_links)
        job = self.job_product
        result_1 = Crosslevel.compute_product(df=df_merged,
                                              col_a = job['col_h'],
                                              col_b = job['col_l'])

        # Compute by calling the worker chain

        this_cl = Crosslevel()
        this_cl._setup_state(self.df_h, self.df_l,
                            self.df_links,
                            self.timevar,
                            self.groupvar_h, self.groupvar_l)

        result_2 = this_cl.worker(self.local_settings, job)

        pd.testing.assert_series_equal(result_1, result_2)

    def test_load_runfile_sets_cols(self):

        cols_h = ["ds_pgm_sb", "osa_pgm_sb"]
        cols_l = ["ds_cm_sb"]

        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.sep.join([tempdir, "run.json"])
            with open(path, 'w') as f:
                json.dump(self.run_db, f)

            cl = Crosslevel()
            cl.load_runfile(path)
            self.assertEqual(cl.cols_h, cols_h)
            self.assertEqual(cl.cols_l, cols_l)
            self.assertEqual(self.run_db['jobs'], cl.jobs)
            self.assertEqual(cl.table_h, "collected_pgm_fcast_test")
            self.assertEqual(cl.table_l, "collected_cm_fcast_test")
            self.assertEqual(cl.schema_h, "landed_test")
            self.assertEqual(cl.schema_l, "landed_test")

    def test_load_local_settings_file_connecstring(self):

        with tempfile.TemporaryDirectory() as tempdir:
            path = os.path.sep.join([tempdir, "local_settings.json"])
            with open(path, 'w') as f:
                json.dump(self.local_settings, f)

            cl = Crosslevel()
            cl.load_local_settings(path)
            self.assertEqual(self.local_settings['connectstring'], 
                             cl.connectstring)

    def test_fetch_data_is_df(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path_settings = os.path.sep.join([tempdir, "local_settings.json"])
            path_runfile = os.path.sep.join([tempdir, "runfile.json"])
            with open(path_settings, 'w') as f:
                json.dump(self.local_settings, f)
            with open(path_runfile, 'w') as f:
                json.dump(self.run_db, f)

            cl = Crosslevel()
            cl.load_local_settings(path_settings)
            cl.load_runfile(path_runfile)

        cl.fetch_data()





if __name__ == "__main__":
    unittest.main()
