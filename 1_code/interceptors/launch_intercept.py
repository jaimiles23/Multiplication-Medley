"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 10:03:48
 * @modify date 2020-05-24 14:03:21
 * @desc [
    Launch interceptor to load persistent and session attributes when opening skill.
]
*/"""


##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor


from logs import logger, log_func_name 
from attr_mngment.persist_attr_manager import PersistAttrMnger
from attr_mngment.sesh_attr_manager import SessionAttrMnger
import launch.data as data



##########
# Launch Interceptor
##########

class LaunchRequestInterceptor(AbstractRequestInterceptor):
    """Loads necessary session attributes from s3 bucket during launch."""
    def process(self, handler_input):
        # type (HandlerInput) -> None
        if handler_input.request_envelope.session.new != True:
            return
        
        logger.debug("LaunchRequestInterceptor")
        PersistAttrMnger.load_persist_attr(handler_input)
        SessionAttrMnger.load_session_attr(handler_input)

        SessionAttrMnger.set_pointer_attr(handler_input)

        return




