__AUTHOR__ = 'Abdul Somat Budiaji'

import logging

import pandas as pd
import numpy as np

from error import *

logger = logging.getLogger('jakservice.post_processing.aggregate')

class Aggregate(object):

    """
    Kelas untuk file input aggregate
    """

    def __init__(self, input_file):

        """
        Inisiasi kelas Aggregate
        """

        # column header names
        # column_names = ['PROVINSI', 'KOTA', 'KECAMATAN', 'KELURAHAN', 'RW', \
        # 'SUBSEKTOR', 'ASET', 'JUMLAH']
        self.df_input = pd.read_csv(input_file)

    def jumlah(self, aset, **kwargs):

        """
        Mendapatkan jumlah aset di wilayah tertentu

        :param aset: tipe aset yang hendak dicari jumlahnya
        :return: jumlah aset
        """

        logger.info('Aggregate.jumlah')

        # get location parameter
        location = {}
        for key, val in kwargs.items():
            location[key] = val
        for geo in location:
            try:
                jumlah_aset = self.aset_in(aset, geo, location[geo])
            except MultipleJumlahAsetError:
                logger.error('multi')
                continue
            except EmptyJumlahAsetError:
                logger.error('empty')
                continue
        # pass
        # print jumlah_aset
        return 5

    def aset_in(self, aset, geolevel, location):

        """
        Mendapatkan potongan data agregat dengan kriteria tertentu

        :param aset: jenis aset
        :param location: lokasi aset
        :return: dataframe
        """

        logger.info('Aggregate.aset_in')

        kriteria = (self.df_input[geolevel]==location) & \
        (self.df_input.ASET==aset)

        df_return = self.df_input[kriteria]
        len_df_return = len(df_return)

        if len_df_return == 1:
            return df_return
        elif len_df_return > 1:
            raise MultipleJumlahAsetError
        elif len_df_return == 0:
            raise EmptyJumlahAsetError

    def satu(self, series):

        """
        Mendapatkan jumlah aset dan nama lokasi yang bersangkutan
        """

        logger.info('Aggregate.satu')

        aset = series.ASET
        location = {}
        mark = []
        for index, value in series.iteritems():
            location[index] = value
            try:
                if np.isnan(value):
                    mark.append(index)
            except TypeError, e:
                logger.error(e)

        # delete item from dict location whose key in mark
        for m in mark:
            location.pop(m)

        # menentukan level aggregat
        if location.has_key('RT'):
            location['LEVEL_AGGREGAT'] = 'RT'
        elif location.has_key('RW'):
            location['LEVEL_AGGREGAT'] = 'RW'
        elif location.has_key('KELURAHAN'):
            location['LEVEL_AGGREGAT'] = 'KELURAHAN'
        elif location.has_key('KECAMATAN'):
            location['LEVEL_AGGREGAT'] = 'KECAMATAN'
        elif location.has_key('KOTA'):
            location['LEVEL_AGGREGAT'] = 'KOTA'
        elif location.has_key('PROVINSI'):
            location['LEVEL_AGGREGAT'] = 'PROVINSI'

        try:
            location['RT'] = self.fix_format_rt(location['RT'])
        except KeyError, e:
            logger.error(e)

        return location

    def fix_format_rt(self, rt):

        """
        Menyeragamkan format nama RT sehingga sesuai dengan format yang ada di
        shapefile hazard (001, 002, 010, dan sebagainya)
        """

        logger.info('Aggregate.fix_format_rt')

        rt = int(rt)
        rt = str(rt)

        if len(rt) == 1:
            rt = '00' + rt
        elif len(rt) == 2:
            rt = '0' + rt

        return rt
