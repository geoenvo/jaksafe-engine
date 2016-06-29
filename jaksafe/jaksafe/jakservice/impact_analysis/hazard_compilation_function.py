__AUTHOR__= 'FARIZA DIAN PRASETYO'

from jaksafe import *

import pandas as pd
import pandas.io.sql as psql

import numpy as np
import os
import zipfile
import shutil

from header_config_variable import *
import Time as t
import psycopg2

import os.path
import subprocess
import sys
from os.path import basename

gisserver='45.118.135.27'

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
    df_compiled = compile_flood_event(df_all_units)
    df_compiled = mapping_compiled_data_to_hazard_class(df_compiled,hazard_config_file)
    return df_compiled

def dump_all_hazard_to_csv(df_all_hazard,base_folder_output,t0,t1):
    t1.set_time_format(glob_folder_format)
    t0.set_time_format(glob_folder_format)

    output_directory = base_folder_output + '/report/' + t0.formattedTime() + '_' + t1.formattedTime() + '/'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    df_all_hazard = df_all_hazard[['id_unit','kelurahan','kecamatan','rt','rw','kedalaman_rata_rata',\
                                   'durasi_rendaman','kelas']]

    filename = t0.formattedTime() + '_' + t1.formattedTime() + '_' + 'hazard_summary.csv'
    df_all_hazard.to_csv((output_directory + filename),index=True)


