"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 12:43:22
 * @modify date 2020-08-15 14:37:10
 * @desc [
    Help Handler to return help message to the user.
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
from helper.help_utils import HelpUtils
from skill_card.card_funcs import CardFuncs
from pause.pauser import Pauser
from aux_utils.last_prompt import LastPrompt

##########
# Help Handler
##########

class HelpHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    
    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        logger.info("HAN    HelpHandler")
        speech_list = []

        ms_help = HelpUtils.get_ms_corresponding_help(handler_input)
        prompt, reprompt = (
            LastPrompt.get_last_prompt(handler_input) for _ in range(2))

        speech_list += Pauser.make_ms_pause_level_list( ms_help, 3, prompt)

        speech = ' '.join(speech_list)
        
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard(
                    card_title, card_text))
                .response)

