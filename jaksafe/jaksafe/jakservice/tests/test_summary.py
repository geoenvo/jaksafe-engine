# coding = utf-8
__author__ = 'Abdul Somat Budiaji'

import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

import post_processing.summary as summary

class SummaryTest(unittest.TestCase):

    def setUp(self):

        self.time_0 = '20150203175959'
        self.time_1 = '20150203235959'

    def test_get_data_table_page_1(self):

        print 'begin test get data table page 1'
        ringkasan = summary.Summary(self.time_0, self.time_1)
        print ringkasan.get_data_table_page_1()
        print ringkasan.get_data_table_page_1()['df_data_sum']

    # def test_get_data_bar_page_1(self):
    #
    #     print 'begin test get data bar page 1'
    #     ringkasan = summary.Summary(self.time_0, self.time_1)
    #     print ringkasan.get_data_bar_page_1()

    # def test_get_data_table_page_4_and_5(self):
    #
    #     print 'begin test get data table page 4 and 5'
    #     ringkasan = summary.Summary(self.time_0, self.time_1)
    #     print ringkasan.get_data_table_page_4_and_5()['KERUSAKAN']
    #
    # def test_get_data_asuransi(self):
    #
    #     print 'begin test get data asuransi'
    #     ringkasan = summary.Summary(self.time_0, self.time_1)
    #     data = ringkasan.get_data_asuransi()
    #     print 'lalalal'
    #     print data['df_table'].ix[1].values


if __name__ == '__main__':

    unittest.main()
