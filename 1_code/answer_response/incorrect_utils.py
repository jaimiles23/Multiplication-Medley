"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-15 16:28:53
 * @modify date 2020-06-16 14:25:26
 * @desc [
    Utility class for response to incorrect answer.
        - Incorrect buzzer & exclamation
        - Incorrect exclamation
        - Incorrect buzzer
 ]
 */
"""

##########
# Imports
##########

import random

from logs import log_func_name, logger

from . import data_incorrect


##########
# IncorrectAnsUtils
##########

class IncorrectAnsUtils(object):

    @staticmethod
    @log_func_name
    def get_buzz_and_incorrect() -> str:
        """Returns incorrect buzz & incorrect message."""
        return (
            IncorrectAnsUtils.get_buzzer() +
            IncorrectAnsUtils.get_ms_incorrect()
        )


    @staticmethod
    @log_func_name
    def get_ms_incorrect() -> str:
        """Returns message that the answer was incorrect."""
        return random.choice( 
            data_incorrect.MT_INCORRECT)


    @staticmethod
    @log_func_name
    def get_buzzer() -> str:
        """Returns buzzer for incorrect response."""
        return data_incorrect.INCORRECT_BUZZ

