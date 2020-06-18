"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-09 11:07:54
 * @modify date 2020-05-13 13:59:44
 * @desc [
    Utility function to provide sample utterance of "Try saying".

 ]
 */
"""

##########
# Imports
##########

import random


##########
# MS Try Saying
##########

def get_ms_try_saying() -> str:
    """Returns message variant for the user to try saying."""
    return random.choice( MT_TRY_SAYING)


##########
# Data
##########

MT_TRY_SAYING = (
    "try saying:",
    "try saying:",
    "you can say:",
)

