import os

def make_dir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print('Create dir {} successfully.'.format(dirname))