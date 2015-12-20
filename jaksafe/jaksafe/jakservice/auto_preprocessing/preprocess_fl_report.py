__AUTHOR__= 'FARIZA DIAN PRASETYO'

from jaksafe import *

import simplejson as json
import pandas as pd
import numpy as np
import pandas.io.sql as psql

import Time as t
import os
from header_config_variable import *

from Time import formatted_date_to_timestamp
from Time import timestamp_to_formatted_date
from Time import timestamp_to_date_time

'''
Convert from json format to data frame
'''
def convert_json_to_data_frame(dims_json,request_time):

    dims_data_dict = json.loads(dims_json)
    df_event = pd.DataFrame.from_dict(dims_data_dict)
    print "df_event from dims"
    print df_event

    dims_column_order = [header_id_distrik,header_kelurahan,header_kecamatan,header_RW,header_RT,header_ketinggian,header_waktu_kejadian]
    fl_event_column_order = [header_id_unit,header_village,header_district,header_rw,header_rt,header_depth,header_report_time]

    ## Adapting the df to database
    for idx,col_name in enumerate(dims_column_order):
        df_event.rename(columns={col_name:fl_event_column_order[idx]},inplace = True)

    ## Adapting the df to database
    df_event[header_request_time] = request_time

    ## Changing data type as float
    df_event_max = df_event

    if not df_event.empty:
        df_event[[header_depth]] = df_event[[header_depth]].astype(float)
        grb = df_event.groupby(header_id_unit)
        df_event_max = grb.aggregate(np.max)
        df_event_max[header_id_unit] = df_event_max.index
        df_event_max['id'] = range(len(df_event_max))
        df_event_max = df_event_max.set_index('id')
        df_event_max.index.name = None

    return df_event,df_event_max

def convert_json_to_data_frame_update(dims_json,request_time):

    ### initialize status df_event and df_event_raw
    df_event = pd.DataFrame()
    df_event_max = df_event

    dims_data_dict = json.loads(dims_json)
    df_event = pd.DataFrame.from_dict(dims_data_dict[header_dims_reports])

    ### For the case if empty reports is fetched
    if df_event.empty:
        print 'empty reports (dict) from dims...'
        return df_event,df_event_max

    print "Get df_event from dims"

    df_event = df_event[df_event[header_id_distrik] != 'null']
    df_event = df_event[df_event[header_ketinggian] != 0]

    ### Empty data frame means no data flood reported    
    if df_event.empty:
        df_event_max = df_event
        return df_event,df_event_max

    dims_time_format = '%Y-%m-%dT%H:%M'
    ## Convert to time_series dataframe
    df_event[header_waktu_kejadian] = df_event.apply(lambda row: convert_dims_to_jaksafe_datetime(row[header_tanggal_kejadian],dims_time_format),axis = 1)

    ## Then filtering the time series with t0 and t1 
    datetime_t1 = convert_dims_to_jaksafe_datetime(request_time,std_time_format)
    df_event = df_event[df_event[header_waktu_kejadian] <= datetime_t1]

    ## drop useless column
    df_event = df_event.drop('TANGGAL_SELESAI_KEJADIAN',1)
    df_event = df_event.drop(header_tanggal_kejadian,1)
    df_event = df_event.drop(header_kodya,1)


    dims_column_order = [header_id_distrik,header_kecamatan,header_kelurahan,header_ketinggian,header_rw,header_rt,header_waktu_kejadian]
    fl_event_column_order = [header_id_unit,header_district,header_village,header_depth,header_rw,header_rt,header_report_time]

     ## Adapting the df to database
    for idx,col_name in enumerate(dims_column_order):
        df_event.rename(columns={col_name:fl_event_column_order[idx]},inplace = True)

    df_event[header_request_time] = datetime_t1

    ## Changing data type as float
    df_event_max = df_event

    if not df_event.empty:
        df_event[[header_depth]] = df_event[[header_depth]].astype(float)
        grb = df_event.groupby(header_id_unit)

        df_event_max = grb.aggregate(np.max)
        df_event_max[header_id_unit] = df_event_max.index
        df_event_max['id'] = range(len(df_event_max))
        df_event_max = df_event_max.set_index('id')
        df_event_max.index.name = None
    

    return df_event,df_event_max


def insert_dims_dataframe_to_database(df_event_dims_raw,df_event_dims,table_raw_name_event,table_name_event,db_con):
    print "Inserting data from dims to fl_database ...."
    df_event_dims.to_sql(con=db_con, name = table_name_event, if_exists='append', flavor='mysql', index = False)
    df_event_dims_raw.to_sql(con=db_con, name = table_raw_name_event, if_exists='append', flavor='mysql', index = False)

