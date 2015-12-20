# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import datetime
import logging
import os
import sys

import config
import dala
import db
from error import *
import post
import report
import summary
import tools

def main(time_0, time_1, list_subsektor, last_row_id):

    logger = logging.getLogger('jaksafe_adhoc.post_processing.run')
    logger.info('AWAL POST PROCESSING')

    # database connection
    db_config = config.Database()
    params = db_config.params_con
    db_con = db.DBase(params)

    data = {
        'damage' : -999,
        'loss' : -999,
        'id' : last_row_id
    }
    
    # post processing
    try:
        pp = post.PostProc(time_0, time_1, tipe='adhoc')
        pp.analyze()
    except NoHazardGeneratedDirError:
        logger.error('No hazard generated dir')
        # insert 0-damage and 0-loss in case of no hazard or impact
        db_con.update('adhoc_calc', data)
        sys.exit(1)
    except NoImpactBuildingError:
        logger.error('No impact building')
        # insert 0-damage and 0-loss in case of no hazard or impact
        db_con.update('adhoc_calc', data)
        sys.exit(1)
    except NoImpactRoadError:
        logger.error('No impact road')
        # insert 0-damage and 0-loss in case of no hazard or impact
        db_con.update('adhoc_calc', data)
        sys.exit(1)
    except NoHazardGeneratedFileError:
        logger.error('No hazard generated file')
        # insert 0-damage and 0-loss in case of no hazard or impact
        db_con.update('adhoc_calc', data)
        sys.exit(1)
        

    # calculate dala
    lada = dala.Dala(time_0, time_1, tipe='adhoc')
    lada.calculate(list_subsektor)

    # summary
    ringkasan = summary.Summary(time_0, time_1, tipe='adhoc')
    pn = ringkasan.summarize()
    total = ringkasan.total()

    # zip hazard and impact
    o_zip = tools.Zipper(time_0, time_1, tipe='adhoc')
    o_zip.zip_result()

    # generate report
    report.report_dala(time_0, time_1, ringkasan, list_subsektor, tipe='adhoc')

    t1 = datetime.datetime.now()
    
    # insert into database
    data = {
        'damage' : total['KERUSAKAN'],
        'loss' : total['KERUGIAN'],
        'id' : last_row_id
    }
    db_con.update('adhoc_calc', data)

    logger.info('AKHIR POST PROCESSING')

    ############################################################################
