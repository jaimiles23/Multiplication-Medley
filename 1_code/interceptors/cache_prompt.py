"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-11 14:13:17
 * @modify date 2020-06-16 18:05:29
 * @desc [
    Interceptor used to cache the reprompt incase user exits flow of skill.

    Cache is referenced when the user calls an auxiliary menu, e.g., help or adjusttime,
    and then needs to be redirected to an activity.
 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type

from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
from ask_sdk_model import Response


from logs import logger
from aux_utils.last_prompt import LastPrompt


##########
# Cache Reprompt Interceptor
##########

class CacheRepromptInterceptor(AbstractResponseInterceptor):
    """Cache reprompt from the response sent to the user during the session.

    This is used to repeat the prompt back to the user when a one-shot
    auxiliary handler is called next.
    """
    def process(self, handler_input, response):
        # type (HandlerInput, Response)
        if (
            (handler_input.request_envelope.session.new == True) or
            is_request_type("SessionEndedRequest")(handler_input) or
            not response
        ):
            return

        try:
            prompt = response.reprompt.output_speech.ssml
            LastPrompt.save_last_prompt_str(handler_input, prompt)
        except Exception as e:
            logger.warning(f"CacheRepromptInterceptor   {e}")
        return



