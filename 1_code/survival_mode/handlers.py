"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 09:56:46
 * @modify date 2020-05-27 12:24:50
 * @desc [
    Handlers for Survival Mode.
    - Start
    - Correct Answer
    - Wrong Answer
    - 

    NOTE: "SM_" Prefix indicates that the objects belong to survival mode.
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
from answer_response.confirmation_utils import ConfirmUtils
from answer_response.congrat_utils import CongratUtils
from answer_response.incorrect_utils import IncorrectAnsUtils
from slots.slot_utils import SlotUtils
from skill_card.card_funcs import CardFuncs
from aux_utils.last_prompt import LastPrompt
from helper.help_utils import HelpUtils
from fallback.fallback_utils import FallbackUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from players.players_dict import PlayerDict
from aux_utils.thanks import get_ms_thanks


from check_answer.answer_speech import GetAnswerSpeech
from check_answer.record_wrong import WrongAnswer
from mult_questions.gen_questions import GenQuestions
from mult_questions.question_attr import QuestionAttr
from mult_questions.sm_questions import SMQuestions
from check_answer.question_checker import QuestionChecker
from stats.session_stats import SessionStats
from stats.mode_stats import ModeStats
from stats.user_stats import UserStats


from survival_mode.endgame_utils import SMEndGame
from survival_mode.survival_attr import SM_Attr
from survival_mode.welcome_utils import SM_WelcomeUtils


##########
# SetUp
##########

class SM_StartHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            is_intent_name("StartSurvivalModeIntent")(handler_input) or
            (
                is_intent_name("AMAZON.YesIntent")(handler_input) and
                attr.get('yes', None) == 'survival'
            )
        )

    def handle(self, handler_input):
        logger.info("HAN    SM_StartHandler")
        speech_list = []

        SM_Attr.set_attr_start_survival_mode(handler_input)
        ModeStats.translate_mode_stats_to_sesh(handler_input)

        ms_welcome = SM_WelcomeUtils.get_ms_welcome(handler_input)
        ms_question = SMQuestions.get_question(handler_input, first_question= True)
        reprompt = GenQuestions.get_same_question(handler_input)
        
        speech_list += Pauser.make_ms_pause_level_list( 
            ms_welcome, 2, ms_question)

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)
        return (
            handler_input.response_builder
                .speak( speech)
                .ask( reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


##########
# Game Play
##########

class SM_CorrectAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'survival' and 
            is_intent_name("AnswerIntent")(handler_input) and
            QuestionChecker.check_answer(handler_input)
        )
    
    def handle(self, handler_input):
        logger.info("HAN    SM_CorrectQuestionHandler")
        speech_list = []

        player_obj = PlayerDict.load_player_obj(handler_input)
        UserStats.update_player_stats(handler_input, correct = True, player_obj= player_obj)
        SM_Attr.increment_sm_upper(handler_input)
        
        ms_congrats = CongratUtils.get_answer_congrats(
            handler_input, player_obj= player_obj, survival_mode=True)

        logger.debug(ms_congrats)

        ms_question = SMQuestions.get_question(
            handler_input, first_question= False, player_obj= player_obj)
        reprompt = GenQuestions.get_same_question(handler_input)
        
        if len(ms_congrats):
            sm_pause = Pauser.get_sm_pause_length(handler_input)
            speech_list += Pauser.make_ms_pause_level_list(ms_congrats, sm_pause)
        speech_list.append( ms_question)
        
        SessionStats.update_consecutive_correct(handler_input, True)
        ModeStats.update_mode_stats(handler_input, True)

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


class SM_WrongAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'survival' and 
            is_intent_name("AnswerIntent")(handler_input) and 
            not QuestionChecker.check_answer(handler_input)
        )
    
    def handle(self, handler_input):
        logger.info("HAN    SM_WrongAnswerHandler")
        player_obj = PlayerDict.load_player_obj(handler_input)
        UserStats.update_player_stats(
            handler_input, correct = False, player_obj= player_obj)
        
        WrongAnswer.record_wrong_question(handler_input)

        ms_incorrect = IncorrectAnsUtils.get_buzz_and_incorrect()
        ms_correct_ans = GetAnswerSpeech.get_ms_answer(handler_input)
        ms_score = SMEndGame.get_ms_game_score(handler_input)

        ms_congrats = CongratUtils.get_player_congrats(handler_input, 1)
        ms_results = SMEndGame.get_ms_score_results(
            handler_input, player_obj= player_obj)
        ms_thanks = get_ms_thanks(handler_input, mode = True, excite=True)

        prompt, reprompt = (
            HelpUtils.get_q_what_todo() for _ in range(2))

        speech_list = (
            ms_incorrect,
            1,
            ms_correct_ans,
            2,
            ms_congrats,
            0.75,
            ms_score,            
            1.25,
            ms_results,
            1.75,
            ms_thanks,
            4.5,
            prompt,
        )
        
        SM_Attr.log_stats(handler_input)
        SessionStats.update_consecutive_correct(handler_input, correct= False)
        ModeStats.update_mode_stats(handler_input, correct= False)
        UserStats.update_player_sm_stats(handler_input, player_obj= player_obj)     #before translating mode stats
        SM_Attr.set_attr_end_survival_mode(handler_input)
        ModeStats.translate_mode_stats_to_sesh(handler_input)
        
        speech = get_ms_from_tuple(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

