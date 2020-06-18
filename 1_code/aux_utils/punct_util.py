""""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 14:34:22
 * @modify date 2020-05-06 14:34:22
 * @desc [
   Utility method to get random punctuation (exclamation mark/period.)
 ]
 */
"""
##########
# Imports
##########

import random


from logs import logger, log_func_name


##########
# Punctuation utils
##########

@log_func_name
def get_random_punct() -> str:
    """Randomly returns exclamation or period."""
    punct = ("!", ".")
    return random.choice(punct)

