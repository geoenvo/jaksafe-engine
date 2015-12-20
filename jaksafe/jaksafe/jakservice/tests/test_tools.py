# coding=utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

import post_processing.tools as tools

class TestTools(unittest.TestCase):

    def setUp(self):

        self.time_0 = '20150210055959'
        self.time_1 = '20150210115959'

        self.o_zipper = tools.Zipper(self.time_0, self.time_1)

    def test_zipper_hazard_impact(self):

        self.o_zipper.zip_result()

if __name__ == '__main__':

    unittest.main()
