"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-24 18:45:02
 * @modify date 2020-05-26 12:59:44
 * @desc [
    Utility class to say the introduction to each practice:
    - incorrect problems
    - high error problems
    - high relative error problems
    - more difficult tables
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
from aux_utils.list_to_speech import get_str_from_list
from answer_response.congrat_utils import CongratUtils

from aux_data.SSML_tags import MW_EXCITED_LOW

from custom_practice.cp_attr import CP_Attr
import custom_practice.data


##########
# Practice Introduction Utility class
##########

class CP_PractIntro(object):

    @staticmethod
    @log_func_name
    def get_ms_practice_type_intro(handler_input, practice_type: str) -> str:
        """Returns message about type of practice."""
        TYPE_MESS_DICT = {
            custom_practice.data.PRACT_TYPES[0]     :   CP_PractIntro.get_ms_practice_incorrect_problems,
            custom_practice.data.PRACT_TYPES[1]     :   CP_PractIntro.get_ms_practice_high_err_tables,
            custom_practice.data.PRACT_TYPES[2]     :   CP_PractIntro.get_ms_practice_high_zscore_tables,
            custom_practice.data.PRACT_TYPES[3]     :   CP_PractIntro.get_ms_practice_new_tables,
        }
        return TYPE_MESS_DICT[practice_type](handler_input)


    @staticmethod
    @log_func_name
    def get_ms_practice_incorrect_problems(handler_input) -> str:
        """Returns message that going to practice incorrect problems."""
        return get_ms_from_tuple(
            custom_practice.data.MMT_INCORRECT_PROBLEMS_IN_DATES)


    @staticmethod
    @log_func_name
    def get_ms_practice_high_err_tables(handler_input) -> str:
        """Returns message that going to practice high error tables."""
        tables_to_practice = CP_Attr.get_top_high_err_tables(handler_input)
        ms_tables_to_practice = get_str_from_list(tables_to_practice, punct= False)
        ms_times_tables_syn = random.choice(
            custom_practice.data.MT_TIMES_TABLE_SYN) + '.'

        speech_list_1 = list( custom_practice.data.MMT_INCORRECT_PROBLEMS)
        speech_list_2 = [
            ms_tables_to_practice,
            ms_times_tables_syn,
            1,
            custom_practice.data.MMT_PRACTICE_THOSE,
        ]

        speech_list = (speech_list_1 + speech_list_2 + 
            CP_PractIntro.get_ms_num_in_row_to_complete())
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_practice_high_zscore_tables(handler_input) -> str:
        """Returns message to practice high relative error tables."""
        tables_to_practice = CP_Attr.get_top_z_score_err_tables(handler_input)
        ms_tables_to_practice = get_str_from_list(tables_to_practice, punct= False)
        ms_times_tables_syn = random.choice(
            custom_practice.data.MT_TIMES_TABLE_SYN) + '.'

        speech_list_1 = list( custom_practice.data.MMT_HIGH_Z_SCORE)
        speech_list_2 = [
            ms_tables_to_practice,
            ms_times_tables_syn,
            1,
            custom_practice.data.MMT_PRACTICE_THOSE,
        ]

        speech_list = (speech_list_1 + speech_list_2 + 
            CP_PractIntro.get_ms_num_in_row_to_complete())
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_practice_new_tables(handler_input) -> str:
        """Returns message that going to practice new tables outside comfort range."""
        speech_list = list(custom_practice.data.MTT_NEW_TABLES)

        ms_congrats = CongratUtils.get_player_congrats(handler_input, 1)
        speech_list.insert(0, ms_congrats)

        speech_list += CP_PractIntro.get_ms_num_in_row_to_complete()
        return get_ms_from_tuple(speech_list)
    

    @staticmethod
    @log_func_name
    def get_ms_num_in_row_to_complete() -> list:
        """Returns message tuple for number of consecutive correct to complete practice."""
        return list( custom_practice.data.MMT_COMPLETE_PRACTICE)
        
