"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-11 11:54:50
 * @modify date 2020-05-13 16:40:27
 * @desc [
    FPUpperLowerBounds utility class to change the Times Tables bounds.
 ]
 */
"""

##########
# Imports
##########

import random


from logs import log_func_name, logger
from slots.slot_utils import SlotUtils
from aux_utils.create_tuple_message_clauses import get_linear_nlg
from aux_utils.list_to_speech import get_str_from_list
from aux_utils.try_saying import get_ms_try_saying
from pause.pauser import Pauser

import free_play.data
from aux_data.SSML_tags import MW_EXCITED_LOW


##########
# Utility class
##########

class FPUpperLowerBounds(object):

    ##########
    # Table Bounds
    ##########
    @staticmethod
    @log_func_name
    def get_ms_set_table_bounds(lower_bound: int, upper_bound: int) -> str:
        """Returns message about setting upper & lower table bound."""

        if (lower_bound is not None) and (upper_bound is not None):
            return FPUpperLowerBounds.get_ms_set_upper_lower_bounds(lower_bound, upper_bound)
        elif (lower_bound is not None):
            return FPUpperLowerBounds.get_ms_set_lower_bound(lower_bound)
        elif (upper_bound is not None):
            return FPUpperLowerBounds.get_ms_set_upper_bound(upper_bound)
        
        logger.error(f"get_ms_table_range_input: End reached.")
        return ''


    @staticmethod
    @log_func_name
    def get_ms_set_upper_lower_bounds(lower_bound: int, upper_bound: int) -> str:
        """Returns message that user set both upper & lower bound."""
        ms_lower_bound = (random.choice(
            free_play.data.MT_LOWER_BOUND).format(lower_bound))
        ms_upper_bound = (random.choice(
            free_play.data.MT_UPPER_BOUND).format(upper_bound))
        speech_list = (ms_lower_bound, ', and ', ms_upper_bound, '.')
        return ''.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_set_upper_bound(upper_bound: int) -> str:
        """Returns message that user set upper bound."""
        ms_upper_bound = (random.choice(
            free_play.data.MT_UPPER_BOUND).format(upper_bound))
        return ms_upper_bound + '.'


    @staticmethod
    @log_func_name
    def get_ms_set_lower_bound(lower_bound: int) -> str:
        """Returns message that user set lower bound."""
        ms_lower_bound = (random.choice(
            free_play.data.MT_LOWER_BOUND).format(lower_bound))
        return ms_lower_bound + '.'


    @staticmethod
    @log_func_name
    def get_ms_can_change_table_bounds() -> str:
        """Returns message that user can change the lower & upper bound of a table."""
        speech_list = [
            free_play.data.MT_CAN,
            free_play.data.MS_CHANGE_UPPER_LOW_BOUNDS,
            free_play.data.MT_QUESTIONS,
            ]
        return get_linear_nlg( speech_list)


    @staticmethod
    @log_func_name
    def get_q_change_bounds() -> str:
        """Returns prompt that can change the upper/lower bound of the tables."""
        if random.random() > 0.5:
            ## lower bound
            bound_type = "lower",
            bound_num = random.randint(3, 7)
            ml_bound_effect = free_play.data.MT_LOWER_BOUND
        else:
            bound_type = "upper"
            bound_num = random.randint(7, 10)
            ml_bound_effect = free_play.data.MT_LOWER_BOUND
        
        ms_bound_effect = random.choice(ml_bound_effect).format(bound_num)
        ms_to_bound = free_play.data.MT_BOUND_TO.format( bound_type)

        speech_list = (
            get_ms_try_saying(),
            free_play.data.MT_CHANGE,
            bound_type,
            ms_to_bound,
            2,
            ms_bound_effect,
        )
        return get_linear_nlg( speech_list)