#### For zip the file ########
def create_zip_file(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            #print 'zipping %s as %s' % (os.path.join(dirname, filename),
            #                            arcname)
            zf.write(absname, arcname)
    zf.close()

def create_zip_of_summary_and_shp(base_folder_output,t0,t1):
    t1.set_time_format(glob_folder_format)
    t0.set_time_format(glob_folder_format)
    output_directory = base_folder_output + '/report/' + t0.formattedTime() + '_' + t1.formattedTime() + '/'

    ### example shapefile_20140101000000_20141231235959.zip    
    zip_filename = 'shapefile' + '_' + t0.formattedTime() + '_' + t1.formattedTime()
    base_zip_filename = base_folder_output + '/report/' + zip_filename

    create_zip_file(output_directory, base_zip_filename)
    #shutil.move((base_folder_output + '/report/' + "%s.zip"%(base_zip_filename)),\
     #           (output_directory + "%s.zip"%(base_zip_filename)))
    shutil.move(("%s.zip"%(base_zip_filename)),(output_directory + "%s.zip"%(zip_filename)))


def updatestyle(layername):
    cmd = 'curl -v -u admin:geoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>'+'Kategori_Banjir'+'</name><workspace>geonode</workspace></defaultStyle></layer>" http://'+gisserver+'/geoserver/rest/layers/geonode:'+layername
    subprocess.call(cmd, shell=True)
    #print cmd
	
def sendlayer(zipfile,shapefile):
    cmd = 'curl -v -u admin:geoserver -XPUT -H "Content-type: application/zip" --data-binary @'+zipfile+' http://'+gisserver+':8080/geoserver/rest/workspaces/geonode/datastores/datastore/file.shp'
    subprocess.call(cmd, shell=True)
    #print cmd

def send_shapefile_to_geonode(zip_file_name,shapefile_layer_name):
    shp_file = shapefile_layer_name + '.shp'
    print zip_file_name    
    print shp_file
    print shapefile_layer_name    
    
    print 'send layer to geonode ....'
    sendlayer(zip_file_name,shp_file)
    
    print 'updating style geonode ....'
    updatestyle(shapefile_layer_name)

def create_zip_of_shp(base_folder_output,t0,t1):
    import glob
    t1.set_time_format(glob_folder_format)
    t0.set_time_format(glob_folder_format)
    output_directory = base_folder_output + '/report/' + t0.formattedTime() + '_' + t1.formattedTime() + '/'
    hazard_base_name = t0.formattedTime() + '_' + t1.formattedTime() + '_' + 'hazard.*'
    all_hazard_files = glob.glob((output_directory + hazard_base_name))
    
    zip_file_name = output_directory + t0.formattedTime() + '_' + t1.formattedTime() + '_' + 'hazard_shapefile.zip'
    shapefile_layer_name = t0.formattedTime() + '_' + t1.formattedTime() + '_' + 'hazard'

    
    with zipfile.ZipFile(zip_file_name, 'w',zipfile.ZIP_DEFLATED) as myzip:
        for hazard_file in all_hazard_files:
            filename, file_extension = os.path.splitext(hazard_file)
            if (file_extension == '.qpj' or file_extension == '.cpg'):
                continue;
            myzip.write(hazard_file,basename(hazard_file))                
        myzip.close()

    ### send to geo node
    #send_shapefile_to_geonode(zip_file_name,shapefile_layer_name)

def dump_to_csv_table_auto_dala_result(id_auto_event,psql_db_con,base_folder_output,t0,t1):
    t1.set_time_format(glob_folder_format)
    t0.set_time_format(glob_folder_format)

    output_directory = base_folder_output + '/report/' + t0.formattedTime() + '_' + t1.formattedTime()
    this_filename = t0.formattedTime() + '_' + t1.formattedTime() + '_' + 'auto_dala_result.csv'    
    
    auto_dala_result_filename = output_directory + '/' + this_filename
    
    sql_query = "SELECT * FROM auto_dala_result WHERE id_event = %s order by sector,subsector,asset"%(id_auto_event)
    df_auto_dala_result = psql.read_sql(sql_query,psql_db_con)
    df_auto_dala_result.to_csv(auto_dala_result_filename,index=False)


def dump_to_csv_table_adhoc_dala_result(id_adhoc_event,psql_db_con,base_folder_output,t0,t1):
    t1.set_time_format(glob_folder_format)
    t0.set_time_format(glob_folder_format)

    output_directory = base_folder_output + '/report/' + t0.formattedTime() + '_' + t1.formattedTime()
    this_filename = t0.formattedTime() + '_' + t1.formattedTime() + '_' + 'adhoc_dala_result.csv'    
    
    adhoc_dala_result_filename = output_directory + '/' + this_filename
    
    sql_query = "SELECT * FROM adhoc_dala_result WHERE id_event = %s order by sector,subsector,asset"%(id_adhoc_event)
    df_adhoc_dala_result = psql.read_sql(sql_query,psql_db_con)
    df_adhoc_dala_result.to_csv(adhoc_dala_result_filename,index=False)


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


### For adhoc table ##################
def insert_fl_hazard_summary_to_postgresql_database(psql_db_con,psql_engine,input_sql_folder,\
                                                    t0,t1,df_fl_hazard,df_hazard_compile):

    t0,t1 = set_input_time_to_psql_formated_time(t0,t1)
    insert_adhoc_event_table_at_psql_database(t0,t1,psql_db_con,psql_engine)
    last_id_ev = insert_adhoc_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,input_sql_folder,\
                                                df_fl_hazard,df_hazard_compile)
    return last_id_ev

### For auto table ##################
def insert_fl_hazard_summary_to_postgresql_database_auto(psql_db_con,psql_engine,input_sql_folder,\
                                                    t0,t1,df_fl_hazard,df_hazard_compile):

    t0,t1 = set_input_time_to_psql_formated_time(t0,t1)
    insert_auto_event_table_at_psql_database(t0,t1,psql_db_con,psql_engine)
    last_id_ev = insert_auto_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,input_sql_folder,\
                                                df_fl_hazard,df_hazard_compile)
    return last_id_ev

## Change time t0 and t1 to psql formated time
def set_input_time_to_psql_formated_time(t0,t1):
    obj_t0 = t.Time(t0)
    obj_t0.set_time_format(psql_time_format)
    obj_t1 = t.Time(t1)
    obj_t1.set_time_format(psql_time_format)
    return obj_t0.formattedTime(),obj_t1.formattedTime()


