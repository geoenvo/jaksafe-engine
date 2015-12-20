import ConfigParser
import os

global_conf_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'global_conf.cfg')

## Defining the parser
conf_parser = ConfigParser.SafeConfigParser()
conf_parser.read(global_conf_file)

## main project folder
project_folder = conf_parser.get('folder_conf','project_folder')
auto_folder_name = conf_parser.get('folder_conf','auto_folder')
adhoc_folder_name = conf_parser.get('folder_conf','adhoc_folder')

## auto dalla
auto_folder = project_folder + '/'+ auto_folder_name

## adhoc dalla
adhoc_folder = project_folder + '/'+ adhoc_folder_name

## input folder
input_folder = auto_folder + '/input'
hazard_kelas_folder = auto_folder + '/config/kelas_dampak'
input_boundary_folder = input_folder + '/boundary'
input_sql_folder = input_folder + '/sql'
input_exposure_folder = input_folder + '/exposure'
input_exposure_shapefile_folder = input_exposure_folder + '/shapefile'


## auto output
auto_output_folder = auto_folder + '/output'

## adhoc output
adhoc_output_folder = adhoc_folder + '/output'
