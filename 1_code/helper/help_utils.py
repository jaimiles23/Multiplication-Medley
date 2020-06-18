"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 12:43:22
 * @modify date 2020-05-23 10:38:27
 * @desc [
    HelpUtils utility class with methods for:
    - help messages
    - general utility methods
    - 
]
*/"""

##########
# Imports
##########

import random


from logs import logger, log_func_name
from pause.pauser import Pauser
from skill_card.card_funcs import CardFuncs
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.list_to_speech import get_str_from_list
from aux_utils.try_saying import get_ms_try_saying
from free_play.fp_timestables import FPTimesTables
from free_play.fp_upp_lower_bounds import FPUpperLowerBounds

import helper.data
import aux_data.skill_data
import act_descriptions.data
    

##########
# Helper Utility class
##########

class HelpUtils(object):
    """Contains methods associated with the HelpHandler."""
    
    ##########
    # Help Messages
    ##########
    @staticmethod
    @log_func_name
    def get_ms_corresponding_help(handler_input) -> str:
        """Returns corresponding help message depending on mode.
        
        TODO:
            - Add other help pointers & corresponding functions.
            - Add corresponding prompts, etc for other functions.
        """
        attr = handler_input.attributes_manager.session_attributes
        help_pointer = attr.get('help_pointer', 'overview')
        logger.debug(f"help_pointer {help_pointer}")

        HELP_MS_POINTER_DICT = {
            'overview'          :   HelpUtils.get_ms_help_overview,
            'user_profile'      :   HelpUtils.get_ms_user_profile,
            'act_descript'      :   HelpUtils.get_ms_act_descript,
            'free_play'         :   HelpUtils.get_ms_free_play,
            'fp_input'          :   HelpUtils.get_ms_fp_table_input,
            'custom_practice'   :   HelpUtils.get_ms_custom_practice,
            'survival_mode'     :   HelpUtils.get_ms_survival_mode,
            'speed_challenge'   :   HelpUtils.get_ms_speed_challenge,
        }
        try:
            ms_help_func = HELP_MS_POINTER_DICT[help_pointer]
        except KeyError:
            logger.warning(f"get_ms_corresponding_help: KeyError    {help_pointer}")
            ms_help_func = HelpUtils.get_ms_act_descript
        return ms_help_func()


    @staticmethod
    @log_func_name
    def get_ms_help_overview() -> str:
        """Returns help message for overview of skill."""
        ms_help_overview = get_ms_from_tuple( helper.data.MT_HELP_OVERVIEW)
        ms_skill_acts = HelpUtils.get_skill_acts()

        speech_list = (
            ms_help_overview,
            0.75,
            ms_skill_acts,
            2.25,
            act_descriptions.data.MS_START_OR_ASK
        )
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_user_profile() -> str:
        """Returns help message for user profile."""
        return get_ms_from_tuple(
            helper.data.MT_HELP_USER_PROFILE)


    @staticmethod
    @log_func_name
    def get_ms_act_descript() -> str:
        """Returns help message for activity description."""
        master_ms_tuple = act_descriptions.data.MMT_GEN_DESCRIPT
        ms_gen_descript = get_ms_from_tuple( master_ms_tuple)
        return ms_gen_descript


    @staticmethod
    @log_func_name
    def get_ms_fp_table_input() -> str:
        """Returns helps message for providing freeplay table parameters."""
        speech_list = [ 
            helper.data.MS_FP_TIMES_TABLES,
            Pauser.get_p_level(1),
            get_ms_try_saying(),
            ]
        if random.random() < 0.25:
            speech_list.append( FPTimesTables.get_example_tables_query())
        else:
            speech_list.append( FPTimesTables.get_example_table_range())

        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_free_play() -> str:
        """Returns helps message for freeplay game mode."""
        speech_list = (
            helper.data.MS_FP_OVERVIEW,
            Pauser.get_p_level(0.5),
            helper.data.MS_FP_STD_PARAMS,
            Pauser.get_p_level(1.5),
            FPUpperLowerBounds.get_ms_can_change_table_bounds()
        )
        return ' '.join(speech_list)
    

    @staticmethod
    @log_func_name
    def get_ms_custom_practice() -> str:
        return get_ms_from_tuple(
            helper.data.MMT_CUSTOM_PRACTICE)
    
    
    @staticmethod
    @log_func_name
    def get_ms_survival_mode() -> str:
        return get_ms_from_tuple(
            helper.data.MTT_SURVIVAL_MODE)
    

    @staticmethod
    @log_func_name
    def get_ms_speed_challenge() -> str:
        return get_ms_from_tuple(
            helper.data.MMT_SPEED_CHALLENGE)
    

    ##########
    # General Utility Methods
    ##########
    @staticmethod
    @log_func_name
    def get_q_what_todo() -> str:
        """Returns prompt asking the user what they want to do."""
        ms_what_todo = random.choice( helper.data.MT_WHAT_TODO)
        ms_what_todo = CardFuncs.format_prompt( ms_what_todo)
        return ms_what_todo


    @staticmethod
    @log_func_name
    def get_skill_acts() -> str:
        """Returns string of skill activities"""
        return get_str_from_list( aux_data.skill_data.MT_SKILL_ACTS)
    

    @staticmethod
    @log_func_name
    def get_q_user_profile() -> str:
        """Returns prompt asking for the user's name."""
        prompt = helper.data.MS_FIRST_PLAY_NAME_REPROMPT
        return CardFuncs.format_prompt(prompt)

