__AUTHOR__= 'KEZIA ROBERTA'

from jaksafe import global_conf_parser
from config_folder import input_sql_folder

import Time as t
#import requests
import sys
import datetime
import os

import pandas.io.sql as psql


#update mysql adhoc predef
def update_adhoc_predef_summary_table(last_event_id,db_con,psql_db_con,table_name):
    query_summary_file = input_sql_folder + '/' + 'sql_query_dala_summary_adhoc_predef.txt'
    sql_query = open(query_summary_file, 'r').read().replace('\n',' ')
    sql_query_final = sql_query %(str(last_event_id))

    ### Get damage and loss
    df_last_adhoc_event = psql.read_sql(sql_query_final,psql_db_con)
    total_damage = df_last_adhoc_event.ix[0]['total_damage']
    total_loss = df_last_adhoc_event.ix[0]['total_loss']

    str_update = "UPDATE "+table_name    
    str_set_column = " SET damage = %.3f, loss = %.3f"%(total_damage,total_loss)
    str_where = " WHERE id_event = %d"%(last_event_id)

    sql_dump = str_update+ str_set_column+ str_where
    print sql_dump

    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    db_con.commit()
   
    
#def initialize_adhoc_predef_summary(t0,t1,db_con,table_name): [ok]
def initialize_adhoc_predef_summary(event_name,id_user,id_group,db_con,table_name):
    ## Damage and loss initialization
    ## id_event => NULL for initialization
    damage = 0.
    loss = 0.

    if id_group == None:
        id_group = 0

    if id_user == None:
        id_user = 0

    sql_dump = "INSERT INTO " + \
                table_name + \
                " (id_user,id_user_group,event_name,damage,loss) "+ \
                "VALUES ('%s','%s','%s',%.2f,%.2f)"%(id_user,id_group,event_name,damage,loss)
    
    # prepare a cursor object using cursor() method
    cursor = db_con.cursor()
    cursor.execute(sql_dump)
    db_con.commit()
    last_row_id = cursor.lastrowid

    return last_row_id
	
#insert into summary hash	[ok]
def insert_hazard_summary(event_id,psql_db_con,psql_engine,temp_table_name):
    cursor_pg = psql_db_con.cursor()
    #create table temp, file dicopy ke temp, setelah selesai proses, drop table
    sql_dump =  "insert into public.adhoc_predef_hazard_summary (id_event, id_unit, kota, kecamatan, kelurahan, rw, rt, kelas) select %s id_event, id_rw, a.kota, a.kecamatan, a.kelurahan, a.rw, a.rt, a.kelas from %s a, boundary b where a.kota=b.kota and a.kecamatan=b.kecamatan and a.kelurahan=b.kelurahan and a.rw=b.rw" % (event_id, temp_table_name)
    cursor_pg.execute(sql_dump)
    psql_db_con.commit()
    last_row_id = cursor_pg.lastrowid
    print cursor_pg
    return last_row_id