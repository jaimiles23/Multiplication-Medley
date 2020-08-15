"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 09:08:15
 * @modify date 2020-05-22 22:07:29
 * @desc [
    LaunchUtils class for launch handler with methods for:
    - Welcome messages
    - Prompts
    - Reprompts
    - Attributes
]
*/
"""

##########
# Imports
##########

import random


from logs import logger, log_func_name 
from helper.help_utils import HelpUtils
from pause.pauser import Pauser
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple

import launch.data as data
from aux_data.SSML_tags import MW_EXCITED_LOW


##########
# Launch Utility Class
##########

class LaunchUtils(object):
    """Utility methods for Launch request."""

    ##########
    # Welcome Messages
    ##########
    @staticmethod
    @log_func_name
    def get_welcome(handler_input) -> str:
        """Determines & calls the appropriate welcome function."""
        attr = handler_input.attributes_manager.session_attributes
        current_player = attr.get('current_player', None)
        logins = int(attr['logins'])

        if logins == 1 or not current_player:
            return LaunchUtils.get_first_welcome()
        
        elif logins == 2:
            return (
                LaunchUtils.get_welcome_back_player_name(current_player) + 
                HelpUtils.get_ms_help_overview())
        
        elif logins in [7, 20, 50]:
            return LaunchUtils.get_welcome_rate_skill(current_player)
        
        return LaunchUtils.get_welcome_back_player_name(current_player)


    @staticmethod
    @log_func_name
    def get_first_welcome() -> str:
        """Returns first welcome message for skill."""
        return data.MS_FIRST_WELCOME


    @staticmethod
    @log_func_name
    def get_welcome_back_player_name(current_player: str) -> str:
        """Returns welcome back message with player_name"""
        ms_welcome_back = random.choice(
            data.MT_WELCOME_BACK_PLAYER).format(current_player)

        return MW_EXCITED_LOW.format(ms_welcome_back)


    @staticmethod
    @log_func_name
    def get_welcome_rate_skill(current_player) -> str:
        """Returns welcome message asking the user to rate the skill."""
        ms_welcome_back = LaunchUtils.get_welcome_back_player_name(current_player)
        ms_rate_skill = data.MS_WELCOME_RATE_SKILL
        speech_list = (
            ms_welcome_back,
            Pauser.get_p_level(1),
            ms_rate_skill,
            Pauser.get_p_level(1),
        )
        return ' '.join(speech_list)


    ##########
    # Prompts
    ##########
    @staticmethod
    @log_func_name
    def get_q_prompt(handler_input) -> str:
        """Determines & returns appropriate question prompt for the user."""
        attr = handler_input.attributes_manager.session_attributes
        current_player = attr.get('current_player', None)

        if not current_player:
            return LaunchUtils.get_q_player_name()

        return HelpUtils.get_q_what_todo()


    @staticmethod
    @log_func_name
    def get_q_player_name() -> str:
        """Returns prompt asking for the player's name."""
        return get_ms_from_tuple( data.MTT_FIRST_PLAYER_NAME)


    ##########
    # Reprompts
    ##########
    @staticmethod
    @log_func_name
    def get_r_appropriate_reprompt(handler_input) -> str:
        """Returns launch reprompt."""
        attr = handler_input.attributes_manager.session_attributes
        current_player = attr.get('current_player', None)
        if not current_player:
            return LaunchUtils.get_r_player_name()
        
        ms_overview = HelpUtils.get_ms_help_overview()
        q_todo = HelpUtils.get_q_what_todo()
        speech_list = (
            ms_overview,
            1,
            q_todo
        )
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_r_player_name() -> str:
        """Returns reprompt asking for the player's name."""
        return data.MS_FIRST_PLAY_NAME_REPROMPT
    

    ##########
    # Attributes
    ##########

    @staticmethod
    @log_func_name
    def set_launch_attr(handler_input) -> str:
        """Sets session attributes for the LaunchIntent"""
        attr = handler_input.attributes_manager.session_attributes
        attr['logins'] += 1
        current_player = attr.get('current_player', None)

        if not current_player:
            attr['next_handler'] = 'create_profile'
            attr['help_pointer'] = 'user_profile'

        return

