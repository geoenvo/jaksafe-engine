# coding = utf-8
__author__ = 'Abdul Somat Budiaji'

import logging
import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

import post_processing.post as post
import post_processing.config as config_post

class PostTest(unittest.TestCase):

    def setUp(self):

        self.time_0 = '20150210055959'
        self.time_1 = '20150210115959'

        path = config_post.Path(self.time_0, self.time_1)
        if not os.path.isdir(path.log_dir):
            os.makedirs(path.log_dir)
        log_file = path.log_dir + 'dala_' + self.time_0 + '_' + self.time_1 + '.log'

        logger = logging.getLogger('jakservice')
        logger.setLevel('INFO')
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)

    def test_run_all_post_proc(self):

        pp = post.PostProc(self.time_0, self.time_1)
        pp.analyze()


if __name__ == '__main__':

    unittest.main()
