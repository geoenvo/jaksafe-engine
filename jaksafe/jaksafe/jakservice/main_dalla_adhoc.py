__AUTHOR__= 'FARIZA DIAN PRASETYO'

from jaksafe import global_conf_parser
from jaksafe import qgis_install_path

from config_folder import input_folder
from config_folder import hazard_kelas_folder
from config_folder import input_boundary_folder
from config_folder import input_exposure_folder
from config_folder import input_exposure_shapefile_folder
from config_folder import adhoc_output_folder
from config_folder import input_sql_folder

from auto_preprocessing.preprocess_fl_report import *
from auto_preprocessing.auto_calc_function import *

from impact_analysis.hazard_compilation_function import *
from impact_analysis.hazard_analysis_class import HazardLayer
from impact_analysis.hazard_analysis_class import hazard_layer_to_dataframe
from impact_analysis.exposure_analysis_class import ExposureLayer

import Time as t
import requests
import sys
import datetime
import os


# Package QGIS
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *

import pandas.io.sql as psql

#input from data dims and database configuration
base_dims_url = global_conf_parser.get('dims_conf','url_dims')
table_name_event = global_conf_parser.get('database_configuration','table_name_event')
table_raw_name_event = global_conf_parser.get('database_configuration','table_raw_name_event')
table_name_autocalc = global_conf_parser.get('database_configuration','table_name_autocalc')

report_hazard_summary_name = global_conf_parser.get('file_output','output_hazard_summary_report')
report_RT_name = global_conf_parser.get('file_output','output_rt_report')
report_RW_name = global_conf_parser.get('file_output','output_rw_report')

#input kelas hazard
kelas_hazard_config_name = global_conf_parser.get('file_input','input_kelas')
kelas_hazard_file = hazard_kelas_folder + '/' + kelas_hazard_config_name

#input layer for hazard
boundary_name = global_conf_parser.get('file_input','input_boundary_layer')
input_boundary_layer_file = input_boundary_folder + '/' + boundary_name

#Output layer for hazard
output_hazard_layer_name = global_conf_parser.get('file_output','output_hazard')

#input layer for building exposure
building_exposure_layer_name = global_conf_parser.get('file_input','input_building_exposure')
input_building_exposure_layer_file = input_exposure_shapefile_folder + '/' + building_exposure_layer_name

#output layer for building exposure
output_building_exposure_layer_name = global_conf_parser.get('file_output','output_building_exposure')

#input layer for road exposure
road_exposure_layer_name = global_conf_parser.get('file_input','input_road_exposure')
input_road_exposure_layer_file = input_exposure_shapefile_folder + '/' + road_exposure_layer_name

#output layer for building exposure
output_road_exposure_layer_name = global_conf_parser.get('file_output','output_road_exposure')

max_observe = 2
base_folder_output = adhoc_output_folder


def calculate_impact_function(df_fl_event,t0,t1):
    try:
        df_all_units = df_fl_event

        ## create fl report
        create_fl_report(df_all_units,t.Time(t1),report_RT_name,report_RW_name,base_folder_output)
        
        ## Compiling hazard report
        df_compiled = compiling_hazard_fl_in_folder(df_all_units,kelas_hazard_file,base_folder_output,t.Time(t0),t.Time(t1))

        obj_hazardlayer = HazardLayer(input_boundary_layer_file,kelas_hazard_file,output_hazard_layer_name,base_folder_output,t.Time(t0),t.Time(t1))
        hazard_fl_layer = obj_hazardlayer.create_hazard_shp(df_compiled)

        ## Creating building impact-exposure layer
        obj_buildingExposure = ExposureLayer(input_building_exposure_layer_file,base_folder_output,'building',t.Time(t0),t.Time(t1))
        obj_buildingExposure.set_building_exposure_layer_output(output_building_exposure_layer_name)
        print "Intersecting exposure building with hazard ...."
        obj_buildingExposure.intersect_building_exposure_with_hazard(hazard_fl_layer)

        obj_roadExposure = ExposureLayer(input_road_exposure_layer_file,base_folder_output,'road',t.Time(t0),t.Time(t1))
        obj_roadExposure.create_exposure_road_layer(output_road_exposure_layer_name,hazard_fl_layer)
        print "Intersecting exposure road with hazard ...."
        obj_roadExposure.intersect_road_exposure_with_hazard(hazard_fl_layer)

    except Exception,e:
        print e
        sys.exit(1)
    return obj_buildingExposure,obj_roadExposure


   
def create_fl_report_and_compilation_report(df_fl_event,t0,t1):
    try:
        df_all_units = df_fl_event   
        ## create fl report for RT,RW,and summary in csv 
        create_summary_fl_report(df_all_units,\
                                 t.Time(t0),\
                                 t.Time(t1),\
                                 report_hazard_summary_name,\
                                 report_RT_name,\
                                 report_RW_name,\
                                 base_folder_output)
        ## create compilation report    
        df_compiled_hazard = compiling_hazard_fl_in_folder(df_all_units,\
                                                           kelas_hazard_file,\
                                                           base_folder_output,\
                                                           t.Time(t0),\
                                                           t.Time(t1))
        ## create shp hazard layer
        obj_layer = HazardLayer(input_boundary_layer_file,\
                                      kelas_hazard_file,\
                                      output_hazard_layer_name,\
                                      base_folder_output,\
                                      t.Time(t0),t.Time(t1))
                                                                               
        hazard_fl_layer = obj_layer.create_hazard_shp(df_compiled_hazard)

        df_all_hazard = hazard_layer_to_dataframe(hazard_fl_layer)
        dump_all_hazard_to_csv(df_all_hazard,base_folder_output,t.Time(t0),t.Time(t1))
                               
    except Exception,e:
        print e
        sys.exit(1)
    #return df_all_units,df_compiled_hazard,df_compiled_hazard2
    return df_all_units,df_all_hazard

