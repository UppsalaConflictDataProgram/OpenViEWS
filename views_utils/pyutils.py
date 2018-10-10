import itertools
import numpy as np

def flatten_list(nested_list):
    """ Return a flat list if given a list of lists"""

    l_flat = list(itertools.chain(*nested_list))

    return l_flat

def drop_duplicates(list_w_duplicates, sort=True):
    """ Drop duplicates from a list """ 

    list_unique = list(np.unique(list_w_duplicates))

    return list_unique
