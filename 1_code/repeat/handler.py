"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 15:09:25
 * @modify date 2020-05-06 10:37:05
 * @desc [
    RepeatHandler to return last response.
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


from logs import logger
from repeat.repeat_utils import RepeatUtils
from pause.pauser import Pauser
from skill_card.card_funcs import CardFuncs
from helper.help_utils import HelpUtils

import fallback.data


##########
# Repeat Handler
##########

class RepeatHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.RepeatIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("HAN    RepeatHandler")
        attr = handler_input.attributes_manager.session_attributes
        speech_list = []

        if 'recent_response' in attr:
            return RepeatUtils.get_recent_response(handler_input)


        ms_help = HelpUtils.get_ms_corresponding_help(handler_input)
        ms_prompt, reprompt = (
            HelpUtils.get_ms_corresponding_help(handler_input) for _ in range(2))
                
        speech_list.append( fallback.data.MS_FALLBACK)
        speech_list.append( Pauser.get_p_level(1))

        ## NOTE: This will need refinement if there are callbacks. 
        ## Develop relevant methods from FallbackUtils.
        speech_list.append( ms_help)
        speech_list.append( ms_prompt)

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title( handler_input)
        card_text = CardFuncs.clean_card_text( speech)
        return (
            handler_input.response_builder
                .speak( speech)
                .ask( reprompt)
                .set_card( SimpleCard(
                    card_title, card_text))
                .response)

