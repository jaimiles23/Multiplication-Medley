"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-25 22:22:09
 * @modify date 2020-05-26 12:53:22
 * @desc [
     Utility class with methods to return message for ending custom practice activities.
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
class CP_PractEnd(object):

    @staticmethod
    @log_func_name
    def get_ms_practice_type_end(handler_input, practice_type: str) -> str:
        """Returns message that user completed practice type."""
        logger.debug(practice_type)
        
        TYPE_END_MESS_DICT = {
            custom_practice.data.PRACT_TYPES[0]     :   CP_PractEnd.get_ms_fin_incorrect,
            custom_practice.data.PRACT_TYPES[1]     :   CP_PractEnd.get_ms_fin_high_err_table,
            custom_practice.data.PRACT_TYPES[2]     :   CP_PractEnd.get_ms_fin_high_z_score_table,
            custom_practice.data.PRACT_TYPES[3]     :   CP_PractEnd.get_ms_fin_new_tables,
        }
        return TYPE_END_MESS_DICT[practice_type]()
    

    @staticmethod
    @log_func_name
    def get_ms_fin_incorrect() -> str:
        """Returns message that user solved all stored incorrect problems."""
        return MW_EXCITED_LOW.format(
            get_ms_from_tuple(
                custom_practice.data.MMT_FIN_INCORRECT_PROBLEMS))


    @staticmethod
    @log_func_name
    def get_ms_fin_high_err_table() -> str:
        """Returns message that user solved all high error tables."""
        return MW_EXCITED_LOW.format(
            get_ms_from_tuple(
                custom_practice.data.MMT_HIGH_ERROR_TABLES))


    @staticmethod
    @log_func_name
    def get_ms_fin_high_z_score_table() -> str:
        """Returns message that user solved all high z score tables."""
        return MW_EXCITED_LOW.format(
            get_ms_from_tuple(
                custom_practice.data.MMT_HIGH_Z_SCORE_TABLES))


    @staticmethod
    @log_func_name
    def get_ms_fin_new_tables() -> str:
        """Returns message that user solved new table problems."""
        return MW_EXCITED_LOW.format(
            get_ms_from_tuple(
                custom_practice.data.MMT_NEW_TABLES))
    
