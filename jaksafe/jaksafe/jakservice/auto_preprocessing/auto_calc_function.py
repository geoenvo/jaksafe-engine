__AUTHOR__= 'FARIZA DIAN PRASETYO'

from jaksafe import *

import simplejson as json
import pandas as pd
import numpy as np
import pandas.io.sql as psql

import Time as t
import os
from header_config_variable import *

def get_latest_report_status(db_con,table_name):
    sql_dump = "SELECT * FROM "+table_name+ \
           " ORDER BY id DESC LIMIT 1"
    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    data = cursor.fetchall()
    t0 = ''
    loss = 0
    if len(data) != 0:
        print 'ada data auto_calc'
        t0 =[row[1] for row in data]
        loss = [row[4] for row in data]
        t0 = str(t0[0])
        loss = loss[0]
        print loss
    else:
        print 'tidak ada data auto_calc'
        t0 = ''
    return t0,loss

def get_latest_t0_status(db_con,table_name,t0):
    sql_dump = "SELECT * FROM "+ table_name +" ORDER BY id DESC LIMIT 1"
    df = psql.read_frame(sql_dump, db_con)

    # This condition might be occured at first time running    
    if df.empty:
        print 'empty data frame..'
        return t0

    # Previous id_event = None, means there is no previous flood happened
    if (df.ix[0]['id_event'] == None):
        print 'No flood at previous time ... t0 is changing'
        return t0
        
    # Previous id_event != None, means there is flood at previous time   
    else:
        print 'There is flood at previous time ... t0 is not changing'
        t0 = str(df.ix[0]['t0'])
        t0_timestamp = t.formatted_date_to_timestamp(t0,psql_time_format)
        t0 = t.timestamp_to_formatted_date(t0_timestamp,std_time_format)
        return t0 
    
    

def create_summary_auto_calculation(t0,t1,db_con,table_name_autocalc,folder_output):    
    table_name = table_name_autocalc
    sql_dump = "INSERT INTO "+table_name+ \
               " (t0,t1,damage,loss) VALUES ('%s','%s',NULL,NULL)"%(t0,t1)

    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)    
    db_con.commit()
    last_row_id = cursor.lastrowid
    return last_row_id
    

def create_log_output(t0,t1,t0_s,t1_s,damage,loss,folder_output):
    t1_s.set_time_format(log_time_format)
    t0_s.set_time_format(log_time_format)
    
    t0 = t.Time(t0)
    t0.set_time_format(log_time_format)

    log_dir = folder_output + '/' + 'log'
    log_file_name = '/' + t1 + '_auto_calc_log.log'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = log_dir + log_file_name

    t1 = t.Time(t1)
    t1.set_time_format(log_time_format)

    print "Log file: %s"%log_file

    f_s = open(log_file,'w')
    f_s.write("Start service time: %s\n"%(t0_s.formattedTime()))
    f_s.write("End service time: %s\n"%(t1_s.formattedTime()))
    f_s.write("Start time for dalla: %s\n"%(t0.formattedTime()))
    f_s.write("End time for dalla: %s\n"%(t1.formattedTime()))
    f_s.write("Total damage: %.3f\n"%(damage))
    f_s.write("Total loss: %.3f\n"%(loss))
    f_s.close()

    
    
