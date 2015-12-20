__AUTHOR__= 'FARIZA DIAN PRASETYO'

# Package QGIS
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
from header_config_variable import *

import os
import sys
import pandas as pd
import numpy as np

class HazardLayer:

    def __init__(self,base_input_layer_name,hazard_class_file,layer_output_name,folder_output,t0,t1):
        ## input attributes        
        self.base_input_layer_name = base_input_layer_name
        self.hazard_class_file = hazard_class_file

        ## output attributes
        self.layer_output_name = layer_output_name
        self.base_folder_output = folder_output
        self.t0 = t0
        self.t1 = t1
        self.folder_format = glob_folder_format        
        self.t0.set_time_format(self.folder_format)
        self.t1.set_time_format(self.folder_format)

        #self.hazard_dir = self.base_folder_output + '/hazard'
        #self.fl_report_dir = self.base_folder_output + '/fl_report'

        self.hazard_dir = self.base_folder_output + '/report'
        self.fl_report_dir = self.base_folder_output + '/report'

    def create_hazard_shp(self,df_compiled):
        ## create output folder
        t0 = self.t0.formattedTime()
        t1 = self.t1.formattedTime()

        self.hazard_dir = self.check_and_create_output_directory(self.hazard_dir,t0,t1)
        hazard_shp_file = self.hazard_dir + '/' + t0 + '_' + t1 + '_' + self.layer_output_name

        self.base_input_layer = self.create_base_layer(self.base_input_layer_name)

        ## Initialize hazard map
        error = QgsVectorFileWriter.writeAsVectorFormat(self.base_input_layer,hazard_shp_file, "CP1250", None, "ESRI Shapefile")
        if error:
            print "Error creating base hazard layer,program is exiting ...."
            sys.exit(1)

        layer_tag = self.t0.formattedTime() + '_' + self.t1.formattedTime() + '_hazard_fl_layer'
        
        ## Open the hazard layer
        layer = QgsVectorLayer(hazard_shp_file, layer_tag, 'ogr')        
        layer.startEditing()
        
        ## Creating new attribute
        self.create_new_attribute_field_name(layer,header_shp_m_depth,QVariant.Double)
        self.create_new_attribute_field_name(layer,header_shp_duration,QVariant.Double)
        self.create_new_attribute_field_name(layer,header_shp_kelas,QVariant.String)

        # Create dictionary for all polygon district
        feature_dict = {f.id(): f for f in layer.getFeatures()}

        # Build a spatial index for district polygon 
        index = QgsSpatialIndex()
        
        base_layer_units = []
        for f in feature_dict.values():
            index.insertFeature(f)
            base_layer_units.append(f[header_shp_ID])

        flag_id_exist = [0] * len(df_compiled.index)

        for f in feature_dict.values():
            if f[header_shp_ID] in df_compiled.index:
                idx = np.where(df_compiled.index == f[header_shp_ID])
                idx_hazard = idx[0][0]
                
                f[header_shp_m_depth] = df_compiled.values[idx_hazard][0]
                f[header_shp_duration] = df_compiled.values[idx_hazard][2]
                f[header_shp_kelas] = df_compiled.values[idx_hazard][3]
                
                flag_id_exist[idx_hazard] = 1
                
                layer.updateFeature(f)

        ### LATER DEVELOPMENT: SECOND CHECKING!!
        df_compiled['is_id_exist'] = flag_id_exist  
        print "Succesfully creating hazard shp"
        
        ## Start to find impacted distric
        df_config_hazard = pd.read_csv(self.hazard_class_file)
        df_config_hazard.fillna(-9999,inplace = True)
        df_config_hazard = df_config_hazard[df_config_hazard['kedalaman_bawah']==-9999]

        buffer_range = 10.

        # Create dictionary for all flooded polygon district    
        feature_fl_dict = {f.id(): f for f in layer.getFeatures() if f[header_shp_kelas]!= None}

        # Create dictionary for all non-flooded polygon district
        feature_non_fl_dict = {f.id(): f for f in layer.getFeatures() if f[header_shp_kelas]== None}
        
        # Build a spatial index for district polygon 
        index_no_fl = QgsSpatialIndex()

        for f in feature_non_fl_dict.values():
            if f[header_shp_kelas]== None:
                index_no_fl.insertFeature(f)
        
        # Iterate only the flooded area
        for f in feature_fl_dict.values():
            fid =  f.id()
            # Define the geometry each feature
            geom = f.geometry()      
            # Create buffer geometry
            buff_geom = geom.buffer(buffer_range,2)
            # Intersection function
            intersecting_ids = index_no_fl.intersects(buff_geom.boundingBox())

            for intersecting_id in intersecting_ids:
                ## Feature that intersect with the flooded district
                intersecting_f = feature_non_fl_dict[intersecting_id]

                if (f != intersecting_f and not intersecting_f.geometry().disjoint(geom)):
                    unit_affected = intersecting_f.id()
                    current_durasi = f[header_shp_duration]

                    ## Check if affected value is existing
                    if intersecting_f[header_shp_kelas] != None:
                        last_durasi = intersecting_f[header_shp_duration]

                        ## Get the maximum duration
                        max_durasi = max(current_durasi,last_durasi)
                        intersecting_f[header_shp_kelas] = self.convert_duration_affected_to_class(df_config_hazard,max_durasi)
                        intersecting_f[header_shp_duration] = max_durasi

                    else:
                        intersecting_f[header_shp_kelas] = self.convert_duration_affected_to_class(df_config_hazard,current_durasi)
                        intersecting_f[header_shp_duration] = current_durasi 

                ## Updating the layer
                layer.updateFeature(intersecting_f)

        ## Commit the changes in layer
        layer.commitChanges()
        print "Succesfully creating affected area hazard shp"
        self.output_layer = layer

        return self.output_layer

    def convert_duration_affected_to_class(self,df_config_hazard,affected_duration):
        affected_class = None
        #df_config_hazard.fillna(-9999,inplace = True)
        for idx,row in df_config_hazard.iterrows():
            if affected_duration >= row['durasi_bawah'] and affected_duration <= row['durasi_atas']:
                affected_class = row['kelas']
        return affected_class

    def create_new_attribute_field_name(self,input_layer,attribute_name,data_type):
        ## Start Editing the layer
        caps = input_layer.dataProvider().capabilities()

        ## Editing the layer to add field name    
        if caps & QgsVectorDataProvider.AddAttributes:
            input_layer.beginEditCommand("Adding attribute vavlue")
            res = input_layer.dataProvider().addAttributes([QgsField(attribute_name,data_type)])
            print "Succesfully adding attribute : %s"%(attribute_name)

            if res == False:
                input_layer.destroyEditCommand()
                sys.exit("Error adding attribute: %s"%(attribute_name))
            input_layer.endEditCommand()
            ## Updating the layer    
            input_layer.updateFields()

    def check_and_create_output_directory(self,base_directory,t0,t1):
        output_directory = base_directory + '/' + t0 + '_' + t1
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        return output_directory

    def create_base_layer(self,base_input_layer_name):
        print "Opening base boundary layer ...."
        baseLayer = QgsVectorLayer(base_input_layer_name,'RW_RT_base_layer', 'ogr')
        if (not baseLayer.isValid()):
            print "input boundary layer is not valid, system is exiting ..."
            sys.exit(1)
        return baseLayer

