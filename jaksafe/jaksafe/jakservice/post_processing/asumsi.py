# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import logging

import pandas as pd
import numpy as np

logger = logging.getLogger('jakservice.post_processing.asumsi')

class Asumsi(object):

    """
    Antarmuka untuk file-file asumsi
    """

    pass

    def __init__(self):

        """
        Inisiasi kelas Asumsi
        """

        pass

    def agregat(self, input_file, aset):

        """
        Mendapatkan parameter-parameter kunci untuk asumsi agregat

        :param input_file: file asumsi agregat
        :param aset: jenis aset
        :return: dictionary yang memiliki struktu data sebagai berikut.
            {JENIS LEVEL: ...,
            NAMA LEVEL: ...,
            KERUSAKAN: ...,
            KERUGIAN: ...,
            SUBSEKTOR: ...,
            ASET: ...,}
        """

        logger.info('Asumsi.agregat')

        df = pd.read_csv(input_file)

        df = df[df.ASET==aset]
        df = df.T

        level = []
        dict_return = {}

        for index, row in df.iterrows():
            if index == 'SUBSEKTOR':
                break
            if not pd.isnull(row.values[0]):
                level.append(index)

        dict_return['JENIS LEVEL'] = level[-1]
        dict_return['NAMA LEVEL'] = df.loc[level].values[0][0]
        dict_return['KERUSAKAN'] = df.loc['KERUSAKAN'].values[0]
        dict_return['KERUGIAN'] = df.loc['KERUGIAN'].values[0]
        dict_return['SUBSEKTOR'] = df.loc['SUBSEKTOR'].values[0]
        dict_return['ASET'] = df.loc['ASET'].values[0]

        return dict_return

    def asuransi(self, input_file):

        """
        Mendapatkan konstanta yan berada di file asumsi asuransi
        """

        logger.info('Asumsi.asuransi')

        df = pd.read_csv(input_file, index_col=0)

        a = df.loc['POPULASI DKI JAKARTA', 'NILAI']
        b = df.loc['KEMUNGKINAN KECELAKAAN', 'NILAI']
        c = df.loc['NILAI KLAIM ASURANSI GENERAL ACCIDENT', 'NILAI']

        return a*b*c

    def penetrasi_asuransi(self, input_file):

        """
        Mendapatkan datfarame file asumsi penetrasi asuransi
        """

        logger.info('Asumsi.penetrasi_asuransi')

        df = pd.read_csv(input_file)

        return df
