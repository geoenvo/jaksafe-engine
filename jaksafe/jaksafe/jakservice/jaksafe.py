import ConfigParser
import os
import sys

#### import postgresql and mysql package
import MySQLdb
import psycopg2
from sqlalchemy import create_engine


global_conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'global_conf.cfg')

def get_database_connection(ip_address,user,paswd,database):
    con = MySQLdb.connect(ip_address,user,paswd,database)
    return con

def get_pgsql_database_connection(user,paswd,database,port_number):
    psql_con = None    
    try:     
        psql_con = psycopg2.connect(database = database,\
                                    user = user,\
                                    password = paswd,\
                                    port = port_number)

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        print 'Program is terminating ....'        
        sys.exit(1)
    return psql_con
    

def get_pgsql_database_engine(ip_address,user,paswd,database,port_number):
    ## example of psql url => 'postgresql://jaksafe:password@localhost:5432/test_db')
    psql_url = 'postgresql://' + user + ':' + paswd + '@' + ip_address + ':' + str(port_number) + '/' + database
    print 'creating postgresql engine at => %s'%(psql_url) 
    pg_engine = create_engine(psql_url)
    return pg_engine

## Defining the parser
global_conf_parser = ConfigParser.SafeConfigParser()
global_conf_parser.read(global_conf_file)

## Dims configuration
dims_url_base = global_conf_parser.get('dims_conf','url_dims')

## MySQL Database configuration
database_url_address = global_conf_parser.get('database_configuration','url_address')
user = global_conf_parser.get('database_configuration','user')
paswd = global_conf_parser.get('database_configuration','paswd')
database_name = global_conf_parser.get('database_configuration','database_name')

## PostgreSQL Database configuration
pgsql_address = global_conf_parser.get('psql_database_configuration','ip_address')
pgsql_user = global_conf_parser.get('psql_database_configuration','user')
pgsql_paswd = global_conf_parser.get('psql_database_configuration','passwd')
pgsql_database_name = global_conf_parser.get('psql_database_configuration','database_name')
pgsql_database_port = global_conf_parser.get('psql_database_configuration','port')

## Initialize QGIS installation path
qgis_install_path = global_conf_parser.get('qgis_conf','qgis_install_path')

## Initialize Open MySQL database connection
db_con = get_database_connection(database_url_address,user,paswd,database_name)

## Initialize Open Postgresql database connection with psyopg2
psql_db_con = get_pgsql_database_connection(pgsql_user,pgsql_paswd,pgsql_database_name,pgsql_database_port)

## Initialize Create postgresql engine with SQLAlchemy
psql_engine = get_pgsql_database_engine(pgsql_address,pgsql_user,pgsql_paswd,pgsql_database_name,pgsql_database_port)
