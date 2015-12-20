__AUTHOR__= 'FARIZA DIAN PRASETYO'

import time
import datetime
import ConfigParser

from header_config_variable import *


def formatted_date_to_timestamp(input_date,time_format):
        return int(time.mktime(datetime.datetime.strptime(input_date,time_format).timetuple()))

def timestamp_to_formatted_date(input_timestamp,time_format):
        return datetime.datetime.fromtimestamp(int(input_timestamp)).strftime(time_format)

def timestamp_to_date_time(input_timestamp):
        return datetime.datetime.fromtimestamp(int(input_timestamp))

'''
This class for creating Time class
'''
class Time:
    ## Standar format time	
    def __init__(self,inputTime):
        self.time_format = std_time_format

        if isinstance(inputTime,int):
            self.timestamp = inputTime

        elif isinstance(inputTime,float):
            self.timestamp = int(inputTime)

        else :
            self.str_time = inputTime
            self.timestamp = formatted_date_to_timestamp(self.str_time,self.time_format)

    def formattedTime(self):
        return timestamp_to_formatted_date(self.timestamp,self.time_format)

    def timeStamp(self):
        return self.timestamp

    def set_time_format(self,time_format):
        self.time_format = time_format
