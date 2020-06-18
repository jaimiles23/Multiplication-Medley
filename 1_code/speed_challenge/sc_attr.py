"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-21 11:57:09
 * @modify date 2020-05-22 22:50:16
 * @desc [
    SC_Attr utility class to manage speed challenge session attributes.
    - General
    - Timer
    - Stats

    TODO: Refactor code for clarity.
 ]
 */
"""

##########
# Imports
##########

import datetime


from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from aux_utils.time_encoder import TimeEncoder


##########
# Speed Challenge Attributes
##########

class SC_Attr(object):

    @staticmethod
    @log_func_name
    def set_sc_diff(handler_input, difficulty: str) -> None:
        """Sets the difficulty for Speed Challenge."""
        attr = handler_input.attributes_manager.session_attributes
        attr['sc_difficulty'] = difficulty
        return


    @staticmethod
    @log_func_name
    def set_attr_start_sc(handler_input) -> None:
        """Sets starting attributes for Speed Challenge."""
        attr = handler_input.attributes_manager.session_attributes

        attr['mode'] = 'speed'
        attr['questions_answered'] = 0
        attr['help_pointer'] = 'speed_challenge'
        
        return None


    @staticmethod
    @log_func_name
    def set_attr_end_sc(handler_input) -> None:
        """Sets attributes when ending Speed Challenge."""
        attr = handler_input.attributes_manager.session_attributes

        end_attrs = (
            'mode',
            'help_pointer',
            'questions_answered',

            'sc_tables', 
            'sc_questions',
            'sc_difficulty',
            'sc_start_time',
            'sc_end_time'
            )
        
        for end_at in end_attrs:
            attr[end_at] = 0
            
        return None


    @staticmethod
    @log_func_name
    def check_no_questions(handler_input) -> bool:
        """Returns boolean representing if there are still speed challenge questions to answer."""
        attr = handler_input.attributes_manager.session_attributes

        sc_questions = attr.get('sc_questions', [-99] )
        return (len(sc_questions) == 0)


    ##########
    # Speed Challenge Timer
    ##########
    @staticmethod
    @log_func_name
    def save_start_time(handler_input) -> None:
        """Saves start time as session attribute."""
        attr = handler_input.attributes_manager.session_attributes

        start_time = datetime.datetime.now()
        start_time_dict = TimeEncoder.convert_datetime_to_dict(start_time)

        attr['sc_start_time'] = start_time_dict
        return None


    @staticmethod
    @log_func_name
    def save_end_time(handler_input) -> None:
        """Saves end time as session attribute."""
        attr = handler_input.attributes_manager.session_attributes

        end_time = datetime.datetime.now()
        end_time_dict = TimeEncoder.convert_datetime_to_dict(end_time)

        attr['sc_end_time'] = end_time_dict
        return None


    @staticmethod
    @log_func_name
    def get_sc_total_time(handler_input) -> int:
        """Returns the difference in seconds between start and end of sc.

        Also saves the float number as a session attribute."""
        attr = handler_input.attributes_manager.session_attributes

        start_time_dict = attr['sc_start_time'] 
        end_time_dict = attr['sc_end_time']
        start_time = TimeEncoder.convert_dict_to_datetime( start_time_dict)
        end_time = TimeEncoder.convert_dict_to_datetime( end_time_dict)

        time_difference = (end_time - start_time).seconds
        attr['sc_time_score'] = time_difference

        log_all(start_time, end_time, time_difference)
        return time_difference


    ##########
    # Stats
    ##########
    @staticmethod
    @log_func_name
    def log_sc_stats(handler_input) -> None:
        """Logs statistics for speed challenge."""
        attr = handler_input.attributes_manager.session_attributes
        sc_time = attr['sc_time_score']
        sc_difficulty = attr['sc_difficulty']

        logger.info(f"sc_time:  {sc_time}")
        logger.info(f"sc_difficulty:    {sc_difficulty}")
        return
