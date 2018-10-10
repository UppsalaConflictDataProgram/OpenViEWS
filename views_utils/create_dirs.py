import os

def create_dirs(*args):
    """Create a folder in locations supplied by each of the arguments"""
    for folder in args:
        if not os.path.isdir(folder):
            os.makedirs(folder)
            print("Created directory ", folder)
