# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import logging
import os
import random
import sys

import numpy as np
import pandas as pd

import aggregate
import config
from error import *
import hazard
import shape

logger = logging.getLogger('jakservice.post_processing.post')

class PostProc():

    """
    Kelas untuk analisa postprocessing

    :param time_0: waktu awal kejadian banjir
    :param time_1: waktu akhir kejadian banjir (waktu dimulainya perhitungan dala)
    """

    def __init__(self, time_0, time_1, tipe='auto'):

        """
        Inisiasi kelas PostProc
        """

        self.time_0 = time_0
        self.time_1 = time_1

        self.path = config.Path(time_0, time_1, tipe=tipe)

    def building(self, shapefile):

        """
        Analisa postprocessing bangunan
        """

        logger.info('PostProc.building')

        # building
        o_building = shape.Shape(shapefile)
        # columns in shapefile building that is extracted
        building_columns = (
            'KABUPATEN',
            'KECAMATAN',
            'KELURAHAN',
            'JS_SECTOR',
            'JS_ASSET',
            'KELAS',
            'JS_COEF'
        )

        try:
            df_building = o_building.get_dataframe(*building_columns)
        except NoColumnSpecifiedError:
            logger.error('no column specified error')
            sys.exit(1)

        df_building['JUMLAH_ASET'] = 1
        df_building['PROVINSI'] = 'DKI JAKARTA'

        # order dataframe column
        new_order = ([
            'PROVINSI',
            'KABUPATEN',
            'KECAMATAN',
            'KELURAHAN',
            'JS_SECTOR',
            'JS_ASSET',
            'KELAS',
            'JUMLAH_ASET',
            'JS_COEF'
        ])
        df_building = df_building.reindex_axis(new_order, axis=1)

        # rename dataframe column
        new_names = ([
            'PROVINSI',
            'KOTA',
            'KECAMATAN',
            'KELURAHAN',
            'SUBSEKTOR',
            'ASET',
            'KELAS_DAMPAK',
            'JUMLAH_ASET',
            'KOEFISIEN'
        ])
        df_building.columns = new_names

        return df_building

    def road(self, shapefile):

        """
        Analisa postprocessing jalan
        """

        logger.info('PostProc.road')

        # road
        o_road = shape.Shape(shapefile)
        road_columns = (
            'NAME',
            'PANJANG',
            'KELAS',
            'KABUPATEN',
            'KECAMATAN',
            'KELURAHAN',
            'RW',
            'RT'
        )

        try:
            df_road = o_road.get_dataframe(*road_columns)
        except NoColumnSpecifiedError:
            logger.error('no column specified error')
            sys.exit(1)

        df_road['PROVINSI'] = 'DKI JAKARTA'

        # order dataframe column
        new_order = ([
            'NAME',
            'PANJANG',
            'KELAS',
            'PROVINSI',
            'KABUPATEN',
            'KECAMATAN',
            'KELURAHAN',
            'RW',
            'RT'
        ])
        df_road = df_road.reindex_axis(new_order, axis=1)

        # rename dataframe column
        new_names = ([
            'NAMA_JALAN',
            'PANJANG',
            'KELAS_DAMPAK',
            'PROVINSI',
            'KOTA',
            'KECAMATAN',
            'KELURAHAN',
            'RW',
            'RT'
        ])
        df_road.columns = new_names

        return df_road

    def aggregate(self, shapefile):

        """
        Analisa postprocessing aggregat
        """

        logger.info('PostProc.aggregate')

        # input
        aggregate_dir = self.path.aggregate_dir
        agg_file = aggregate_dir + 'aggregate.csv'

        # raise error if no file aggregate csv
        if not os.path.isfile(agg_file):
            raise NoAggregateFileError

        agg = aggregate.Aggregate(agg_file)
        haz = hazard.Hazard(shapefile)

        data = []

        for index, series in agg.df_input.iterrows():
            loc = agg.satu(series)
            # print loc
            # loc is a dictionary
            df = haz.percent(loc)
            df['ASET'] = loc['ASET']
            df['SUBSEKTOR'] = loc['SUBSEKTOR']
            df['JUMLAH'] = loc['JUMLAH']
            df['KOEFISIEN'] = loc['KOEFISIEN']
            # df['DESCRIPTION'] = loc['DESCRIPTION']
            data.append(df)

        df_return = pd.concat(data)
        # print df_return.head()

        group = ([
            'KELAS_DAMPAK',
            'KOTA',
            'KECAMATAN',
            'KELURAHAN',
            'ASET',
            'SUBSEKTOR',
            'KOEFISIEN',
            # 'DESCRIPTION'
        ])
        df_per = df_return.groupby(group)['PERCENTAGE'].sum()
        df_jum = df_return.groupby(group)['JUMLAH'].mean()
        df_return = pd.concat([df_per, df_jum], axis=1)
        df_return.reset_index(inplace=True)
        df_return['JUMLAH_ASET'] = np.ceil(df_return['PERCENTAGE'] * df_return['JUMLAH'])
        df_return['PROVINSI'] = 'DKI JAKARTA'
        df_return.drop(['PERCENTAGE', 'JUMLAH'], inplace=True, axis=1)

        new_order = ([
            'PROVINSI',
            'KOTA',
            'KECAMATAN',
            'KELURAHAN',
            'SUBSEKTOR',
            'ASET',
            'KELAS_DAMPAK',
            'JUMLAH_ASET',
            'KOEFISIEN',
            # 'DESCRIPTION'
        ])

        df_return = df_return.reindex_axis(new_order, axis=1)
        # print df_return.tail()

        return df_return

    def analyze(self):

        """
        Analisa postprocessing
        """

        logger.info('PostProc.analyze')

        # directory
        shape_impact_dir = self.path.shp_impact_dir
        summary_dir = self.path.summary_dir
        shape_hazard_dir = self.path.shp_hazard_dir

        # raise error if no hazard folder generated
        if not os.path.isdir(shape_hazard_dir):
            print shape_hazard_dir
            raise NoHazardGeneratedDirError

        # necessary files
        # input files
        impact_shp_building = shape_impact_dir + \
            self.time_0 + '_' + self.time_1 + '_impact_building.shp'
        impact_shp_road = shape_impact_dir + \
            self.time_0 + '_' + self.time_1 + '_impact_roads.shp'
        impact_shp_train = shape_impact_dir + \
            self.time_0 + '_' + self.time_1 + '_impact_train.shp'
        hazard_shp = shape_hazard_dir + \
            self.time_0 + '_' + self.time_1 + '_hazard.shp'

        # raise error if no file exists
        if not os.path.isfile(impact_shp_building):
            print impact_shp_building
            raise NoImpactBuildingError
        if not os.path.isfile(impact_shp_road):
            print impact_shp_road
            raise NoImpactRoadError
        if not os.path.isfile(hazard_shp):
            print hazard_shp
            raise NoHazardGeneratedFileError

        # result files
        osm_file = summary_dir + 'osm_impact.csv'
        road_file = summary_dir + 'osm_road_impact.csv'
        agg_file = summary_dir + 'agg_impact.csv'

        # dataframe
        df_building = self.building(impact_shp_building)
        df_road = self.road(impact_shp_road)
        try:
            df_agg = self.aggregate(hazard_shp)
        except NoAggregateFileError:
            logger.error('No Aggregate file')
            sys.exit(1)

        try:
            fho = open(osm_file, 'w')
            fha = open(agg_file, 'w')
            fhr = open(road_file, 'w')
        except IOError, e:
            os.makedirs(summary_dir)
            fho = open(osm_file, 'w')
            fha = open(agg_file, 'w')
            fhr = open(road_file, 'w')

        # save to csv
        df_building.to_csv(fho, index=False)
        df_road.to_csv(fhr, index=False)
        df_agg.to_csv(fha, index=False)

        # close file handler
        fho.close()
        fha.close()
        fhr.close()

################################################################################
