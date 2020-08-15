"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-21 11:55:58
 * @modify date 2020-06-16 23:33:58
 * @desc [
    SC_Difficulty class with methods to set speed challenge difficulty:
    - Ask for difficulties
    - Acknowledge difficulty message.
 ]
 */
"""

##########
# Imports
##########

from statistics import mean
import random


from logs import log_func_name, logger
from aux_utils.create_tuple_message_clauses import get_linear_nlg
from pause.pauser import Pauser

import speed_challenge.data


##########
# Imports
##########

class SC_Difficulty(object):

    ##########
    # Ask for Difficulty
    ##########

    @staticmethod
    @log_func_name
    def get_q_sc_difficulty(player_object, ) -> str:
        """Master method to return what difficulty prompt."""
        sc_plays = player_object.sc_plays
        speech_list = []

        if sc_plays < 2:
            ms_difficulty_list = SC_Difficulty.get_ms_difficulty_list()
            ms_get_help = SC_Difficulty.h_get_ms_can_ask_help()

            speech_list += Pauser.make_ms_pause_level_list(
                ms_difficulty_list, 2.1, ms_get_help, 1.75)

        q_what_difficulty = SC_Difficulty.h_get_ms_what_difficulty()
        speech_list.append(q_what_difficulty)

        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def h_get_ms_what_difficulty() -> str:
        """Helper method returns prompt asking what difficulty."""
        return get_linear_nlg(
            speed_challenge.data.MMT_WHAT_DIFFICULTY)


    @staticmethod
    @log_func_name
    def get_ms_difficulty_list() -> str:
        """Returns message of list of difficulties user can select."""
        return get_linear_nlg(
            speed_challenge.data.MMT_CAN_USE_DIFF)


    @staticmethod
    @log_func_name
    def h_get_ms_can_ask_help() -> str:
        """Tells the user to ask for help to hear about the difficulties."""
        return speed_challenge.data.MS_GET_DIFF_HELP


    @staticmethod
    @log_func_name
    def get_ms_not_register() -> str:
        """Returns message that did not register user's input."""
        return get_linear_nlg(
            speed_challenge.data.MTT_TRY_AGAIN)


    ##########
    # Acknowledge Difficulty
    ##########
    @staticmethod
    @log_func_name
    def get_ms_using_difficulty(difficulty: str) -> str:
        """Returns message that will use difficulty."""
        ms_use = random.choice(
            speed_challenge.data.MT_USE)
        ms_difficulty = speed_challenge.data.MS_DIFFICULTY_FORMAT.format(
            difficulty)
        return ' '.join([ms_use, ms_difficulty])

