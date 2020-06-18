"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 14:38:23
 * @modify date 2020-05-06 14:38:23
 * @desc [
    ExceptionUtils for exception utility methods.

    get_ms_next_handler_exception(handler_input) -> str:
        "Returns message when exception in `next_handler`."
    
    create_response_next_handler_exc(handler_input) -> str:
        "Returns exception response when error in next_Handler"
 ]
 */
"""

##########
# Imports
##########

import random


from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import logger, log_func_name
from skill_card.card_funcs import CardFuncs
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
import exceptions.data as data


##########
# Exception Utility methods
##########

class ExceptionUtils(object):
    ## Decided to keep response objects assinged to handlers
    pass
