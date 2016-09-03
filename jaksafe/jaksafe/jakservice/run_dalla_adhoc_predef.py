#run dala adhoc predefine :
# process the uploaded file

from main_dalla_adhoc_predef import initialize_adhoc_predef_summary
from main_dalla_adhoc_predef import insert_hazard_summary
from main_dalla_adhoc_predef import update_adhoc_predef_summary_table
from impact_analysis.hazard_compilation_function import inserting_table_dala_predef_result
from impact_analysis.hazard_compilation_function import dump_to_csv_table_adhoc_predef_dala_result
from config_folder import input_sql_folder
from config_folder import adhoc_output_folder

from header_config_variable import std_time_format

from jaksafe import db_con
from jaksafe import psql_db_con
from jaksafe import psql_engine
from jaksafe import global_conf_parser

import Time as t
import datetime
import sys

import sys, getopt

# import post processing
import logging
import post_processing.config as config_post
#import post_processing.adhoc as adhoc_post

# Package QGIS
#from qgis.core import *
#import qgis.utils
import sys
import os

## Get adhoc table name
table_name_adhoc_calc = global_conf_parser.get('database_configuration','table_name_adhoc_predef_calc')

#t0=''
#t1=''

if __name__ == '__main__':

    try:
        myopts, args = getopt.getopt(sys.argv[1:],"n:u:g:t:")
        print myopts

    except getopt.GetoptError as e:
        print (str(e))
        print("Usage parameter: %s -n event_name -u id_user -g id_group -t temp_tblname" % sys.argv[0])
        sys.exit(1)

    for o, a in myopts:
        if o == '-n':
            event_name = a

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

        elif o == '-t':
            if a == 'None':
                a = None
            else :
                a = str(a)
            temp_tblname = a
    try:
        
        print "event name : %s"%(event_name)
        print "Id user : %s"%(id_adhoc_user)
        print "Id group : %s"%(id_adhoc_group)


        ### Initialize adhoc summary at mysql database
        #last_summary_id = initialize_adhoc_summary(t0,t1,db_con,table_name_adhoc_calc)
		#insert ke mysql table
        event_id = initialize_adhoc_predef_summary(event_name,id_adhoc_user,id_adhoc_group,db_con,table_name_adhoc_calc)
        print 'event_id :'
        print event_id
        
        path = config_post.Path(str(id_adhoc_user), str(event_id), tipe='adhoc')
        
        if not os.path.isdir(path.log_dir):
            os.makedirs(path.log_dir)
        log_file = path.log_dir + 'dala_' + str(id_adhoc_user) + '_' + str(event_id) + '.log'
        print log_file
        logger = logging.getLogger('jakservice')
        logger.setLevel('INFO')
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        logger.info('AWAL PERHITUNGAN DALA ADHOC PREDEF')
        logger.info('AWAL IMPACT ANALYSIS')		
		##insert hazard ke table hazard summary
        last_row_hazard = insert_hazard_summary(event_id,psql_db_con,psql_engine,temp_tblname)
        print last_row_hazard
		
		#calculate dala
        inserting_table_dala_predef_result(event_id,psql_db_con,input_sql_folder)
		
		#update adhoc predef mysal
        print 'update adhoc'
        update_adhoc_predef_summary_table(event_id,db_con,psql_db_con,table_name_adhoc_calc)
		
		#dump report csv
        base_folder_output = adhoc_output_folder
        dump_to_csv_table_adhoc_predef_dala_result(event_id,psql_db_con,base_folder_output,id_adhoc_user)

        # Close all database connection
        db_con.close()
        psql_db_con.close()

        # Close QGIS service
        #QgsApplication.exitQgis()
        
        print "End of dalla service ...."
        logger.info('AKHIR IMPACT ANALYSIS')

    except Exception,e:
        print e
        logger.exception(e)
        sys.exit(1)
