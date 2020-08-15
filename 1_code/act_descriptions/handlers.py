"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-07 11:12:39
 * @modify date 2020-08-15 14:37:39
 * @desc [
    Handlers for Act Description intents:
        - ActDescriptHandler
        - Handles requests to describe activities
        - Optional slot to include activity
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
from act_descriptions.act_descript_utils import DescriptUtils
from pause.pauser import Pauser
from slots.slot_utils import SlotUtils
from skill_card.card_funcs import CardFuncs


##########
# ActDescript Handler
##########

class ActDescriptHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("DescribeActivityIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("HAN    ActDescriptHandler")
        speech_list = []

        activity = SlotUtils.get_resolved_value( handler_input, "activity")

        if not activity:
            logger.info("ActDescriptHandler: Non-resolved activity.")
            ms_overall_descript = DescriptUtils.get_ms_overall_act_descript()
            speech_list.append( ms_overall_descript)
        
        else:
            DescriptUtils.set_attr(handler_input, activity)
            ms_act_descript = DescriptUtils.get_ms_corresponding_descript(activity)
            speech_list.append( ms_act_descript)
        
        prompt, reprompt = (
            DescriptUtils.get_q_play_activity(activity) for _ in range(2))
        prompt = CardFuncs.format_prompt(prompt)
        speech_list.append( Pauser.get_p_level(4))
        speech_list.append(prompt)

        speech = ' '.join(speech_list)
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)

        return (
            handler_input.response_builder
                .speak( speech)
                .ask( reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

