"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-21 13:04:14
 * @modify date 2020-06-16 15:51:25
 * @desc [
    Utility class to save and store datetime and date objects in json file.
 ]
 */
"""

##########
# Imports
##########

import datetime


from logs import log_func_name, logger, log_all


##########
# Time Encoder
##########
class TimeEncoder(object):

    @staticmethod
    @log_func_name
    def convert_datetime_to_dict(time_obj: object) -> dict:
        """Returns time object as dictionary."""
        time_dict = {
            'datetime.datetime' :   True,
            'year'              :   time_obj.year,
            'month'             :   time_obj.month,
            'day'               :   time_obj.day,
            'hour'              :   time_obj.hour,
            'minute'            :   time_obj.minute,
            'second'            :   time_obj.second,
            'microsecond'       :   time_obj.microsecond,
        }
        return time_dict


    @staticmethod
    @log_func_name
    def convert_dict_to_datetime(time_dict: dict) -> object:
        """Loads datetime object from dictionary."""
        if 'datetime.datetime' not in time_dict.keys():
            logger.error("convert_dict_to_datetime: Not datetime dict.")
            return None
        
        time_keys = ('year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond')
        year, month, day, hour, minute, second, microsecond = (
            (time_dict[key] for key in time_keys))
        
        return datetime.datetime(
            year= year,
            month= month,
            day= day,
            hour= hour,
            minute= minute,
            second= second,
            microsecond= microsecond
            )


    @staticmethod
    @log_func_name
    def convert_date_to_str(date_obj: object) -> str:
        """Converts the date to str format, for dict key.

        Follows YYYY_MM_DD format.
        """
        str_joiner = "_"
        year, month, day = str(date_obj.year), str(date_obj.month), str(date_obj.day)

        date_info = (year, month, day)
        date_key = str_joiner.join(date_info)
        return date_key


    @staticmethod
    @log_func_name
    def convert_str_to_date(date_str: str) -> object:
        """Converts str object to date object for time delta comparisons.

        Follows YYYY_MM_DD format."""
        str_joiner = "_"
        year, month, day = (int(date) for date in date_str.split(str_joiner))

        return datetime.date(year, month, day)