## inserting auto event table at postgresql
def insert_auto_event_table_at_psql_database(t0,t1,psql_db_con,psql_engine):
    try:     
        dict_auto_event_time = {'t0':t0,'t1':t1}
        df_input = pd.DataFrame([dict_auto_event_time])
        df_input.to_sql('auto_event', psql_engine,if_exists='append',index=False)   ## index -> False for auto increment

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e        
        if db_con:
            db_con.rollback()
        sys.exit(1)


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
        sys.exit(1)

def insert_adhoc_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,input_sql_folder,\
                                                df_fl_hazard,df_hazard_compile):
    try:
        ### Get last id event index from adhoc_event_table    
        df_last_adhoc_event = psql.read_sql("SELECT id_event FROM adhoc_event order by id_event DESC LIMIT 1",psql_db_con)
        last_id_adhoc_event = df_last_adhoc_event.ix[0]['id_event']
        
        ### Prepare the hazard adhoc event data frame to be inserted to database
        df_adhoc_hazard_event = df_fl_hazard[['unit','depth','report_time','request_time']]
        df_adhoc_hazard_event['id_event'] = last_id_adhoc_event
        df_adhoc_hazard_event = df_adhoc_hazard_event[['id_event','unit','depth','report_time','request_time']]
        df_adhoc_hazard_event.columns = ['id_event','id_unit','kedalaman','report_time','request_time']

        ### convert id_event to integer
        df_adhoc_hazard_event['id_unit'] = df_adhoc_hazard_event['id_unit'].astype(int) 

        ### Insert to database
        #print df_adhoc_hazard_event
        df_adhoc_hazard_event.to_sql('adhoc_hazard_event',psql_engine,if_exists='append',index=False)

        ### Prepare the hazard adhoc summary frame to be inserted to database
        df_adhoc_summary = df_hazard_compile
        #df_hazard_compile.reset_index(inplace=True)
        #df_fl_hazard.reset_index(inplace=True)
        #df_fl_hazard = df_fl_hazard.drop_duplicates(subset='unit',take_last = True)
        #df_district_detail = df_fl_hazard[['unit','village','district','rt','rw']]       
        #df_merge_adhoc_summary = pd.merge(df_hazard_compile, df_district_detail, how='left', on=['unit'])
        #df_adhoc_summary = df_merge_adhoc_summary[['unit','village','district','rt','rw','mean_depth','duration','kelas']]
        df_adhoc_summary['id_event'] = last_id_adhoc_event
        #df2['id_event'] = last_id_adhoc_event
        #df_adhoc_summary = df_adhoc_summary[['id_event','unit','village','district',\
        #                                     'rt','rw','mean_depth','duration','kelas']]
        #df_adhoc_summary.columns = ['id_event','id_unit','kelurahan',\
        #                            'kecamatan','rt','rw','kedalaman_rata_rata',\
        #                            'durasi_rendaman','kelas']
        df_adhoc_summary = df_adhoc_summary[['id_event','id_unit','kelurahan','kecamatan','rt','rw',\
                                                   'kedalaman_rata_rata','durasi_rendaman','kelas']]
        
        ### convert id_event to integer
        #df_adhoc_summary['id_unit'] = df_adhoc_summary['id_unit'].astype(int)

        ### Insert to database summary
        print df_adhoc_summary
        df_adhoc_summary.to_sql('adhoc_hazard_summary',psql_engine,if_exists='append',index=False)

        ### Insert dala database
        inserting_table_dala_result(last_id_adhoc_event,psql_db_con,input_sql_folder)

        return last_id_adhoc_event

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e        
        if psql_db_con:
            psql_db_con.rollback()
        sys.exit(1)

    except Exception,e:
        print e
        sys.exit(1)

