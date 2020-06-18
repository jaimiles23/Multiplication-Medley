"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-25 12:01:40
 * @modify date 2020-05-25 12:01:40
 * @desc [
    CP_Utils methods to manage custom practice:
    - get_oldest_date
    - reduce_num_incorrect
    
 ]
 */
"""

##########
# Imports
##########

from math import sqrt

from logs import logger, log_func_name, log_all

from ask_sdk_core.handler_input import HandlerInput



##########
# Custom Practice Utility Class
##########

class CP_Utils(object):
    @staticmethod
    @log_func_name
    def get_oldest_date(wrong_quest_by_date: dict) -> str:
        """Returns the oldest date key for wrong_questions_by_date."""
        date_keys = list(wrong_quest_by_date.keys())
        date_keys.sort()

        log_all(date_keys)
        return date_keys[-1]        # most recent dates 1st.

    @staticmethod
    @log_func_name
    def reduce_num_incorrect(num_incorrect: int) -> int:
            """Uses formula to return reduced number incorrect."""
            return int( sqrt(num_incorrect + 1))