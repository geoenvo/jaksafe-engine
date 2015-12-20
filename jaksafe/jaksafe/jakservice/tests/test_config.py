# coding = utf-8
__author__ = 'Abdul Somat Budiaji'

import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

import post_processing.config as config

class ConfigTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_config_daftar_subsektor(self):
        pass
        subs = config.ListSubsektor()
        print subs.subsektor


if __name__ == '__main__':

    unittest.main()