def hazard_layer_to_dataframe(hazard_layer):
        if (not hazard_layer.isValid()):
            print "total hazard layer is not valid, system is exiting ..."
            sys.exit(1)
        else:
            formula_rule = header_shp_kelas+" is not NULL"
            request_feature = QgsFeatureRequest()
            request_feature.setFilterExpression(formula_rule)

            hazard_features = hazard_layer.getFeatures(request_feature)

            list_hazard = []
            
            for f in hazard_features:
                dict_f = {}
                dict_f['unit'] = f['ID']
                dict_f['kelurahan'] = f['KELURAHAN']
                dict_f['kecamatan'] = f['KECAMATAN']
                dict_f['rt'] = ''

                if f['RW'] == None:
                    f['RW'] = 'RW 099'
                dict_f['rw'] = f['RW']

                if f['M_DEPTH'] == None:
                    f['M_DEPTH'] = 0
                dict_f['kedalaman_rata_rata'] = f['M_DEPTH']

                dict_f['durasi_rendaman'] = f['DURATION']
                dict_f['kelas'] = f['KELAS'] 
                
                list_hazard.append(dict_f)

            df_hazard_summary = pd.DataFrame.from_dict(list_hazard)
            df_hazard_summary['rw'] = df_hazard_summary['rw'].replace({'RW ':''},regex=True)

            ## casting 
            df_hazard_summary['unit'] = df_hazard_summary['unit'].astype(int)
            df_hazard_summary['id_unit'] = df_hazard_summary['unit']            
            df_hazard_summary['kedalaman_rata_rata'] = df_hazard_summary['kedalaman_rata_rata'].\
                                                                         astype(float)
            df_hazard_summary['durasi_rendaman'] = df_hazard_summary['durasi_rendaman'].astype(float)
            
            return df_hazard_summary