def get_latest_fl_event(db_con,table_name,t_now,event_duration):
    ## Default event_duration = 2 days
    print 'get latest fl event... (max 2 days)'    
    if event_duration < 1 or event_duration > 3:
        event_duration = 2

    event_duration = (event_duration * 24 * 3600)
    ta = t.Time(t_now.timeStamp()-event_duration)
    sql_dump = "SELECT * FROM %s WHERE request_time <= '%s' and request_time >= '%s'"%(table_name,t_now.formattedTime(),ta.formattedTime())
    print sql_dump
    df = psql.read_frame(sql_dump, db_con, index_col = 'id')
    return df

def get_fl_event(db_con,table_name,t0,t1):
    ## Creating sql dump
    sql_dump = "SELECT * FROM %s WHERE request_time <= '%s' and request_time >= '%s'"%(table_name,t1,t0)
    df = psql.read_frame(sql_dump, db_con, index_col = 'id')
    return df

def preprocessing_the_hazard_data(df_units):
    requested_times = pd.Series(df_units[header_request_time].values).unique()
    df_unit_list = []

    for f in requested_times:
        df_each = df_units[df_units[header_request_time] == f]
        df_each_rw,df_each_rt = split_to_rt_rw(df_each)
      
        if df_each_rt.empty:
            pass
        else:
            df_each_rt['is_overlapped'] = df_each_rt.apply(lambda row: check_overlapped_rt_on_rw(row[header_id_unit],df_each_rw), axis = 1)

            ## Remove the overlapped
            df_each_rt = df_each_rt[df_each_rt['is_overlapped'] == False]
            df_each_rt = df_each_rt.drop('is_overlapped',1)
            df_each = pd.concat([df_each_rw,df_each_rt])

        df_unit_list.append(df_each)

    df_units = pd.concat(df_unit_list)
    return df_units

def split_to_rt_rw(df_units):
    ## Get unit rw  
    df_units_rw = df_units[df_units[header_rt]==""]
    ## Get unit rt
    df_units_rt = df_units[df_units[header_rt]!=""]
    return df_units_rw,df_units_rt

def check_overlapped_rt_on_rw(id_rt,df_event_rw):
    id_rt = str(id_rt)
    id_rw_base = id_rt[:13] + '000'
    id_rw_values = map(str,df_event_rw[header_id_unit].values)
    
    if id_rw_base in id_rw_values:
        return True

    return False

def create_fl_report(df_units,t1,report_RT,report_RW,output_folder):
    folder_format = glob_folder_format
    t_1 = t1
    t1.set_time_format(folder_format)
   
    report_dir_name = 'fl_report'
    
    report_dir = output_folder+'/'+report_dir_name+'/'+t_1.formattedTime()

    if not os.path.exists(report_dir):
      os.makedirs(report_dir)
    
    df_rw,df_rt = split_to_rt_rw(df_units)
    df_rw = df_rw.drop(header_rt,1)
    
    ## Creating RW report
    rw_report_file = report_dir + "/" + t_1.formattedTime() + '_' + report_RW
    df_rw.to_csv(rw_report_file,sep=',',index=False)

    ## Creating RT report
    rw_report_file = report_dir + "/" + t_1.formattedTime() + '_' + report_RT
    df_rt.to_csv(rw_report_file,sep=',',index=False)


def create_summary_fl_report(df_units,t0,t1,report_summary,report_RT,report_RW,output_folder):
    folder_format = glob_folder_format
    t_0 = t0
    t_1 = t1

    t0.set_time_format(folder_format)
    t1.set_time_format(folder_format)
   
    report_dir_name = 'report'    
    report_dir = output_folder+'/'+ report_dir_name + '/'+ t_0.formattedTime() + '_' + t_1.formattedTime()

    if not os.path.exists(report_dir):
      os.makedirs(report_dir)
    
    df_rw,df_rt = split_to_rt_rw(df_units)
    df_rw = df_rw.drop(header_rt,1)
    
    ## Creating RW report
    rw_report_file = report_dir + "/" + t_0.formattedTime() + '_' + t_1.formattedTime() + '_' + report_RW
    df_rw.to_csv(rw_report_file,sep=',',index=False)

    ## Creating RT report
    rt_report_file = report_dir + "/" + t_0.formattedTime() + '_' + t_1.formattedTime() + '_' + report_RT
    df_rt.to_csv(rt_report_file,sep=',',index=False)

    ## Creating all summary report
    summary_report_file = report_dir + "/" + t_0.formattedTime() + '_' + t_1.formattedTime() + '_' + report_summary
    df_units.to_csv(summary_report_file,sep=',',index=False)

def convert_dims_to_jaksafe_datetime(inputTime,time_format):
    timestamp = formatted_date_to_timestamp(inputTime,time_format)
    datetime = timestamp_to_date_time(timestamp)
    return datetime
