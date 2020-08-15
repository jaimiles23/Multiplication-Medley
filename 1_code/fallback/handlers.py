"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 13:56:45
 * @modify date 2020-08-15 14:37:24
 * @desc [
     Fallback Handler - called when no other handlers can handle event.
 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler

from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import logger, log_func_name
from pause.pauser import Pauser
from skill_card.card_funcs import CardFuncs
from helper.help_utils import HelpUtils
from aux_utils.last_prompt import LastPrompt

from fallback.fallback_utils import FallbackUtils
import fallback.data as data


##########
# FallBack Handler
##########

class FallbackHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            is_intent_name("AMAZON.FallbackIntent")(handler_input)
            or
            True)
    
    def handle(self, handler_input):
        logger.info("HAN    FallbackHandler")
        FallbackUtils.log_fallback_intent(handler_input)
        speech_list = []

        # ms_help = HelpUtils.get_ms_corresponding_help(handler_input)
        ms_prompt, reprompt = (
            LastPrompt.get_last_prompt(handler_input) for _ in range(2))
                
        speech_list.append( data.MS_FALLBACK)
        speech_list.append( Pauser.get_p_level(1))

        ## NOTE: ms_help needs refinement if help after fallback handler.
        ## Develop relevant methods from FallbackUtils.
        # speech_list.append( ms_help)
        speech_list.append( ms_prompt)

        speech = ' '.join(speech_list)
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask( reprompt)
                .set_card( SimpleCard(
                    card_title, card_text))
                .response)

