"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-07 11:12:39
 * @modify date 2020-05-07 20:13:29
 * @desc [
    Utility class for ActDescription. Includes functions for:
    - Activity descriptions
    - Attributes
    - Prompt to play activity

 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from helper.help_utils import HelpUtils


import aux_data.skill_data
from . import data


##########
# Utility Class
##########

class DescriptUtils(object):

    ##########
    # Activity description
    ##########
    @staticmethod
    @log_func_name
    def get_ms_corresponding_descript(activity: str) -> str:
        """Returns description of the passed activity."""
        master_ms_tuple = data.DESCRIPT_DICT[activity]
        
        ms_act_descript = get_ms_from_tuple(master_ms_tuple)
        return ms_act_descript


    @staticmethod
    @log_func_name
    def get_ms_overall_act_descript() -> str:
        """Returns description of overall activities.
        
        Triggered if activity slot is not resolved."""
        master_ms_tuple = data.MMT_GEN_DESCRIPT
        ms_gen_descript = get_ms_from_tuple( master_ms_tuple)
        return ms_gen_descript


    ##########
    # Attributes
    ##########
    @staticmethod
    @log_func_name
    def set_attr(handler_input, activity: str):
        """Sets `yes` attr to point to the activity asked about."""
        attr = handler_input.attributes_manager.session_attributes
        if activity:
            attr['yes'] = activity 
        
        attr['help_pointer'] = 'act_descript'
        return

    
    ##########
    # Prompts= to play activity.
    ##########
    @staticmethod
    @log_func_name
    def get_q_play_activity(activity: str = None) -> str:
        """Returns prompt asking user if they want to play activity.
        
        If no activity, returns prompt what to do."""
        if not activity:
            return HelpUtils.get_q_what_todo()
        
        ms_want_to_play = get_ms_from_tuple( data.MMT_WANT_TO_PLAY)
        activity = aux_data.skill_data.MODE_ACT_DICT[activity]

        speech_list = (
            ms_want_to_play,
            " ",
            activity,
            "?",
        )
        return ''.join(speech_list)

