# coding = utf-8

import datetime
import logging

# import pre processing / impact analysis
from main_dalla_auto import main_impact_analysis
from main_dalla_auto import main_impact_analysis_update
from header_config_variable import std_time_format
from jaksafe import db_con
from jaksafe import qgis_install_path
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

    # Set current time
    t0_s = datetime.datetime.strftime(datetime.datetime.now(),std_time_format)
    t0_s = t.Time(t0_s)

    # Defining t1 and t0
    
    ## because cron is limited down to minute and we need to run to specific second, replace seconds with 59
    t1 = datetime.datetime.strftime(datetime.datetime.now(),std_time_format)
    t1 = t1[:-2] + '59'
    t1 = t.Time(t1)
    
    ## uncomment next line to set manual t1
    # t1 = t.Time('20150424235959')
    
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
        # folder_output,t0_update = main_impact_analysis(t0,t1,db_con)
        folder_output,t0_update = main_impact_analysis_update(t0,t1,db_con)
        t0 = t0_update
        
        ## folder_output is False when no flood reports found in period (t1 - 2days)
        if folder_output != False:
            found_flood_events = True
        
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
        logger.exception(e)
        sys.exit(1)


    ## Creating and writing auto calculation summary
    try:
        t1_s = datetime.datetime.strftime(datetime.datetime.now(),std_time_format)
        t1_s = t.Time(t1_s)
        last_row_id = create_summary_auto_calculation(t0,t1,db_con,table_name_autocalc,folder_output)


        print "Last row id time = %d" % last_row_id

    except Exception,e:
        logger.exception(e)
        sys.exit(1)

    db_con.close()
    logger.info('AKHIR IMPACT ANALYSIS')

    ############################################################################
    # POST PROCESSING
    # normalize time format
    t0 = config_post.time_formatter(t0, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')
    t1 = config_post.time_formatter(t1, '%Y%m%d%H%M%S', '%Y%m%d%H%M%S')

    # daftar subsektor
    o_list = config_post.ListSubsektor()
    list_subsektor = o_list.subsektor

    try:
        run_post.main(t0, t1, list_subsektor, last_row_id, found_flood_events)
        QgsApplication.exitQgis()
    except Exception, e:
        logger.exception(e)

    logger.info('AKHIR PERHITUNGAN DALA')
