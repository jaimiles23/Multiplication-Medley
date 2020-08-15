"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 13:56:45
 * @modify date 2020-05-15 17:59:46
 * @desc [
     FallbackUtils class with Fallback methods.
     - unknown slots
     - reset session attr - TODO/Think
     - Log fallback
 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import log_func_name, logger
from aux_utils.last_prompt import LastPrompt
from skill_card.card_funcs import CardFuncs
from pause.pauser import Pauser
from aux_utils.create_tuple_message_clauses import get_linear_nlg
from mult_questions.fp_question import FPQuestions
from mult_questions.gen_questions import GenQuestions

import fallback.data


##########
# FallbackUtils
##########

class FallbackUtils(object):

    @staticmethod
    @log_func_name
    def return_unknown_slot_response(handler_input) -> object:
        """If cannot find answer slot, returns same response prompt.
        
        NOTE: Can probably just return last response object.
        """
        speech_list = []
        attr = handler_input.attributes_manager.session_attributes
        
        ms_not_understand = get_linear_nlg( fallback.data.MMT_NOT_UNDERSTAND)
        
        if attr.get('mode', None) == 'free_play':
            prompt, reprompt = (
                GenQuestions.get_same_question(handler_input) for _ in range(2))
        else:
            prompt, reprompt = (
                LastPrompt.get_last_prompt(handler_input) for _ in range(2))
        
        speech_list += Pauser.make_ms_pause_level_list(
            ms_not_understand, 2, prompt)
        
        speech = ' '.join(speech_list)
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask( reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


    @staticmethod
    @log_func_name
    def reset_session_attr(handler_input) -> None:
        """May like to have a function that resets session attributes
        to clean any logic issues??
        
        Note: Will need to save & reload player objs.
        """
        pass


    @staticmethod
    @log_func_name
    def log_fallback_intent(handler_input) -> None:
        """Logs intent name for what intent caused fallback."""
        try:
            intent_name = handler_input.request_envelope.request.intent.name
        except Exception as e:
            intent_name = f"unable to acess intent.name: {e}"
        
        logger.info(f"FB Intent {intent_name}")
        return

