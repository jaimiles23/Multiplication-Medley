"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-23 12:23:41
 * @modify date 2020-06-16 17:13:10
 * @desc [
    Practice Manager Class to determine the type of practice.
    Checks:
    - Incorrect problems
    - High error tables
    - Relatively high error tables
 ]
 */
"""

##########
# Imports
##########

import datetime
from statistics import mean, stdev

from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from aux_utils.time_encoder import TimeEncoder
from aux_utils.z_score import calc_z_score

from custom_practice.cp_attr import CP_Attr
import custom_practice.data


##########
# Practice Manager class
##########

class CP_PracticeType(object):

    ##########
    # Get Practice type -- Master
    ##########
    @staticmethod
    @log_func_name
    def get_practice_type(
        handler_input, 
        allow_incorrect_problems: bool = False
        ) -> str:
        """Returns string representing the type of practice for user.

        Loops through conditions and return practice type if true.
        
        Optional allow_incorrect_problems: bool parameter. This is used to skip 
        check_incorrect_problems practice type.
        """

        COND_AND_PRACT_TYPE = (
            (CP_PracticeType.check_incorrect_problems,  custom_practice.data.PRACT_TYPES[0]),
            (CP_PracticeType.check_high_error_tables,   custom_practice.data.PRACT_TYPES[1]),
            (CP_PracticeType.check_high_err_z_score,    custom_practice.data.PRACT_TYPES[2]),
        )
        for i in range(len(COND_AND_PRACT_TYPE)):
            if (i == 0) and (not allow_incorrect_problems):
                continue

            condition, practice_type = COND_AND_PRACT_TYPE[i]
            if condition(handler_input):
                return practice_type
        
        return custom_practice.data.PRACT_TYPES[-1]     # new_tables key.


    ##########
    # Check Incorrect Problems
    ##########
    @staticmethod
    @log_func_name
    def check_incorrect_problems(handler_input) -> bool:
        """Returns bool indicating if there are questions to ask."""
        attr = handler_input.attributes_manager.session_attributes

        wrong_quest_by_date = attr['wrong_quest_by_date']
        wrong_quest_by_date = CP_PracticeType.del_old_date_dicts(wrong_quest_by_date)

        return len(wrong_quest_by_date.keys()) != 0


    @staticmethod
    @log_func_name
    def del_old_date_dicts(wrong_quest_by_date: dict) -> dict:
        """Deletes dict keys and values that are older than limit."""
        today = datetime.date.today()

        for date_key in wrong_quest_by_date.keys():
            date = TimeEncoder.convert_str_to_date(date_key)
            age = today - date

            if age.days > custom_practice.data.ALLOWED_MAX_DICT_AGE:
                del wrong_quest_by_date[date_key]

        return wrong_quest_by_date


    ##########
    # Check High Error Tables
    ##########
    @staticmethod
    @log_func_name
    def check_high_error_tables(handler_input) -> bool:
        """Returns boolean if high error tables are present.
        
        Check 1st element's mean error. 
        NOTE: tbl_list_mean_errs is reverse sorted."""
        attr = handler_input.attributes_manager.session_attributes
        tbl_list_mean_errs = attr['tbl_list_mean_errs']
        
        if tbl_list_mean_errs[0][1] > custom_practice.data.HIGH_ERR_THRESHOLD:
            return True
        return False


    ##########
    # Check High Relative Errors
    ##########
    @staticmethod
    @log_func_name
    def check_high_err_z_score(handler_input) -> bool:
        """Returns if high error z-score table is present.
        
        NOTE: Should probably save tbl error means list as session attr."""
        attr = handler_input.attributes_manager.session_attributes
        tbl_list_mean_errs = attr['tbl_list_mean_errs']

        tbl_means_only = [val[1] for val in tbl_list_mean_errs]
        total_err_mean = mean(tbl_means_only)
        total_err_stdev = stdev(tbl_means_only, xbar= total_err_mean)
        total_err_stdev = total_err_stdev if total_err_stdev else 1

        first_z_score = calc_z_score( 
            data_point = tbl_list_mean_errs[0][1], 
            data_mean = total_err_mean,
            data_stdev = total_err_stdev,
            )

        if first_z_score > custom_practice.data.HIGH_Z_SCORE_ERR:
            return True
        return False

