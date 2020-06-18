""""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-14 10:51:47
 * @modify date 2020-05-14 10:51:47
 * @desc [
    Handler class to tell user the answer.
    Only accessible in free_play and custom mode.
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
from skill_card.card_funcs import CardFuncs
from mult_questions.fp_question import FPQuestions
from pause.pauser import Pauser

from check_answer.answer_speech import GetAnswerSpeech
from mult_questions.question_attr import QuestionAttr


##########
# GetAnswerHandler
##########

class GetAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            is_intent_name("GetAnswerIntent")(handler_input) and
            attr.get('mode', False) in ('free_play', 'custom') and
            attr.get('question', None)      # Active question
        )

    def handle(self, handler_input):
        logger.info("HAN    GetAnswerHandler")
        speech_list = []
        
        ms_answer = GetAnswerSpeech.get_ms_answer(handler_input)
        next_question = FPQuestions.get_question(handler_input)
        QuestionAttr.increment_questions_answered(handler_input, False) # undo increment.

        speech_list += Pauser.make_ms_pause_level_list(
            ms_answer, 2, next_question)

        reprompt = next_question

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

    
