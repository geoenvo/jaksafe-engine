import sys
import os
sys.path.append(os.path.abspath('..'))

import main_dalla_adhoc
from main_dalla_adhoc import main_adhoc_impact_analysis
from header_config_variable import std_time_format
from jaksafe import db_con
from auto_preprocessing.auto_calc_function import *

import Time as t
import datetime
import sys

import sys, getopt

# import post processing
import logging
import post_processing.config as config_post
import post_processing.adhoc as adhoc_post

# Package QGIS
from qgis.core import *
import qgis.utils

table_name_adhoccalc = global_conf_parser.get('database_configuration','table_name_adhoc_calc')
t0=''
t1=''

if __name__ == '__main__':

    ############################################################################
    # IMPACT ANALYSIS

    try:
        myopts, args = getopt.getopt(sys.argv[1:],"s:e:")
        print myopts
    except getopt.GetoptError as e:
        print (str(e))
        print("Usage parameter: %s -s start_time -e end_time" % sys.argv[0])
        sys.exit(1)

    for o, a in myopts:
        if o == '-s':
            t0=a
        elif o == '-e':
            t1=a
    try:
        QgsApplication.setPrefixPath(qgis_install_path, True)
        QgsApplication.initQgis()

        t0 = t.Time(str(t0))
        t1 = t.Time(str(t1))

        if t0.timeStamp() > t1.timeStamp():
            print "ERROR:date t0:%s is greater than date t1:%s"%(t0.formattedTime(),t1.formattedTime())
            sys.exit(1)


        print "Start time: %s"%(t0.formattedTime())
        print "Start time: %s"%(t1.formattedTime())

        t0 = t0.formattedTime()
        t1 = t1.formattedTime()

        time_0 = config_post.time_formatter(t0, '%y%m%d%H%M%S', '%Y%m%d%H%M%S')
        time_1 = config_post.time_formatter(t1, '%y%m%d%H%M%S', '%Y%m%d%H%M%S')

        path = config_post.Path(time_0, time_1, tipe='adhoc')
        if not os.path.isdir(path.log_dir):
            os.makedirs(path.log_dir)
        log_file = path.log_dir + 'dala_' + time_1 + '.log'

        logger = logging.getLogger('jaksafe_adhoc')
        logger.setLevel('INFO')
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        logger.info('AWAL PERHITUNGAN DALA')
        logger.info('AWAL IMPACT ANALYSIS')

        # print table_name_adhoccalc
        # last_row_id = main_dalla_adhoc.create_summary_auto_calculation(t0,t1,db_con,table_name_adhoccalc)
        # main_adhoc_impact_analysis(t0,t1,db_con)
        #
        # db_con.close()
        # print "End of dalla service ...."
        logger.info('AKHIR IMPACT ANALYSIS')

    except Exception,e:
        print "ERROR: %s"%e
        sys.exit(1)

    ############################################################################
    # POST PROCESSING
    # normalize time format
    t0 = config_post.time_formatter(t0, '%y%m%d%H%M%S', '%Y%m%d%H%M%S')
    t1 = config_post.time_formatter(t1, '%y%m%d%H%M%S', '%Y%m%d%H%M%S')

    # daftar subsektor
    o_list = config_post.ListSubsektor()
    list_subsektor = o_list.subsektor

    try:
        adhoc_post.main(t0, t1, list_subsektor, last_row_id)
        QgsApplication.exitQgis()
    except Exception, e:
        logger.exception(e)
        pass

    logger.info('AKHIR PERHITUNGAN DALA')