def create_summary_auto_calculation(t0,t1,db_con,table_name_autocalc):
    table_name = table_name_autocalc
    print table_name
    sql_dump = "INSERT INTO "+table_name+ \
               " (t0,t1,damage,loss) VALUES ('%s','%s',NULL,NULL)"%(t0,t1)

    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    db_con.commit()
    last_row_id = cursor.lastrowid
    return last_row_id

#def initialize_adhoc_summary(t0,t1,db_con,table_name):
def initialize_adhoc_summary(t0,t1,id_user,id_group,db_con,table_name):
    ## Damage and loss initialization
    ## id_event => NULL for initialization
    damage = 0.
    loss = 0.

    if id_group == None:
        id_group = 'NULL'

    if id_user == None:
        id_user = 'NULL'

    sql_dump = "INSERT INTO " + \
                table_name + \
                " (id_event,id_user,id_user_group,t0,t1,damage,loss) "+ \
                "VALUES (NULL,'%s','%s','%s','%s',%.2f,%.2f)"%(id_user,id_group,t0,t1,damage,loss)
    
    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    db_con.commit()
    last_row_id = cursor.lastrowid

    return last_row_id

def create_summary_adhoc_calculation(t0,t1,db_con,psql_db_con,last_id_adhoc,table_name_adhoc_calc):
    query_summary_file = input_sql_folder + '/' + 'sql_query_dala_summary_adhoc.txt'
    sql_query = open(query_summary_file, 'r').read().replace('\n',' ')
    sql_query_final = sql_query %(str(last_id_adhoc))

    df_last_adhoc_event = psql.read_sql(sql_query_final,psql_db_con)
    total_damage = df_last_adhoc_event.ix[0]['total_damage']
    total_loss = df_last_adhoc_event.ix[0]['total_loss']

    table_name = table_name_adhoc_calc
    print table_name
    sql_dump = "INSERT INTO "+table_name+ \
               " (t0,t1,damage,loss) VALUES ('%s','%s',%.3f,%.3f)"%(t0,t1,total_damage,total_loss)

    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    db_con.commit()

    last_row_id = cursor.lastrowid
    return last_row_id

def update_adhoc_summary_table(last_summary_id,last_event_id,db_con,table_name):
    query_summary_file = input_sql_folder + '/' + 'sql_query_dala_summary_adhoc.txt'
    sql_query = open(query_summary_file, 'r').read().replace('\n',' ')
    sql_query_final = sql_query %(str(last_event_id))

    ### Get damage and loss
    df_last_adhoc_event = psql.read_sql(sql_query_final,psql_db_con)
    total_damage = df_last_adhoc_event.ix[0]['total_damage']
    total_loss = df_last_adhoc_event.ix[0]['total_loss']

    str_update = "UPDATE "+table_name    
    str_set_column = " SET id_event = %d, damage = %.3f, loss = %.3f"%(last_event_id,total_damage,total_loss)
    str_where = " WHERE id = %d"%(last_summary_id)

    sql_dump = str_update+ str_set_column+ str_where
    print sql_dump

    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    db_con.commit()
   

def main_adhoc_impact_analysis(t0,t1,db_con):
    QgsApplication.setPrefixPath(qgis_install_path, True)
    QgsApplication.initQgis()

    print "Fetching data from fl_event..."
    print t0
    print t1

    df_fl_event = get_fl_event(db_con,table_name_event,t0,t1)

    if not df_fl_event.empty:

        ## preprocessing df_fl_event
        df_all_units = preprocessing_the_hazard_data(df_fl_event)

        ## calculate impact function
        obj_buildingExposure,obj_roadExposure = calculate_impact_function(df_fl_event,t0,t1)

        print "End of impact analysis service ..."
    else:
        print "There is no Flood event from %s until %s"%(t0,t1)

    return base_folder_output
    
def main_adhoc_impact_analysis_dump_csv(t0,t1,db_con,psql_db_con,psql_engine):
    ### Initialization of Qgis installation path
    QgsApplication.setPrefixPath(qgis_install_path,True)
    QgsApplication.initQgis()

    ### Initial id event as None (NULL)
    last_id_ev = None

    print "Fetching data from fl_event..."
    df_fl_event = get_fl_event(db_con,table_name_event,t0,t1)
    is_hazard_empty = df_fl_event.empty
    
    if not df_fl_event.empty:
        ## preprocessing the hazard
        df_all_units = preprocessing_the_hazard_data(df_fl_event)
        df_fl_event = df_all_units
        
        ## creating hazard report
        df_fl_hazard,df_hazard_compile = create_fl_report_and_compilation_report(df_fl_event,t0,t1)

        ## inserting data fl_hazard and fl_compile to postgresql database
        last_id_ev = insert_fl_hazard_summary_to_postgresql_database(psql_db_con,\
                                                        psql_engine,\
                                                        input_sql_folder,\
                                                        t0,t1,\
                                                        df_fl_hazard,\
                                                        df_hazard_compile)

        ## inserting data fl_hazard and fl_compile to postgresql database
        dump_to_csv_table_adhoc_dala_result(last_id_ev,psql_db_con,base_folder_output,t.Time(t0),t.Time(t1))

        ## create compilation zip file
        create_zip_of_summary_and_shp(base_folder_output,\
                                      t.Time(t0),\
                                      t.Time(t1))

        ## create zip shp compilation
        create_zip_of_shp(base_folder_output,\
                                      t.Time(t0),\
                                      t.Time(t1))

    return is_hazard_empty,last_id_ev
