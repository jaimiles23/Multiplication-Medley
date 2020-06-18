"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 14:14:31
 * @modify date 2020-05-26 15:27:10
 * @desc [
    ExitUtils class manage attributes when user stops skill:
    - exit_skill_attr_mngment
    - update_player_mode_stats
    - session performance - TODO
    - ms exit game.
]*/
"""


##########
# Imports
##########

import random


from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from stats.user_stats import UserStats
from stats.mode_stats import ModeStats

from attr_mngment.persist_attr_manager import PersistAttrMnger
import exit_skill.data as data


##########
# ExitUtils
##########

class ExitUtils(object):
    """Methods related to exiting the skill."""

    @staticmethod
    @log_func_name
    def exit_skill_attr_management(handler_input) -> None:
        """Saves persistent attributes for  """
        PersistAttrMnger.save_persist_attr(handler_input)
        handler_input.attributes_manager.session_attributes = None

        return None
    

    @staticmethod
    @log_func_name
    def update_player_mode_statistics(handler_input, player_obj: object) -> None:
        """Updates relevant mode statistics."""
        attr = handler_input.attributes_manager.session_attributes
        mode = attr.get('mode', None)
        
        if mode:
            correct, _ = ModeStats.get_mode_stats(handler_input, mode)
        else:
            correct = 0

        MODE_FUNC_DICT = {
            'free_play'     :   UserStats.update_player_fp_stats,
            'custom'        :   UserStats.update_player_cp_stats,
            'speed'         :   UserStats.update_player_sc_stats,
            'survival'      :   UserStats.update_player_sm_stats,
        }
        update_stats_func = MODE_FUNC_DICT.get(mode, None)
        log_all( update_stats_func, correct)

        if (update_stats_func) and (correct > 4):
            update_stats_func(handler_input, player_obj)

        return None


    @staticmethod
    @log_func_name
    def get_ms_session_performance(handler_input) -> str:
        """Returns message about the player's performance in the session.

        TODO
            - Come back and practice the problems you got wrong!
            - Nice job setting new highscore today!             
            - You solved 100 problems today!              
        """
        return ' '


    @staticmethod
    @log_func_name
    def get_ms_exit_game():
        """Returns message for exiting the game."""
        return random.choice( data.MT_EXIT)
    


