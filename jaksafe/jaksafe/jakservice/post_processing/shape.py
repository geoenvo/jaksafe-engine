__AUTHOR__ = 'Abdul Somat Budiaji'

import logging
import os

import qgis.core as qcore
import pandas as pd

from error import *

logger = logging.getLogger('jakservice.post_processing.shape')

class Shape():

    """
    Kelas untuk pengelolaan shapefile
    """

    def __init__(self, shapefile):

        """
        Inisiasi kelas Shape
        """

        # set up qgis in order to work
        qcore.QgsApplication.setPrefixPath("/usr", True)
        qcore.QgsApplication.initQgis()

        self.shapefile = shapefile
        self.layer_name = os.path.basename(self.shapefile)
        self.layer = qcore.QgsVectorLayer(self.shapefile, self.layer_name, 'ogr')

    def get_features(self, request=None):

        """
        Mendapatkan fitur dari layer
        """

        logger.info('Shape.get_features')

        if request == None:
            # get all features
            return self.layer.getFeatures()

        # to do
        # else implementation with request

    def get_dataframe(self, *args):

        """
        Mendapatkan dataframe dari layer features

        :params args: Kolom dari data yang ada di shapefile
        """

        logger.info('Shape.get_dataframe')

        if len(args) == 0:
            raise NoColumnSpecifiedError

        data = {}

        for head in args:
            data[head] = []
            for f in self.layer.getFeatures():
                try:
                    data[head].append(f[head])
                except KeyError, e:
                    raise NoColumnSpecifiedError

        df = pd.DataFrame(data)
        # make dataframe column order as input args
        df = df[list(args)]

        return df
