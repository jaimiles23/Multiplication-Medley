"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 15:09:25
 * @modify date 2020-05-05 15:09:25
 * @desc [
     RepeatUtils class to get most recent response.
 ]
 */
"""

##########
# Imports
##########

import json


from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_model import ui, Response


from logs import logger, log_func_name


##########
# RepeatUtils
##########

class RepeatUtils(object):
    @staticmethod
    @log_func_name
    def get_recent_response(handler_input):
        """Returns last response object sent."""
        attr = handler_input.attributes_manager.session_attributes

        cached_response_str = json.dumps(attr['recent_response'])
        cached_response = DefaultSerializer().deserialize(
            cached_response_str, Response)
        return cached_response

