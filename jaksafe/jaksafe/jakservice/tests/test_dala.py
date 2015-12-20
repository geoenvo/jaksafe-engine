# coding = utf-8
__author__ = 'Abdul Somat Budiaji'

import logging
import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))

import post_processing.dala as dala
import post_processing.config as config_post

class DalaTest(unittest.TestCase):

    def setUp(self):

        self.time_0 = '20150203175959'
        self.time_1 = '20150203235959'

        path = config_post.Path(self.time_0, self.time_1)
        if not os.path.isdir(path.log_dir):
            os.makedirs(path.log_dir)
        log_file = path.log_dir + 'dala_' + self.time_0 + '_' + self.time_1 + '.log'

        logger = logging.getLogger('jakservice')
        logger.setLevel('INFO')
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)

    # def test_dala_satu_include_koefisien(self):
    #
    #     print 'begin test dala satu include koefisien'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_satu('PUSKESMAS')
    #     # lada.dala_satu('PROVIDER')

    # def test_dala_satu_agama_include_koefisien(self):
    #
    #     print 'begin test dala satu agama include koefisien'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_satu('MASJID')
    #     lada.dala_satu('GEREJA')
    #     lada.dala_satu('VIHARA')

    # def test_dala_satu_minimarket_include_koefisien(self):
    #
    #     print 'begin test dala satu minimarket include koefisien'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_satu('MINIMARKET')

    # def test_dala_satu_pasartradisional_include_koefisien(self):
    #
    #     print 'begin test dala satu pasar tradisional include koefisien'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_satu('PASAR TRADISIONAL')

    #
    def test_dala_dua_include_koefisien(self):

        print 'begin test dala dua include koefisien'
        lada = dala.Dala(self.time_0, self.time_1)
        # lada.dala_dua('TAMBAK')
        lada.dala_dua('KEBERSIHAN')
        # lada.dala_satu('PROVIDER')
    #
    # def test_dala_tiga_no_koefisien(self):
    #
    #     print 'begin test dala tiga jalan tanpa koefisien'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_tiga('JALAN')

    # not pass
    # data still not completed
    # def test_dala_empat_no_koefisien(self):
    #
    #     print 'begin test dala empat kendaraan tanpa koefisien'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_empat('KENDARAAN')

    # def test_dala_lima(self):
    #
    #     print 'begin test dalam lima'
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.dala_lima('PROVIDER')
    #     lada.dala_lima('PERBANKAN')
    #     lada.dala_lima('BONGKAR MUAT PELABUHAN')

    # def test_dala_complete_using_hardcoded_list_subsektor(self):
    #
    #     print 'begin test dala complete using hardcoded list subsektor'
    #     list_subsektor = ['PERDAGANGAN', 'TRANSPORTASI', 'TELEKOMUNIKASI', 'FINANSIAL']
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.calculate(list_subsektor)

    # def test_dala_complete_sung_config_list_subsektor(self):
    #
    #     print 'begin test dala complete using global config list subsektor'
    #     ls_sub = config_post.ListSubsektor()
    #     list_subsektor = ls_sub.subsektor
    #     lada = dala.Dala(self.time_0, self.time_1)
    #     lada.calculate(list_subsektor)

if __name__ == '__main__':

    unittest.main()
