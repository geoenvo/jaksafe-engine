__AUTHOR__= 'FARIZA DIAN PRASETYO'

from jaksafe import *

import pandas as pd
import pandas.io.sql as psql

import numpy as np
import os

from header_config_variable import *
import Time as t
import psycopg2


def compile_flood_event(df_all_units):
    df_compile = df_all_units[[header_id_unit,header_depth]]
    grb = df_compile.groupby(header_id_unit)
    df1 = grb.aggregate(np.mean).rename(columns = {header_depth:'mean_depth'})
    df1['mean_depth'] = df1['mean_depth']
    df1['count'] = grb.aggregate(len).rename(columns = {header_depth:'count'})
    df1['duration'] = (df1['count'] * 6)/24.
    return df1

def compiling_hazard_fl(df_all_units,hazard_config_file):
    df_compiled = compile_flood_event(df_all_units)
    df_compiled = mapping_compiled_data_to_hazard_class(df_compiled,hazard_config_file)
    df_compiled.to_csv('compiled_event.csv')
    return df_compiled

def compiling_hazard_fl_in_folder(df_all_units,hazard_config_file,base_folder_output,t0,t1):
    t1.set_time_format(glob_folder_format)
    t0.set_time_format(glob_folder_format)

    ## ## /output/hazard/20150210055959_20150210115959/
    output_directory = base_folder_output + '/hazard/' + t0.formattedTime() + '_' + t1.formattedTime() + '/'

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    df_compiled = compile_flood_event(df_all_units)
    df_compiled = mapping_compiled_data_to_hazard_class(df_compiled,hazard_config_file)
    df_compiled_report = df_compiled[['mean_depth','duration','kelas']]
    df_compiled_report.to_csv(output_directory + 'compiled_event.csv')
    
    return df_compiled

def mapping_compiled_data_to_hazard_class(df_compiled,hazard_class_file):
    df_config_hazard = pd.read_csv(hazard_class_file)
    df_compiled['kelas'] = df_compiled.apply(lambda row: classify_hazard_class(row['mean_depth'],row['duration'],df_config_hazard), axis = 1)
    return df_compiled

def classify_hazard_class(mean_depth,duration,df_config_hazard):
    kelas = None
    for idx,row in df_config_hazard.iterrows():
        if mean_depth >= row['kedalaman_bawah'] and mean_depth <= row['kedalaman_atas']:
            if duration >= row['durasi_bawah'] and duration <= row['durasi_atas']:
                kelas = row['kelas']
                break
    return kelas

def insert_fl_hazard_summary_event_to_postgresql_database(psql_db_con,\
                                                          psql_engine,\
                                                          t0,\
                                                          t1,\
                                                          df_fl_hazard,\
                                                          df_hazard_compile,\
                                                          event_type):    
    t0,t1 = set_input_time_to_psql_formated_time(t0,t1)
    insert_adhoc_event_table_at_psql_database(t0,t1,psql_db_con,psql_engine)
    insert_adhoc_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,df_fl_hazard,df_hazard_compile)


def insert_fl_hazard_summary_to_postgresql_database(psql_db_con,psql_engine,t0,t1,df_fl_hazard,df_hazard_compile):
    t0,t1 = set_input_time_to_psql_formated_time(t0,t1)
    insert_adhoc_event_table_at_psql_database(t0,t1,psql_db_con,psql_engine)
    insert_adhoc_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,df_fl_hazard,df_hazard_compile)

## Change time t0 and t1 to psql formated time
def set_input_time_to_psql_formated_time(t0,t1):
    obj_t0 = t.Time(t0)
    obj_t0.set_time_format(psql_time_format)
    obj_t1 = t.Time(t1)
    obj_t1.set_time_format(psql_time_format)
    return obj_t0.formattedTime(),obj_t1.formattedTime()


## inserting adhoc event table at postgresql
def insert_adhoc_event_table_at_psql_database(t0,t1,psql_db_con,psql_engine):
    try:     
        dict_adhoc_event_time = {'t0':t0,'t1':t1}
        df_input = pd.DataFrame([dict_adhoc_event_time])
        df_input.to_sql('adhoc_event', psql_engine,if_exists='append',index=False)   ## index -> False for auto increment

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e        
        if db_con:
            db_con.rollback()
        last_id_adhoc_event = df_last_adhoc_event.ix[0]['id_event']
        
        ### Prepare the hazard adhoc event data frame to be inserted to database
        df_adhoc_hazard_event = df_fl_hazard[['unit','depth','report_time','request_time']]
        df_adhoc_hazard_event['id_event'] = last_id_adhoc_event
        df_adhoc_hazard_event = df_adhoc_hazard_event[['id_event','unit','depth','report_time','request_time']]
        df_adhoc_hazard_event.columns = ['id_event','id_unit','kedalaman','report_time','request_time']

        ### Insert to database
        print df_adhoc_hazard_event
        df_adhoc_hazard_event.to_sql('adhoc_hazard_event',psql_engine,if_exists='append',index=False)

        ### Prepare the hazard adhoc summary frame to be inserted to database
        df_hazard_compile.reset_index(inplace=True)
        df_fl_hazard.reset_index(inplace=True)
        df_fl_hazard = df_fl_hazard.drop_duplicates(subset='unit',take_last = True)
        df_district_detail = df_fl_hazard[['unit','village','district','rt','rw']]       
        df_merge_adhoc_summary = pd.merge(df_hazard_compile, df_district_detail, how='left', on=['unit'])
        df_adhoc_summary = df_merge_adhoc_summary[['unit','village','district','rt','rw','mean_depth','duration','kelas']]
        df_adhoc_summary['id_event'] = last_id_adhoc_event
        df_adhoc_summary = df_adhoc_summary[['id_event','unit','village','district',\
                                             'rt','rw','mean_depth','duration','kelas']]
        df_adhoc_summary.columns = ['id_event','id_unit','kelurahan',\
                                    'kecamatan','rt','rw','kedalaman_rata_rata',\
                                    'durasi_rendaman','kelas']
        ### Insert to database
        print df_adhoc_summary
        df_adhoc_summary.to_sql('adhoc_hazard_summary',psql_engine,if_exists='append',index=False)

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e        
        if psql_db_con:
            psql_db_con.rollback()
        sys.exit(1)

    except Exception,e:
        print e
        sys.exit(1)
        sys.exit(1)

def insert_adhoc_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,df_fl_hazard,df_hazard_compile):   
    try:
        ### Get last id event index from adhoc_event_table    
        df_last_adhoc_event = psql.read_sql("SELECT id_event FROM adhoc_event order by id_event DESC LIMIT 1",psql_db_con)
