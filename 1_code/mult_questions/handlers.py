"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-17 14:52:34
 * @modify date 2020-05-20 12:32:57
 * @desc [
    Contains handler for non-mode specific intents related to questions:
        - NumQuestionsAnsweredHandler
 ]
 */
"""

##########
# Imports
##########

import random


from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import log_decorators, logger
from pause.pauser import Pauser
from answer_response.confirmation_utils import ConfirmUtils
from aux_utils.last_prompt import LastPrompt
from helper.help_utils import HelpUtils
from skill_card.card_funcs import CardFuncs


import mult_questions.data


##########
# Handlers
##########

class NumQuestionsAnsweredHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("NumQuestionsAnsweredIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("HAN    NumQuestionsAnsweredHandler")
        attr = handler_input.attributes_manager.session_attributes
        speech_list = []

        questions_answered = attr.get('questions_answered', 0)
        ms_confirm = ConfirmUtils.get_player_confirmation(handler_input)
        
        ms_ans_questions = random.choice(
            mult_questions.data.MT_NUM_QUESTIONS_ANS).format(
                questions_answered)

        prompt, reprompt = (
            LastPrompt.get_last_prompt(handler_input) for _ in range(2))
        speech_list += Pauser.make_ms_pause_level_list( ms_confirm, 1, ms_ans_questions, 2, prompt)

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)
