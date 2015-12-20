__AUTHOR__= 'FARIZA DIAN PRASETYO'

import requests
import json
import pandas as pd
import numpy as np
import pandas.io.sql as psql

from Time import Time
from Time import formatted_date_to_timestamp
from Time import timestamp_to_formatted_date
from Time import timestamp_to_date_time

from jaksafe import db_con
from jaksafe import global_conf_parser

from header_config_variable import *
from datetime import datetime

from Time import formatted_date_to_timestamp
from Time import timestamp_to_formatted_date

from auto_preprocessing.preprocess_fl_report import convert_dims_to_jaksafe_datetime
from auto_preprocessing.preprocess_fl_report import insert_dims_dataframe_to_database

## Time Format from DIMS
dims_format_time = '%Y%m%d%H'

#input from data dims and database configuration
base_dims_url = global_conf_parser.get('dims_conf','url_dims')
table_name_event = global_conf_parser.get('database_configuration','table_name_event')
table_raw_name_event = global_conf_parser.get('database_configuration','table_raw_name_event')


def get_fl_event_content(db_con,table_name):
    ## Creating sql dump
    sql_dump = "SELECT * FROM %s ORDER BY report_time DESC LIMIT 1"%(table_name)
    df = psql.read_frame(sql_dump, db_con, index_col = 'id')
    return df


def create_request_time(report_time):
    time_batch = ['05:59:59','11:59:59','17:59:59','23:59:59']
    t_dims = datetime.strptime(str(report_time), log_time_format)
    t_request_time = time_batch[(t_dims.hour // 6)]
    t_request_time = str(report_time).split(' ')[0]  + ' ' + t_request_time
    return t_request_time


def dimsdata_to_fl_dataframe(dims_json,timestamp_t0):
    dims_data_dict = json.loads(dims_json)
    df_event = pd.DataFrame.from_dict(dims_data_dict[header_dims_reports])

    print "df_event from dims"

    df_event = df_event[df_event[header_id_distrik] != 'null']
    df_event = df_event[df_event[header_ketinggian] != 0]

    print "Skipping ID_DISTRIK=>null and KETINGGIAN=>zero(0)"

    dims_time_format = '%Y-%m-%dT%H:%M'

    ## Convert to time_series dataframe
    df_event[header_waktu_kejadian] = df_event.apply(lambda row: convert_dims_to_jaksafe_datetime(row[header_tanggal_kejadian],dims_time_format),axis = 1)

    ## drop useless column
    df_event = df_event.drop('TANGGAL_SELESAI_KEJADIAN',1)
    df_event = df_event.drop(header_tanggal_kejadian,1)
    df_event = df_event.drop(header_kodya,1)

    dims_column_order = [header_id_distrik,header_kecamatan,header_kelurahan,header_ketinggian,header_rw,header_rt,header_waktu_kejadian]
    fl_event_column_order = [header_id_unit,header_district,header_village,header_depth,header_rw,header_rt,header_report_time]

     ## Adapting the df to database
    for idx,col_name in enumerate(dims_column_order):
        df_event.rename(columns={col_name:fl_event_column_order[idx]},inplace = True)
    df_event.sort([header_report_time],inplace = True)

    if df_event.empty:
        import sys
        print "Ooops there is No data from dims...!!!"
        print "System is exiting...."
        sys.exit(1)

    df_event[header_request_time] =  df_event.apply(lambda row: create_request_time(row[header_report_time]),axis = 1)

    t0 = timestamp_to_formatted_date(timestamp_t0,log_time_format)
    datetime_t0 = convert_dims_to_jaksafe_datetime(t0,log_time_format)     
    
    ## raw event will be written to fl_event_raw    
    df_event = df_event[df_event[header_report_time] > datetime_t0]

    ### Group by id and request time
    gr = df_event.groupby([header_request_time,header_id_unit],as_index=False)
    
    ## maximum event will be written to fl_event
    df_event_max = gr.aggregate(np.max)

    return df_event,df_event_max
    

def get_data_from_dims(timestamp_t0):
    t0 = timestamp_to_formatted_date(timestamp_t0,dims_format_time)
    print "Starting crawling data from dims ..."
    time_conf = 'fromTime=%s'%(t0)
    dims_url = base_dims_url+'?'+ time_conf
    print "url dims => %s"%(dims_url)
    response = requests.get(dims_url)
    if response.status_code != 200:
        print "DIMS Service is not available...."
        print "DALLA service is terminating ..."
        sys.exit(1)
    dims_data = response.content
    return dims_data


def main():
    print "Starting populating data dims..."

    ## Default t0   
    t0_default = '2001010100'
    timestamp_t0 = formatted_date_to_timestamp(t0_default,dims_format_time)

    ## Check fl_event
    print "Checking fl event from database..."
    df_last = get_fl_event_content(db_con,table_raw_name_event)
    print df_last
    if not df_last.empty:
        print "Database fl is not empty..."
        indexes = df_last.index.values
        t0_last = str(df_last.ix[indexes[0]][header_report_time])        
        timestamp_t0 = formatted_date_to_timestamp(t0_last,log_time_format)
        print "Found latest t0 => %s"%(t0_last)
    else:
        print "Database fl is empty..."
        print "t0 using default => %s"%(t0_default)

    dims_data = get_data_from_dims(timestamp_t0)
    df_event_dims_raw,df_event_dims = dimsdata_to_fl_dataframe(dims_data,timestamp_t0)

    ## Check fl_event
    try:
        insert_dims_dataframe_to_database(df_event_dims_raw,df_event_dims,table_raw_name_event,table_name_event,db_con)
    except Exception,e:
        print e
        sys.exit(1)

if __name__ == '__main__':
    main()
