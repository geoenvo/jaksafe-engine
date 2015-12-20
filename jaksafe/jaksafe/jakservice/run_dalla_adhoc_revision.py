import main_dalla_adhoc

from main_dalla_adhoc import main_adhoc_impact_analysis
from main_dalla_adhoc import main_adhoc_impact_analysis_dump_csv
from main_dalla_adhoc import create_summary_adhoc_calculation
from main_dalla_adhoc import initialize_adhoc_summary
from main_dalla_adhoc import update_adhoc_summary_table

from header_config_variable import std_time_format

from jaksafe import db_con
from jaksafe import psql_db_con
from jaksafe import psql_engine

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
import sys
import os

## Get adhoc table name
table_name_adhoc_calc = global_conf_parser.get('database_configuration','table_name_adhoc_calc')

#t0=''
#t1=''

if __name__ == '__main__':

    try:
        #myopts, args = getopt.getopt(sys.argv[1:],"s:e:")
        myopts, args = getopt.getopt(sys.argv[1:],"s:e:u:g:")
        print myopts

    except getopt.GetoptError as e:
        print (str(e))
        print("Usage parameter: %s -s start_time -e end_time -u id_user -g id_group" % sys.argv[0])
        sys.exit(1)

    for o, a in myopts:
        if o == '-s':
            t0 = a
       
        elif o == '-e':
            t1 = a

        elif o == '-u':
            if a == 'None':
                a = None
            else :
                a = int(a)
            id_adhoc_user = a

        elif o == '-g':
            if a == 'None':
                a = None
            else :
                a = int(a)
            id_adhoc_group = a

    try:
        QgsApplication.setPrefixPath(qgis_install_path, True)
        QgsApplication.initQgis()

        t0 = t.Time(str(t0))
        t1 = t.Time(str(t1))

        if t0.timeStamp() > t1.timeStamp():
            print "ERROR:date t0:%s is greater than date t1:%s"%(t0.formattedTime(),t1.formattedTime())
            sys.exit(1)


        print "Start time: %s"%(t0.formattedTime())
        print "End time: %s"%(t1.formattedTime())
        print "Id user : %s"%(id_adhoc_user)
        print "Id group : %s"%(id_adhoc_group)


        t0 = t0.formattedTime()
        t1 = t1.formattedTime()

        
        time_0 = config_post.time_formatter(t0, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')
        time_1 = config_post.time_formatter(t1, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')

        path = config_post.Path(time_0, time_1, tipe='adhoc')
        
        if not os.path.isdir(path.log_dir):
            os.makedirs(path.log_dir)
        log_file = path.log_dir + 'dala_' + time_0 + '_' + time_1 + '.log'

        logger = logging.getLogger('jakservice')
        logger.setLevel('INFO')
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        logger.info('AWAL PERHITUNGAN DALA')
        logger.info('AWAL IMPACT ANALYSIS')

        ### Initialize adhoc summary at mysql database
        #last_summary_id = initialize_adhoc_summary(t0,t1,db_con,table_name_adhoc_calc)
        last_summary_id = initialize_adhoc_summary(t0,t1,id_adhoc_user,id_adhoc_group,db_con,table_name_adhoc_calc)

        ### Starting to get the flood hazard
        is_hazard_empty,last_event_id = main_adhoc_impact_analysis_dump_csv(t0,\
                                                                            t1,\
                                                                            db_con,\
                                                                            psql_db_con,\
                                                                            psql_engine)
        ### Update adhoc summary table if hazard exists
        if (not is_hazard_empty):
            update_adhoc_summary_table(last_summary_id,last_event_id,db_con,table_name_adhoc_calc)


        # Close all database connection
        db_con.close()
        psql_db_con.close()

        # Close QGIS service
        QgsApplication.exitQgis()
        
        print "End of dalla service ...."
        logger.info('AKHIR IMPACT ANALYSIS')

    except Exception,e:
        print e
        logger.exception(e)
        sys.exit(1)
