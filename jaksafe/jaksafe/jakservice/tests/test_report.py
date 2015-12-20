# coding = utf-8
__author__ = 'Abdul Somat Budiaji'

import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

import post_processing.report as report
import post_processing.config as config_post
import post_processing.summary as summary

class ReportTest(unittest.TestCase):

    def test_create_report(self):

        print 'begin test create report'
        time_0 = '20150203175959'
        time_1 = '20150203235959'

        o_list = config_post.ListSubsektor()
        list_subsektor = o_list.subsektor

        ringkasan = summary.Summary(time_0, time_1)
        report.report_dala(time_0, time_1, ringkasan, list_subsektor)


if __name__ == '__main__':

    unittest.main()
