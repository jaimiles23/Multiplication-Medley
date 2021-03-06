"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-27 12:01:03
 * @modify date 2020-08-15 14:38:20
 * @desc [
    Handler for AMAZON.NoIntent
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
from aux_utils.create_tuple_message_clauses import get_linear_nlg
from answer_response.confirmation_utils import ConfirmUtils


##########
# No Handler
##########

class NoHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("HAN    NoHandler")

        ms_confirmation = ConfirmUtils.get_confirmation(punct= True)
        prompt = HelpUtils.get_q_what_todo()

        reprompt = HelpUtils.get_ms_help_overview()

        speech_list = (
            ms_confirmation,
            1,
            prompt
        )
        speech = get_linear_nlg(speech_list)
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard(
                    card_title, card_text))
                .response)