def insert_auto_hazard_tables_at_psql_database(t0,t1,psql_db_con,psql_engine,input_sql_folder,\
                                                df_fl_hazard,df_hazard_compile):
    try:
        ### Get last id event index from adhoc_event_table    
        df_last_auto_event = psql.read_sql("SELECT id_event FROM auto_event order by id_event DESC LIMIT 1",psql_db_con)
        last_id_auto_event = df_last_auto_event.ix[0]['id_event']
        
        ### Prepare the hazard adhoc event data frame to be inserted to database
        df_auto_hazard_event = df_fl_hazard[['unit','depth','report_time','request_time']]
        df_auto_hazard_event['id_event'] = last_id_auto_event
        df_auto_hazard_event = df_auto_hazard_event[['id_event','unit','depth','report_time','request_time']]
        df_auto_hazard_event.columns = ['id_event','id_unit','kedalaman','report_time','request_time']

        ### convert id_event to integer
        df_auto_hazard_event['id_unit'] = df_auto_hazard_event['id_unit'].astype(int) 

        ### Insert to database
        #print df_adhoc_hazard_event
        df_auto_hazard_event.to_sql('auto_hazard_event',psql_engine,if_exists='append',index=False)

        ### Prepare the hazard adhoc summary frame to be inserted to database
        df_auto_summary = df_hazard_compile
        df_auto_summary['id_event'] = last_id_auto_event
        df_auto_summary = df_auto_summary[['id_event','id_unit','kelurahan','kecamatan','rt','rw',\
                                                   'kedalaman_rata_rata','durasi_rendaman','kelas']]

        ### Insert to database summary
        print df_auto_summary
        df_auto_summary.to_sql('auto_hazard_summary',psql_engine,if_exists='append',index=False)

        ### Insert dala database
        inserting_table_dala_result_auto(last_id_auto_event,psql_db_con,input_sql_folder)

        return last_id_auto_event

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e        
        if psql_db_con:
            psql_db_con.rollback()
        sys.exit(1)

    except Exception,e:
        print e
        sys.exit(1)

def inserting_table_dala_result(last_id_adhoc_event,psql_db_con,input_sql_folder):
    sql_file = input_sql_folder + '/' + 'sql_query_dala_aset_adhoc.txt'
    #sql_query = open(sql_file, 'r').read().replace('\n',' ')
    sql_query = open(sql_file, 'r').read()

    list_data = []
    for i in range(57):
        list_data.append(last_id_adhoc_event)    
    data = tuple(list_data)

    sql_query_final = sql_query%data
    cur = psql_db_con.cursor()
    cur.execute(sql_query_final)
    psql_db_con.commit()

def inserting_table_dala_result_auto(last_id_auto_event,psql_db_con,input_sql_folder):
    sql_file = input_sql_folder + '/' + 'sql_query_dala_aset_auto.txt'
    sql_query = open(sql_file, 'r').read()

    list_data = []
    for i in range(57):
        list_data.append(last_id_auto_event)    
    data = tuple(list_data)

    sql_query_final = sql_query%data
    cur = psql_db_con.cursor()
    cur.execute(sql_query_final)
    psql_db_con.commit()
    
    # update total at table auto_dala_result PostgreSQL
    sql_dump_total = "UPDATE auto_dala_result SET total = damage+loss WHERE id_event=%s"%(last_id_auto_event)
    cur.execute(sql_dump_total)
    psql_db_con.commit()
    
    sql_dump_damage = "UPDATE auto_dala_result SET total = damage WHERE asset='KENDARAAN' AND loss is null AND id_event=%s"%(last_id_auto_event)
    cur.execute(sql_dump_damage)
    psql_db_con.commit()
    
    sql_dump_loss = "UPDATE auto_dala_result SET total = loss WHERE asset='KENDARAAN' AND damage is null AND id_event=%s"%(last_id_auto_event)
    cur.execute(sql_dump_loss)
    psql_db_con.commit()