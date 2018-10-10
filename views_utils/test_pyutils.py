import unittest
import itertools

import pyutils

class TestPyutilsFlattenList(unittest.TestCase):

    def setUp(self):
        """ Setups some lists """ 

        self.l_flat = [1, 3, 2]
        self.l_nested = [[1, 3], [2]]

    def tearDown(self):
        """ Empty teardown """
        pass

    def test_flatten_list_basic_functionality(self):
        """ Test that list is flattened """

        l_flattened = pyutils.flatten_list(self.l_nested)

        self.assertEqual(self.l_flat, l_flattened)




class TestPyutilsDropDuplicates(unittest.TestCase):
    def setUp(self):
        """ Setup some lists """ 

        self.l_w_duplicates = [3, 1, 2, 2, 3]
        self.l_without_duplicates = [1, 2, 3]

        self.l_w_dupes_diff_types = ["a", "b", "a", 2, 1, 3]
        self.l_wo_dupes_diff_types = ["a", "b", 1, 2, 3]


    def test_drop_duplicates_basic_functionality(self):
        """ Test that duplicates are dropped """

        deduped = pyutils.drop_duplicates(self.l_w_duplicates)

        self.assertEqual(deduped, self.l_without_duplicates)




if __name__=="__main__":
    unittest.main()