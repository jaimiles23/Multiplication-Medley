"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 11:34:51
 * @modify date 2020-05-06 17:48:56
 * @desc [
    Utility class for confirmation methods. Methods for:
        - get confirmation
        - get player confirmation
        - get random confirmation
 ]
 */
"""

##########
# Imports
##########

import random

from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name
from . import data_confirm


##########
# Confirmation Utility class
##########

class ConfirmUtils(object):

    @staticmethod
    @log_func_name
    def get_confirmation(punct: bool = False) -> str:
        """Returns confirmation statement."""
        confirm = random.choice( data_confirm.MT_CONFIRMATION)
        if punct:
            confirm += "."
        return confirm


    @staticmethod
    @log_func_name
    def get_player_confirmation(handler_input) -> str:
        """Returns confirmation statement with playername."""
        attr = handler_input.attributes_manager.session_attributes
        confirmation = ConfirmUtils.get_confirmation(punct = False)
        player_name = attr['current_player']

        speech_list = [
            confirmation,
            " ",
            player_name,
            "."
        ]
        return ''.join(speech_list)


    @staticmethod
    @log_func_name
    def get_random_confirmation(handler_input, freq_player_name: float = 0.5) -> str:
        """Returns confirmation w/ or w/o player_name."""
        if random.random() > (1 - freq_player_name):
            return ConfirmUtils.get_player_confirmation(handler_input)
        
        return ConfirmUtils.get_confirmation(punct=True)

