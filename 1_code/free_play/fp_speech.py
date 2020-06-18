"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-08 11:11:05
 * @modify date 2020-05-17 16:57:06
 * @desc [
    FrePlaySpeech Utility class with methods to get messages for::
    - Welcome
    - Answered all questions
    - Free play parameters
    - Exit
 ]
 */
"""

##########
# Imports
##########

import random


from logs import log_func_name, logger
from slots.slot_utils import SlotUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.list_to_speech import get_str_from_list
from aux_utils.try_saying import get_ms_try_saying
from pause.pauser import Pauser
from players.players_dict import PlayerDict

import free_play.data
from free_play.fp_attr import FreePlayAttr
from aux_data.SSML_tags import MW_EXCITED_LOW


##########
# FreePlaySpeechUtils
##########

class FPSpeech(object):

    ##########
    # Welcome
    ##########
    @staticmethod
    @log_func_name
    def get_ms_welcome(handler_input) -> str:
        """Returns welcome message for Free Play mode."""
        player = PlayerDict.load_player_obj(handler_input)

        if player.fp_plays in [0, 1]:
            ms_welcome = free_play.data.MS_FP_FIRST_WELCOME
        elif not player.fp_plays % 4:
            ms_welcome = free_play.data.MS_FP_INCLUDE_PARAMS
        else:
            ms_welcome = free_play.data.MS_FP_WELCOME
        return MW_EXCITED_LOW.format(ms_welcome)


    ##########
    # Answered All questions
    ##########
    @staticmethod
    @log_func_name
    def get_ms_answered_all_questions(num_questions: int) -> str:
        """Returns message that answered all requested questions."""
        ms_num = free_play.data.MS_NUM.format(num_questions)
        speech_list = (
            free_play.data.MT_DET,
            ms_num,
            free_play.data.MT_PROBLEM_SYNS,
            free_play.data.MT_REQUESTED,
        )
        return get_ms_from_tuple(speech_list)
    

    ##########
    # Free Play Parameters
    ##########
    @staticmethod
    @log_func_name
    def get_ms_fp_parameters(handler_input) -> str:
        """Returns message about the current free play parameters."""
        fp_param_dict = FreePlayAttr.get_fp_parameters(handler_input)

        num_questions = fp_param_dict['num_questions']
        if num_questions:
            ms_ask_q = free_play.data.MS_ASK_NUM_Q.format(num_questions)
        else: 
            ms_ask_q =  free_play.data.MS_ASK_Q
        
        times_tables = fp_param_dict['times_tables']
        if not times_tables:
            times_tables = [" You have not set any times tables"]
        else:
            times_tables = [str(table) for table in times_tables]
        ms_tables = ''.join(
            [free_play.data.MS_FROM_TABLES, ', and '.join(times_tables), '.']
        )

        lower_b, upper_b = fp_param_dict['lower_bound'], fp_param_dict['upper_bound']
        if lower_b is not None and upper_b is not None:
            ms_bound = free_play.data.MS_LOWER_UPPER_BOUND.format(lower_b, upper_b)
        elif lower_b is not None:
            ms_bound = free_play.data.MS_LOWER_BOUND.format(lower_b)
        elif upper_b is not None:
            ms_bound = free_play.data.MS_UPPER_BOUND.format(upper_b)
        else:
            ms_bound = ''
        
        speech_list = (ms_ask_q, ms_tables, ms_bound)
        logger.debug(speech_list)
        return ' '.join(speech_list)


    ##########
    # Exit
    ##########
    @staticmethod
    @log_func_name
    def get_ms_stop_fp() -> str:
        """Returns message done playing free_play."""
        return get_ms_from_tuple( free_play.data.MMT_STOP_FP)

