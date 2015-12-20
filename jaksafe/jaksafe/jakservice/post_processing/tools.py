# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import os
import zipfile

import config

class Zipper(object):

    """
    Kelas Zipper
    """

    def __init__(self, time_0, time_1, tipe='auto'):

        self.time_0 = time_0
        self.time_1 = time_1

        self.path = config.Path(time_0, time_1, tipe=tipe)

    def zip_result(self):

        """
        Memasukkan direktori hazard dan impact ke dalam file zip di dalam folder
        report
        """

        # directory
        shape_impact_dir = self.path.shp_impact_dir
        shape_hazard_dir = self.path.shp_hazard_dir

        # hazard and impact dir (input)
        # dir_impact = shape_impact_dir + self.time_1
        # dir_hazard = shape_hazard_dir + self.time_1

        ## shapefile output
        zip_file = self.path.output_dir + 'shapefile_' + \
            self.time_0 + '_' + self.time_1 + '.zip'
        o_zip = zipfile.ZipFile(zip_file, 'w')
        
        for file in os.listdir(self.path.shp_hazard_dir):
            # print os.path.join(self.path.shp_hazard_dir, file)
            path = os.path.join(self.path.shp_hazard_dir, file)
            if os.path.isfile(path):
                o_zip.write(path, arcname=file)
        
        for file in os.listdir(self.path.shp_impact_dir):
            # print os.path.join(self.path.shp_impact_dir, file)
            path = os.path.join(self.path.shp_impact_dir, file)
            if os.path.isfile(path):
                o_zip.write(path, arcname=file)

        o_zip.close()
        
        ## calculation csv output
        calc_zip_file = self.path.output_dir + 'calculation_' + \
            self.time_0 + '_' + self.time_1 + '.zip'
        calc_o_zip = zipfile.ZipFile(calc_zip_file, 'w')
        
        for file in os.listdir(self.path.summary_dir):
            path = os.path.join(self.path.summary_dir, file)
            if os.path.isfile(path) and path.lower().endswith(('.csv')):
                calc_o_zip.write(path, arcname=file)
        
        ## dala_csv_filename = 'dala_' + self.time_0 + '_' + self.time_1 + '.csv'
        ## calc_o_zip.write(os.path.join(self.path.output_dir, dala_csv_filename), arcname=file)
        
        for file in os.listdir(self.path.output_dir):
            path = os.path.join(self.path.output_dir, file)
            if os.path.isfile(path) and path.lower().endswith(('.csv')):
                calc_o_zip.write(path, arcname=file)
        
        calc_o_zip.close()