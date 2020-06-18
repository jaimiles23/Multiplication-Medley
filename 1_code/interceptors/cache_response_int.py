"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 15:13:41
 * @modify date 2020-05-05 15:15:56
 * @desc [
    Response Interceptor to cache the last response.
 ]
 */"""


##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_core.utils import is_request_type
from ask_sdk_model import Response


from logs import logger, log_func_name


##########
# Repeat Interceptor
##########

class CacheResponseForRepeatInterceptor(AbstractResponseInterceptor):
    '''Cache the response sent to the user during session. 
    This can be used to repeat the response back to the user when
    the RepeatIntent is triggered.
    '''
    def process(self, handler_input, response):
        # type (HandlerInput, Response) -> None
        ## can probably move this to a utility function for other interceptors too
        if (
            (handler_input.request_envelope.session.new == True) or
            (is_request_type("SessionEndedRequest")(handler_input)) or
            not response
            ):
            return

        logger.debug("INTER:    CacheResponseForRepeatInterceptor")
        try: 
            handler_input.attributes_manager.session_attributes['recent_response'] = response
        except Exception as e:
            logger.warning(f"""INTER:   CacheResponseForRepeatInterceptor
            Could not cache repeated response:  {e}""")
            pass
        return
