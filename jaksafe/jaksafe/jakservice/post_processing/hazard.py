# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import logging

import numpy as np
from qgis.core import NULL

import shape

logger = logging.getLogger('jakservice.post_processing.hazard')

class Hazard(object):

    """
    Kelas Hazard
    """

    def __init__(self, hazard_shp):

        """
        Inisiasi kelas haard
        """

        self.shp = shape.Shape(hazard_shp)
        column = (
            'KABUPATEN',
            'KECAMATAN',
            'KELURAHAN',
            'RW',
            'RT',
            'AREA_HZ',
            'KELAS'
        )
        df_shp = self.shp.get_dataframe(*column)
        df_shp['PROVINSI'] = 'DKI JAKARTA'

        # order pandas dataframe column
        new_order = ([
            'PROVINSI',
            'KABUPATEN',
            'KECAMATAN',
            'KELURAHAN',
            'RW',
            'RT',
            'AREA_HZ',
            'KELAS'
        ])
        df_shp = df_shp.reindex_axis(new_order, axis=1)

        # rename pandas dataframe column
        new_names = ([
            'PROVINSI',
            'KOTA',
            'KECAMATAN',
            'KELURAHAN',
            'RW',
            'RT',
            'AREA',
            'KELAS_DAMPAK'
        ])
        df_shp.columns = new_names
        self.df_shp = df_shp

    def percent(self, dict_loc):

        """
        Mendapatkan persentasi wilayah untuk menghitung jumlah aset dalam wilayah
        tertentu
        """

        logger.info('Hazard.percent')

        # level = len(dict_loc)
        level = dict_loc['LEVEL_AGGREGAT']

        # kriteria filter
        kriteria = {}
        kriteria['KELAS'] = (self.df_shp['KELAS_DAMPAK']!=NULL)
        try:
            kriteria['PROVINSI'] = (self.df_shp['PROVINSI']==dict_loc['PROVINSI'])
        except KeyError:
            pass
        try:
            kriteria['KOTA'] = (self.df_shp['KOTA']==dict_loc['KOTA'])
        except KeyError:
            pass
        try:
            kriteria['KECAMATAN'] = (self.df_shp['KECAMATAN']==dict_loc['KECAMATAN'])
        except KeyError:
            pass
        try:
            kriteria['KELURAHAN'] = (self.df_shp['KELURAHAN']==dict_loc['KELURAHAN'])
        except KeyError:
            pass
        try:
            kriteria['RW'] = (self.df_shp['RW']==dict_loc['RW']) & \
                (self.df_shp['KELURAHAN']==dict_loc['KELURAHAN'])
        except KeyError:
            pass
        try:
            kriteria['RT'] = (self.df_shp['RT']==dict_loc['RT']) & \
                (self.df_shp['RW']==dict_loc['RW']) & \
                (self.df_shp['KELURAHAN']==dict_loc['KELURAHAN'])
            # mengantisipasi RT yang NULL
            if len(kriteria['RT'] > 1):
                kriteria['RT'] = (self.df_shp['RW']==dict_loc['RW']) & \
                    (self.df_shp['KELURAHAN']==dict_loc['KELURAHAN'])
        except KeyError:
            pass

        if level == 'PROVINSI':
            df_return = self.detail(kriteria['PROVINSI'])
        elif level == 'KOTA':
            df_return = self.detail(kriteria['KOTA'])
        elif level == 'KECAMATAN':
            df_return = self.detail(kriteria['KECAMATAN'])
        elif level == 'KELURAHAN':
            df_return = self.detail(kriteria['KELURAHAN'])
        elif level == 'RW':
            df_return = self.detail(kriteria['RW'])
        elif level == 'RT':
            df_return = self.detail(kriteria['RT'])

        df_return = df_return[kriteria['KELAS']]
        # print df_return[df_return['RT']==NULL].head()

        return df_return

    def detail(self, kriteria):

        logger.info('Hazard.detail')

        df_return = self.df_shp[kriteria]
        luas_total = df_return.sum().AREA
        df_return['PERCENTAGE'] = self.df_shp.AREA / luas_total

        return df_return

    def percent_agg(self, dict_loc):

        """
        Mendapatkan persentasi wilayah untuk menghitung dala aggregat

        :param: dict_loc
            dictionary dengan struktur sebagai berikut
            {
                'JENIS LEVEL' : PROVINSI, KOTA, KECAMATAN
                'NAMA LEVEL' : nama level yang tersebut
            }
        """

        logger.info('Hazard.percent_agg')

        level = dict_loc['JENIS LEVEL']

        # kriteria filter
        kriteria = {}
        kriteria['KELAS'] = (self.df_shp['KELAS_DAMPAK']!=NULL)
        try:
            kriteria['PROVINSI'] = (self.df_shp['PROVINSI']==dict_loc['NAMA LEVEL']) & \
            (kriteria['KELAS'])
        except KeyError:
            pass
        try:
            kriteria['KOTA'] = (self.df_shp['KOTA']==dict_loc['NAMA LEVEL']) & \
            (kriteria['KELAS'])
        except KeyError:
            pass
        try:
            kriteria['KECAMATAN'] = (self.df_shp['KECAMATAN']==dict_loc['NAMA LEVEL']) & \
            (kriteria['KELAS'])
        except KeyError:
            pass

        df_return = self.df_shp[kriteria[level]]
        luas_total = df_return.sum().AREA
        df_return['PERCENTAGE'] = df_return.AREA / luas_total

        return df_return
