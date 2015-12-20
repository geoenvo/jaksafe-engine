# coding = utf-8

import datetime
import logging

# import pre processing / impact analysis
from main_dalla_auto import main_impact_analysis_update
from main_dalla_auto import main_impact_analysis_dump_csv
from main_dalla_auto import update_auto_summary_table

from header_config_variable import std_time_format
from jaksafe import qgis_install_path

### import connection of postgresql
from jaksafe import psql_db_con
from jaksafe import psql_engine

### import connection of mysql
from jaksafe import db_con

from auto_preprocessing.auto_calc_function import *

import Time as t

# import post processing
import post_processing.config as config_post
import post_processing.run as run_post

# Package QGIS
from qgis.core import *
import qgis.utils
import sys
import os

table_name_autocalc = global_conf_parser.get('database_configuration','table_name_autocalc')


if __name__ == '__main__':

    ############################################################################
    # IMPACT ANALYSIS

    # Defining t1 and t0
    
    ## because cron is limited down to minute and we need to run to specific second, replace seconds with 59
    #t1 = datetime.datetime.strftime(datetime.datetime.now(),std_time_format)
    #t1 = t1[:-2] + '59'
    #t1 = t.Time(t1)
    
    ## uncomment next line to set manual t1 
    #t1 = t.Time('20150210115959')
    t1 = t.Time('20151116175959')

    t0 = t.Time(t1.timeStamp()-(6*3600))

    # Convert to formatted time
    t1 = t1.formattedTime()
    t0 = t0.formattedTime()

    # logging configuration
    time_0 = config_post.time_formatter(t0, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')
    time_1 = config_post.time_formatter(t1, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')

    path = config_post.Path(time_0, time_1)
    
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

    ## default damage and loss
    last_row_id = 0
    found_flood_events = False

    ## impact analysis module
    try:
        QgsApplication.setPrefixPath(qgis_install_path, True)
        QgsApplication.initQgis()

        id_event,t0_update,t1,damage,loss = main_impact_analysis_dump_csv(t0,t1,db_con,psql_db_con,psql_engine)
        t0 = t0_update
        
        ### Update auto summary table if hazard exists
        update_auto_summary_table(db_con,table_name_autocalc,id_event,t0,t1,damage,loss)

        
        ## reuse old log file and continue in new log file with updated t0
        ## remove old log file handler
        logger.removeHandler(fh)
        time_0 = config_post.time_formatter(t0, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')
        updated_log_file = path.log_dir + 'dala_' + time_0 + '_' + time_1 + '.log'

        ## rename old log file with updated t0
        os.rename(log_file, updated_log_file)
        fh = logging.FileHandler(updated_log_file)
        logger.addHandler(fh)
        fh.setFormatter(formatter)
        
    except Exception, e:
        print e
        logger.exception(e)
        sys.exit(1)

    except Exception,e:
        print e
        logger.exception(e)
        sys.exit(1)

    ### close the database postgresql and mysql
    db_con.close()
    psql_db_con.close()

    # Close QGIS service
    QgsApplication.exitQgis()

    print 'AKHIR IMPACT ANALYSIS'
    logger.info('AKHIR IMPACT ANALYSIS')

