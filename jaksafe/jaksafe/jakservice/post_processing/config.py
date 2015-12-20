# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import ConfigParser
import datetime
import os
import sys
import time

conf = ConfigParser.SafeConfigParser()
global_conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../global_conf.cfg')
conf.read(global_conf_file)
project_dir = conf.get('folder_conf', 'project_folder')
subsektor_dir = conf.get('directory', 'subsektor')
sys.path.append(subsektor_dir)

from error import *

import subsektor

################################################################################

class Subsektor(object):

    """
    Antarmuka untuk berhubungan dengan subsektor.py
    """

    def __init__(self):
        pass

    def get_subsektor(self, **kwargs):

        """
        Mendapatkan jenis subsektor dari aset tertentu

        :param kwargs: kunci argumen yang valid hanya aset
        """

        for k in kwargs:
            if not k == 'aset':
                raise InvalidArgumentError

        return subsektor.ASET[kwargs['aset']]['SUBSEKTOR']

    def get_sektor(self, **kwargs):

        """
        Mendapatkan jenis sektor

        :param kwargs: kunci argument yang valid hanya aset dan subsektor
        """

        # for k in kwargs:
        #     if not k == 'aset':
        #         raise InvalidArgumentError

        if 'aset' in kwargs.keys():
            return subsektor.ASET[kwargs['aset']]['SEKTOR']
        elif 'subsektor' in kwargs.keys():
            return subsektor.ASET[kwargs['subsektor']]['SEKTOR']

    def get_hazard(self, aset):

        """
        Mendapatkan status apakah perhitungan dala untuk aset tersebut
        menggunakan shapefile hazard atau tidak
        """

        return subsektor.ASET[aset]['HAZARD']

    def get_impact(self, aset):

        """
        Mendapatkan nama file impact yang digunakan untuk perhitungan dala
        """

        return subsektor.ASET[aset]['IMPACT']

    def get_dala(self, aset):

        """
        Mendapatkan jenis perhitungan dala
        """

        return subsektor.ASET[aset]['DALA']

    def get_list_aset(self, subs):

        """
        Mendapatkan list aset dari sebuah subsektor
        """

        subs_list = []
        for s_key, s_val in subsektor.ASET.items():
            if s_val['SUBSEKTOR'] == subs:
                subs_list.append(s_val['ASET'])

        return subs_list

################################################################################

class Path(object):

    """
    Antarmuka config untuk filesystem
    """

    def __init__(self, time_0, time_1, tipe='auto'):

        """
        Inisiasi kelas Path
        """

        self.time_0 = time_0
        self.time_1 = time_1

        # input dir
        self.assumption_dir = conf.get('directory', 'assumption')
        self.aggregate_dir = conf.get('directory', 'aggregate')

        # output dir
        if tipe=='auto':
            # log dir
            self.log_dir = conf.get('directory', 'log')
            self.resource_dir = conf.get('directory', 'resource')

            self.impact_dir = conf.get('directory', 'impact') + \
                self.time_0 + '_' + self.time_1 + '/'
            self.output_dir = conf.get('directory', 'report') + \
                self.time_0 + '_' + self.time_1 + '/'
            self.shp_impact_dir = conf.get('directory', 'impact') + \
                self.time_0 + '_' + self.time_1 + '/shapefile/'
            self.shp_hazard_dir = conf.get('directory', 'hazard') + \
                self.time_0 + '_' + self.time_1 + '/'
            self.summary_dir = conf.get('directory', 'impact') + \
                self.time_0 + '_' + self.time_1 + '/summary/'
        elif tipe=='adhoc':
            # log dir
            self.log_dir = conf.get('directory', 'log_adhoc')
            self.resource_dir = conf.get('directory', 'resource')

            self.impact_dir = conf.get('directory', 'impact_adhoc') + \
                self.time_0 + '_' + self.time_1 + '/'
            self.output_dir = conf.get('directory', 'report_adhoc') + \
                self.time_0 + '_' + self.time_1 + '/'
            self.shp_impact_dir = conf.get('directory', 'impact_adhoc') + \
                self.time_0 + '_' + self.time_1 + '/shapefile/'
            self.shp_hazard_dir = conf.get('directory', 'hazard_adhoc') + \
                self.time_0 + '_' + self.time_1 + '/'
            self.summary_dir = conf.get('directory', 'impact_adhoc') + \
                self.time_0 + '_' + self.time_1 + '/summary/'

################################################################################

class Database(object):

    """
    Antarmuka config untuk database
    """

    def __init__(self):

        """
        Inisiasi kelas Database
        """

        self.params_con = {
            'host' : conf.get('database_configuration', 'url_address'),
            'user' : conf.get('database_configuration', 'user'),
            'passwd' : conf.get('database_configuration', 'paswd'),
            'db' : conf.get('database_configuration', 'database_name'),
            'port' : int(conf.get('database_configuration', 'port'))
        }

################################################################################

def time_formatter(time_input, format_input, format_output):

    """
    Mengubah format waktu dari satu format ke format lainnya
    """

    time_rep = int(time.mktime(datetime.datetime.strptime(time_input, format_input).timetuple()))
    time_res = datetime.datetime.fromtimestamp(time_rep).strftime(format_output)

    return time_res

################################################################################

class ListSubsektor(object):

    """
    Antar muka untuk berhubungan dengan daftar subsektor yang akan digunakan
    untuk perhitungan
    """

    def __init__(self):
        self.subsektor = conf.get('subsektor', 'subsektor').split(',')

################################################################################
