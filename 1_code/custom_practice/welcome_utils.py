"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-23 12:29:55
 * @modify date 2020-05-27 11:31:11
 * @desc [
    CP_Welcome with methods to welcome user to custom practice.
 ]
 */
"""

##########
# Imports
##########

import random

from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple

from aux_data.SSML_tags import MW_EXCITED_LOW
import custom_practice.data


##########
# Welcome Utility class
##########

class CP_Welcome(object):

    @staticmethod
    @log_func_name
    def get_ms_welcome(handler_input, player_obj: object) -> str:
        """Returns welcome message to the user."""
        cp_plays = player_obj.cp_plays

        if cp_plays == 0:
            ms_welcome = CP_Welcome.get_ms_first_welcome()

        elif cp_plays in (1, 2):
            ms_welcome = CP_Welcome.get_ms_long_welcome()

        elif random.random() < 0.5:
            ms_welcome = CP_Welcome.get_ms_short_welcome()

        else:
            ms_welcome = CP_Welcome.get_ms_long_welcome()
        
        return MW_EXCITED_LOW.format( ms_welcome)
    

    @staticmethod
    @log_func_name
    def get_ms_first_welcome() -> str:
        """Returns first welcome message for the user."""
        return get_ms_from_tuple(
            custom_practice.data.MMT_FIRST_WELCOME)
    

    @staticmethod
    @log_func_name
    def get_ms_long_welcome() -> str:
        """Returns long welcome message to the user."""
        return get_ms_from_tuple(
            custom_practice.data.MMT_LONG_WELCOME)
    

    @staticmethod
    @log_func_name
    def get_ms_short_welcome() -> str:
        """Returns short welcome message to the user."""
        return get_ms_from_tuple(
            custom_practice.data.MMT_SHORT_WELCOME)
    

    ##########
    # Need More data
    ##########
    @staticmethod
    @log_func_name
    def get_ms_need_more_data(questions_answered: int) -> str:
        """Returns message that user needs to answer more questions before playing."""
        ms_answered_so_far = custom_practice.data.MS_ANSWERED_Q_SO_FAR.format(
            questions_answered)
        speech_list = (
            custom_practice.data.MS_MORE_DATA,
            2,
            ms_answered_so_far,
            1,
            custom_practice.data.MS_COME_BACK_AFTER
        )
        return get_ms_from_tuple(speech_list)



