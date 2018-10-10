""" Crosslevel module

This module provides cross level models that combine high and low resolution
models.

_h and _l refer to high and low resolution respectively.

Examples of high resolution might be priogrid and low might be country but
any low resolution should logically contain the higher resolution.

"""
import sys
import argparse
import json

sys.path.append("..")
from views_utils import dbutils
from views_utils import pyutils


class Crosslevel():

    def __init__(self):
        """ Init Crosslevel instance with empty state """
        self.timevar = None
        self.groupvar_l = None
        self.groupvar_h = None
        self.df = None
        self.table_h = None
        self.table_l = None
        self.schema_h = None
        self.schema_l = None
        self.cols_h = []
        self.cols_l = []
        self.jobs = []

    @staticmethod
    def merge_levels(df_h, df_l, df_links):
        """ Merge high resolution and low resolution prediction using links"""

        def assert_same_timevar(df_a, df_b):
            """ Assert that the three input dataframes share a common timevar"""
            timevar_a = df_a.index.names[0]
            timevar_b = df_b.index.names[0]


            msg = ("dfs in merge_levels() use different timevar "
                   "{} is not {}").format(timevar_a, timevar_b)
            assert timevar_a == timevar_b, msg

        def assert_same_timelimits(df_a, df_b):
            """ Make sure df_a and df_b cover the same time frame """
            def get_time_limits(df):
                """ Get a tuple (min, max) of index level 0 values """
                t_start = df.index.get_level_values(0).min()
                t_end = df.index.get_level_values(0).max()
                limits = (t_start, t_end)
                return limits

            limits_a = get_time_limits(df_a)
            limits_b = get_time_limits(df_b)
            msg = "{} is not {}".format(limits_a, limits_b)
            assert limits_a == limits_b, msg


        assert_same_timevar(df_h, df_l)
        assert_same_timevar(df_h, df_links)
        assert_same_timelimits(df_h, df_l)

        timevar = df_h.index.names[0]
        groupvar_h = df_h.index.names[1]
        groupvar_l = df_l.index.names[1]

        # Merge in the links, i.e. the low res groupvar
        df = df_h.merge(df_links, left_index=True, right_index=True)

        # Merge on indexes to keep indexes in merged df
        df.reset_index(inplace=True)
        df.set_index([timevar, groupvar_l], inplace=True)
        df = df.merge(df_l, left_index=True, right_index=True)
        df.reset_index(inplace=True)
        df.set_index([timevar, groupvar_h], inplace=True)
        df.sort_index(inplace=True)

        return df

    @staticmethod
    def compute_product(df, col_a, col_b):
        """ Compute simple product of col_h and col_l in df """

        cols = [col_a, col_b]
        product = df[cols].product(axis=1)

        return product

    @staticmethod
    def compute_colaresi(df, col_h, col_l, timevar, groupvar_l):
        """ Colaresian cross level probability """

        # Sum of high resolution probabilities for each low level area
        sum_h_by_l = df.groupby([timevar, groupvar_l])[col_h].transform(sum)

        # Low resolution prob multiplied by share of high res prob of area in a
        # particular area
        joint_prob = df[col_l] * (df[col_h] / sum_h_by_l)

        return joint_prob

    def worker_colaresi(self, local_settings, job):
        col_h = job['col_h']
        col_l = job['col_l']
        timevar = self.timevar
        groupvar_l = self.groupvar_l

        result = Crosslevel.compute_colaresi(self.df,
                                             col_h, col_l,
                                             timevar, groupvar_l)

        return result

    def worker_product(self, local_settings, job):
        col_a = job['col_h']
        col_b = job['col_l']

        result = Crosslevel.compute_product(self.df,
                                            col_a,
                                            col_b)

        return result

    def worker(self, local_settings, job):

        def worker_assigner(self, job):
            """ Returns appropriate worker for the jobs method """

            method = job['method']

            if method == "colaresi":
                return self.worker_colaresi
            elif method == "product":
                return self.worker_product
            else:
                msg = "Found no worker for method {]".format(method)
                raise NotImplementedError(msg)

        this_worker = worker_assigner(self, job)
        result = this_worker(local_settings, job)
        return result

    def _setup_state(self, df_h, df_l, df_links,
                    timevar, groupvar_h, groupvar_l):

        self.df = self.merge_levels(df_h, df_l, df_links)
        self.timevar = timevar
        self.groupvar_h = groupvar_h
        self.groupvar_l = groupvar_l

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--path_runfile", type=str, required=True,
                            help="path to json specifying job")
        parser.add_argument("--path_local_settings", type=str, required=True,
                            help="path to json specifying job")
        args = parser.parse_args()
        argdict = {
            'path_runfile' : args.path_runfile,
            'path_local_settings' : args.path_local_settings
        }

        return argdict

    def load_runfile(self, path_runfile):

        with open(path_runfile, 'r') as f:
            run = json.load(f)

        self.name = run['name']
        self.jobs = run['jobs']
        self.groupvar_l = run['groupvar_l']
        self.groupvar_h = run['groupvar_h']
        self.timevar = run['timevar']

        self.schema_h, self.table_h = run['table_h'].split(".")
        self.schema_l, self.table_l = run['table_l'].split(".")

        for job in self.jobs:
            self.cols_h.append(job['col_h'])
            self.cols_l.append(job['col_l'])

        self.cols_h = pyutils.drop_duplicates(self.cols_h)
        self.cols_l = pyutils.drop_duplicates(self.cols_l)



    def load_local_settings(self, path_local_settings):

        with open(path_local_settings, 'r') as f:
            local_settings = json.load(f)

        self.connectstring = local_settings['connectstring']

    def fetch_data(self):
        self.df_h = dbutils.db_to_df(connectstring=self.connectstring, 
                                     schema=self.schema_h,
                                     table=self.table_h)


    def main(self):
        """ Crosslevel main """
        args = self.parse_args()
        path_local_settings = args['path_local_settings']
        path_runfile = args['path_runfile']

        self.load_runfile(path_runfile)
        self.load_local_settings_file(path_local_settings)

if __name__ == "__main__":
    crosslevel = Crosslevel()
    crosslevel.main()
