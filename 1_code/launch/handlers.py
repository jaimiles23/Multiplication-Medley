"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 09:08:15
 * @modify date 2020-08-15 14:37:13
 * @desc [
     LaunchRequestHandler 
]
*/
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import logger, log_func_name
from launch.launch_utils import LaunchUtils
from pause.pauser import Pauser
from skill_card.card_funcs import CardFuncs
from aux_utils.create_tuple_message_clauses import get_linear_nlg


##########
# Launch Request Handler
##########

class LaunchRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input) -> bool:
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self, handler_input):
        logger.info("HAN    LaunchRequestHandler")
        speech_list = []

        ms_welcome = LaunchUtils.get_welcome(handler_input)
        prompt = LaunchUtils.get_q_prompt(handler_input)
        prompt = CardFuncs.format_prompt(prompt)

        speech_list = (
            ms_welcome, 
            1.75,
            prompt
        )

        speech = get_linear_nlg(speech_list)
        reprompt = LaunchUtils.get_r_appropriate_reprompt(handler_input)
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)

        LaunchUtils.set_launch_attr(handler_input)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard(card_title, card_text))
                .response)

