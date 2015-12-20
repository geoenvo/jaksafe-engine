__AUTHOR__= 'FARIZA DIAN PRASETYO'

# Package QGIS
from qgis.core import *
import qgis.utils
from PyQt4.QtCore import *
from header_config_variable import *

import os
import sys

headers = [header_shp_m_depth,header_shp_duration,header_shp_kelas,header_shp_kelurahan,\
    header_shp_kecamatan,header_shp_kabupaten,header_shp_rw,header_shp_rt]

class ExposureLayer:
   
    def __init__(self,base_input_layer_name,folder_output,exposureType,t0,t1):
        self.base_input_layer_name = base_input_layer_name
        self.base_folder_output = folder_output
        self.t0 = t0
        self.t1 = t1
        self.folder_format = glob_folder_format
        self.t0.set_time_format(self.folder_format)
        self.t1.set_time_format(self.folder_format)
        self.exposureType = exposureType
        self.shp_writer = None
        self.base_layer = self.create_base_layer(self.base_input_layer_name)       
        self.impact_folder = self.base_folder_output + '/impact' 

    def set_building_exposure_layer_output(self,output_filename):
        t0 = self.t0.formattedTime()
        t1 = self.t1.formattedTime()
        self.impact_folder = self.check_and_create_output_directory(self.impact_folder,t0,t1)
        self.output_filename = output_filename
        self.output_layer_file = self.impact_folder + '/' + t0 + '_' + t1 + '_' + self.output_filename
        try:
            error = QgsVectorFileWriter.writeAsVectorFormat(self.base_layer,self.output_layer_file, "CP1250", None, "ESRI Shapefile")
            if error == QgsVectorFileWriter.NoError:
                print "Success creating building exposure layer output: %s"%(self.output_filename)
                self.output_layer = QgsVectorLayer(self.output_layer_file, (t0 + '_' + t1 + '_' +'exposure_output_layer'), 'ogr')
            else :
                print "Error creating building exposure layer output: %s"%(self.output_filename)
        except Exception,e:
            print e
            sys.exit(0)

    def create_exposure_road_layer(self,output_filename,hazard_layer):
        t0 = self.t0.formattedTime()
        t1 = self.t1.formattedTime()
        self.impact_folder = self.check_and_create_output_directory(self.impact_folder,t0,t1)
        self.output_filename = output_filename
        self.output_layer_file = self.impact_folder + '/' + t0 + '_' + t1 + '_' + self.output_filename

        ## Get the Fields from the base layer and hazard layer
        fields = self.base_layer.pendingFields()
        hazard_fields = hazard_layer.pendingFields()
        fields.extend(hazard_fields)

        ## Get the Fields from the base layer and hazard layer
        fields.append(QgsField(header_shp_panjang,QVariant.Double))
        try:
            self.shp_writer = QgsVectorFileWriter(self.output_layer_file, "CP1250", fields, self.base_layer.wkbType(), \
                                                                                    self.base_layer.crs(), "ESRI Shapefile")
            if self.shp_writer.hasError() != QgsVectorFileWriter.NoError:
                print "Error when creating shapefile: ", self.shp_writer.hasError()
        except Exception,e:
            print e
            sys.exit(0)


    def intersect_road_exposure_with_hazard(self,hazard_layer):
        # obtain the exposure base_layer feature
        exposureFeatures = self.base_layer.getFeatures()

        # create dictionary of base_layer features and spatial index for exposure
        exposure_feature_dict = {}
        spatial_index_exposure = QgsSpatialIndex()

        for f in exposureFeatures:
            exposure_feature_dict[f.id()] = f
            spatial_index_exposure.insertFeature(f)

        # Iterating over the hazard feature that flooded and impacted
        for hazard_feature in hazard_layer.getFeatures():
            if hazard_feature[header_shp_kelas] != None:
                hazardAttributes = [hazard_feature[header_shp_m_depth],hazard_feature[header_shp_duration],hazard_feature[header_shp_kelas]]

                hazard_geom = hazard_feature.geometry()

                ## Get exposure that is intersected   
                intersecting_ids = spatial_index_exposure.intersects(hazard_geom.boundingBox())

                for intersecting_id in intersecting_ids:
                    fet = QgsFeature()

                    intersecting_f = exposure_feature_dict[intersecting_id]

                    clipped_exposure_geom = intersecting_f.geometry().intersection(hazard_geom)

                    if clipped_exposure_geom == None:
                        continue

                    if not clipped_exposure_geom.isGeosEmpty():
                        fet.setGeometry(clipped_exposure_geom)
                        impactAttributes = intersecting_f.attributes()
                        impactAttributes.extend(hazard_feature.attributes())
                        impactAttributes.append(clipped_exposure_geom.length())

                        fet.setAttributes(impactAttributes)
                        self.shp_writer.addFeature(fet)
        del self.shp_writer


    def create_new_attribute_field_name(self,input_layer,attribute_name,data_type):
        ## Start Editing the layer
        self.output_layer = input_layer

        caps = self.output_layer.dataProvider().capabilities()

        ## Editing the layer to add field name  
        if caps & QgsVectorDataProvider.AddAttributes:
            self.output_layer.beginEditCommand("Adding attribute vavlue")
            res = self.output_layer.dataProvider().addAttributes([QgsField(attribute_name,data_type)])
            print "Succesfully adding attribute : %s"%(attribute_name)

            if res == False:
                self.output_layer.destroyEditCommand()
                sys.exit("Error adding attribute: %s"%(attribute_name))
            self.output_layer.endEditCommand()
            ## Updating the layer
            self.output_layer.updateFields()

    def assign_feature_to_attribute_dictionary(self,attribute_dict,hazard_feature):
        attribute_dict[header_shp_m_depth] = hazard_feature[header_shp_m_depth]
        attribute_dict[header_shp_duration] = hazard_feature[header_shp_duration]
        attribute_dict[header_shp_kelas] = hazard_feature[header_shp_kelas]
        attribute_dict[header_shp_kelurahan] = hazard_feature[header_shp_kelurahan]
        attribute_dict[header_shp_kecamatan] = hazard_feature[header_shp_kecamatan]
        attribute_dict[header_shp_kabupaten] = hazard_feature[header_shp_kabupaten]
        attribute_dict[header_shp_rt] = hazard_feature[header_shp_rt]
        attribute_dict[header_shp_rw] = hazard_feature[header_shp_rw]
        attribute_dict[header_shp_area] = hazard_feature[header_shp_area]
        return attribute_dict

    def intersect_building_exposure_with_hazard(self,hazard_layer):
        ## [u'full_id', u'osm_id', u'ID', u'Kelurahan', u'Kecamatan', u'Kabupaten', u'RW', u'RT', u'm_depth', u'duration', u'kelas']
        hazard_field1 = u'full_id'
        hazard_field2 = u'osm_id'
        hazard_field3 = u'ID'

        fields_iter = hazard_layer.pendingFields()
        fields = [field.name() for field in fields_iter]
  
        if hazard_field1 in fields:
            fields.remove(hazard_field1)

        if hazard_field2 in fields:
            fields.remove(hazard_field2)

        if hazard_field3 in fields:
            fields.remove(hazard_field3)

        ## Start editing building layer
        self.output_layer.startEditing()

        for field in fields:
            data_type = QVariant.String
            if field == header_shp_m_depth or field == header_shp_m_depth:
                data_type = QVariant.Double
            self.create_new_attribute_field_name(self.output_layer,field,data_type)

        exposureFeatures = self.output_layer.getFeatures()
        exposure_feature_dict = {}
        spatial_index_exposure = QgsSpatialIndex()

        for f in exposureFeatures:
            exposure_feature_dict[f.id()] = f 
            spatial_index_exposure.insertFeature(f)

        hazardFeatures = hazard_layer.getFeatures()
        hazard_fl_feature_dict = {f.id(): f for f in hazardFeatures if f[header_shp_kelas] != None}

        for hazard_feature in hazard_fl_feature_dict.values():
            geom = hazard_feature.geometry()

            ## Get area that is intersected   
            intersecting_ids = spatial_index_exposure.intersects(geom.boundingBox())

            for intersecting_id in intersecting_ids:
                intersecting_f = exposure_feature_dict[intersecting_id]

                attribute_dict = {}

                if (not intersecting_f.geometry().disjoint(geom)):
                    attribute_dict = self.assign_feature_to_attribute_dictionary(attribute_dict,hazard_feature)

                    if attribute_dict[header_shp_m_depth] == None:
                        attribute_dict[header_shp_m_depth] = -9999

                    if intersecting_f[header_shp_kelas] != None:
                        last_m_depth = intersecting_f[header_shp_m_depth]
                        last_durasi = intersecting_f[header_shp_duration]

                        if last_m_depth == None:
                            last_m_depth = -9999

                        if last_m_depth > attribute_dict[header_shp_m_depth]:
                            attribute_dict = self.assign_feature_to_attribute_dictionary(attribute_dict,intersecting_f)
                        else:
                            if last_durasi > attribute_dict[header_shp_duration]:
                                attribute_dict = self.assign_feature_to_attribute_dictionary(attribute_dict,intersecting_f)

                    if attribute_dict[header_shp_duration] == -9999:
                        attribute_dict[header_shp_duration] = None

                    if attribute_dict[header_shp_m_depth] == -9999:
                        attribute_dict[header_shp_m_depth] = None

                    intersecting_f[header_shp_m_depth] = attribute_dict[header_shp_m_depth] 
                    intersecting_f[header_shp_duration] = attribute_dict[header_shp_duration]  
                    intersecting_f[header_shp_kelas] = attribute_dict[header_shp_kelas] 
                    intersecting_f[header_shp_kelurahan] = attribute_dict[header_shp_kelurahan] 
                    intersecting_f[header_shp_kecamatan] = attribute_dict[header_shp_kecamatan] 
                    intersecting_f[header_shp_kabupaten] = attribute_dict[header_shp_kabupaten] 
                    intersecting_f[header_shp_rt] = attribute_dict[header_shp_rt] 
                    intersecting_f[header_shp_rw] = attribute_dict[header_shp_rw]
                    intersecting_f[header_shp_area] = attribute_dict[header_shp_area] 

                    ## Updating the layer
                    self.output_layer.updateFeature(intersecting_f)

        ## Deleting non-impacted and affected feature in at the exposure
        formula_rule = header_shp_kelas+" is NULL"

        request_feature = QgsFeatureRequest()
        request_feature.setFilterExpression(formula_rule)

        non_impacted_features = self.output_layer.getFeatures(request_feature)

        for feature in non_impacted_features:
            self.output_layer.dataProvider().deleteFeatures([feature.id()]) 
        self.output_layer.commitChanges()

        return self.output_layer        

    def create_base_layer(self,base_input_layer_name):
        print "Opening base boundary layer ...."
        baseLayer = QgsVectorLayer(base_input_layer_name,'base_exposure_'+(self.exposureType), 'ogr')
        if (not baseLayer.isValid()):
            print "input layer exposure %s is not valid, system is exiting ..."%(self.exposureType)
            sys.exit(1)
        print "Sucesfully open exposure base layer: %s"%(self.base_input_layer_name)
        return baseLayer

    def check_and_create_output_directory(self,base_directory,t0,t1):
        output_directory = base_directory + '/' + t0 + '_' + t1 + '/' + 'shapefile'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        return output_directory

    def get_base_layer(self):
        return self.base_layer

    def get_output_layer(self):
        return self.output_layer
