"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-23 10:28:10
 * @modify date 2020-06-16 17:18:00
 * @desc [
    Handlers for Custom Practice.
    - Start CP
    - Correct Answer
    - Wrong Answer
    - Correct Answer & next activity.

    TODO: Users should be able to pick what practice they want to do,
    e.g., request practice new times tables, or (f) error tables.
    Currently, implemented in linear fashion and can't skip an activity.
]*/
"""


##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from answer_response.confirmation_utils import ConfirmUtils
from answer_response.congrat_utils import CongratUtils
from answer_response.incorrect_utils import IncorrectAnsUtils
from aux_utils.last_prompt import LastPrompt
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.thanks import get_ms_thanks
from check_answer.question_checker import QuestionChecker
from check_answer.record_wrong import WrongAnswer
from logs import logger, log_func_name, log_all
from helper.help_utils import HelpUtils
from skill_card.card_funcs import CardFuncs
from slots.slot_utils import SlotUtils
from stats.session_stats import SessionStats
from stats.mode_stats import ModeStats
from stats.user_stats import UserStats
from pause.pauser import Pauser
from players.players_dict import PlayerDict
from mult_questions.gen_questions import GenQuestions
from mult_questions.cp_questions import CP_Questions

from custom_practice.cp_attr import CP_Attr
from custom_practice.welcome_utils import CP_Welcome
from custom_practice.practice_type import CP_PracticeType
from custom_practice.pract_intro import CP_PractIntro
from custom_practice.cp_pract_end import CP_PractEnd
import custom_practice.data


##########
# Start Handler
##########

class CP_StartHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            is_intent_name("StartCustomPracticeIntent")(handler_input) or
            (
                is_intent_name("AMAZON.YesIntent")(handler_input) and
                attr.get('yes', None) == 'custom'
            )
        )

    def handle(self, handler_input):
        logger.info("HAN    CP_StartHandler")
        player_obj = PlayerDict.load_player_obj(handler_input)
        
        ## Check Sufficient Data
        ## NOTE: make like to refacor this into a method that returns response object
        ## That will remove the nested loop below.
        answered_questions = player_obj.get_answered_questions()
        if answered_questions < custom_practice.data.MIN_DATA_REQUIRED:
            prompt, reprompt = (
                HelpUtils.get_q_what_todo() for _ in range(2))

            speech_list = (
                CP_Welcome.get_ms_need_more_data(answered_questions),
                2,
                prompt,
            )
            
        else:
            CP_Attr.set_attr_start_cp(handler_input)
            CP_Attr.set_tbl_mean_err_list_attr(handler_input, player_obj)   # used in practice type
            
            ms_welcome = CP_Welcome.get_ms_welcome(handler_input, player_obj)

            practice_type = CP_PracticeType.get_practice_type(
                handler_input, allow_incorrect_problems= True)
            CP_Attr.save_practice_type(handler_input, practice_type)
            CP_Attr.set_pract_type_attr(handler_input, player_obj, practice_type)
            CP_Attr.update_last_question_attr(handler_input, correct = True)
            
            ms_practice_intro = CP_PractIntro.get_ms_practice_type_intro(handler_input, practice_type)
            question = CP_Questions.get_question(
                handler_input, player_obj, practice_type, first_question= True)
            reprompt  = GenQuestions.get_same_question(handler_input)
            speech_list = (
                ms_welcome,
                2.5,
                ms_practice_intro,
                2,
                question,
            )

        speech = get_ms_from_tuple(speech_list)
        reprompt = GenQuestions.get_same_question(handler_input)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


##########
# Answer Handlers
##########

class CP_CorrectAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'custom' and 
            is_intent_name("AnswerIntent")(handler_input) and 
            QuestionChecker.check_answer(handler_input)
        )

    def handle(self, handler_input):
        logger.info("HAN    CP_CorrectAnswerHandler")
        attr = handler_input.attributes_manager.session_attributes
        speech_list = []

        practice_type = attr['practice_type']
        if practice_type == custom_practice.data.PRACT_TYPES[0]:
            CP_Attr.remove_question_from_incorrect_questions(handler_input)     ## Before updating last question
        CP_Attr.update_last_question_attr(handler_input, correct = True)

        player_obj = PlayerDict.load_player_obj(handler_input)
        UserStats.update_player_stats(handler_input, correct = True, player_obj= player_obj)

        ms_congrats = CongratUtils.get_answer_congrats(
            handler_input, player_obj = player_obj)
        ms_question = CP_Questions.get_question(
            handler_input, player_object= player_obj, 
            practice_type = practice_type, first_question= False)
        reprompt  = GenQuestions.get_same_question(handler_input)

        speech_list = (
            ms_congrats,
            1,
            ms_question
        )

        SessionStats.update_consecutive_correct(handler_input, True)
        ModeStats.update_mode_stats(handler_input, True)
        PlayerDict.save_player_obj(handler_input, player_obj)

        speech = get_ms_from_tuple(speech_list)
        reprompt = GenQuestions.get_same_question(handler_input)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


class CP_WrongAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'custom' and 
            is_intent_name("AnswerIntent")(handler_input) and 
            not QuestionChecker.check_answer(handler_input)
        )

    def handle(self, handler_input):
        logger.info("HAN    CP_WrongAnswerHandler")
        speech_list = []

        player_obj = PlayerDict.load_player_obj(handler_input)

        CP_Attr.update_last_question_attr( handler_input, correct = False)
        UserStats.update_player_stats( handler_input, correct = False, player_obj= player_obj)
        
        ms_wrong = IncorrectAnsUtils.get_ms_incorrect()
        question = GenQuestions.get_same_question(handler_input)
        reprompt = question
        speech_list = (
            ms_wrong, 
            1,
            question,
        )

        SessionStats.update_consecutive_correct(handler_input, correct=False)
        ModeStats.update_mode_stats(handler_input, correct=False)
        WrongAnswer.record_wrong_question(handler_input)
        PlayerDict.save_player_obj(handler_input, player_obj)

        speech = get_ms_from_tuple(speech_list)
        reprompt = GenQuestions.get_same_question(handler_input)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


##########
# Next Activity Handler
##########

class CP_NextPracticeHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'custom' and  
            is_intent_name("AnswerIntent")(handler_input) and
            QuestionChecker.check_answer(handler_input) and 
            CP_Attr.check_last_question(handler_input)
        )
        
    def handle(self, handler_input):
        logger.info("HAN    CP_NextPracticeHandler")
        attr = handler_input.attributes_manager.session_attributes
        speech_list = []

        player_obj = PlayerDict.load_player_obj(handler_input)
        UserStats.update_player_stats(
            handler_input, correct = True, player_obj= player_obj)
        
        CP_Attr.set_attr_new_practice(handler_input)
        CP_Attr.set_tbl_mean_err_list_attr(handler_input, player_obj)

        practice_type = attr['practice_type']
        ms_end_pract_type = CP_PractEnd.get_ms_practice_type_end(
            handler_input, practice_type = practice_type)

        if practice_type == custom_practice.data.PRACT_TYPES[0]:
            CP_Attr.remove_question_from_incorrect_questions(handler_input)
        
        ms_congrats = CongratUtils.get_player_congrats(handler_input)

        if practice_type != custom_practice.data.PRACT_TYPES[-1]: 

            practice_type = CP_PracticeType.get_practice_type(
                handler_input, allow_incorrect_problems= False)
            CP_Attr.save_practice_type(handler_input, practice_type)
            CP_Attr.set_pract_type_attr(handler_input, player_obj, practice_type)
            CP_Attr.update_last_question_attr(handler_input, correct = True)

            ms_practice_intro = CP_PractIntro.get_ms_practice_type_intro(
                handler_input, practice_type = practice_type)
            question = CP_Questions.get_question(
                handler_input, player_obj, practice_type, first_question= True)
            reprompt  = GenQuestions.get_same_question(handler_input)

            speech_list = (
                ms_congrats, 
                0.5,
                ms_end_pract_type,
                2.5,
                ms_practice_intro,
                2,
                question,
            )
        else:
            UserStats.update_player_cp_stats(handler_input, player_obj)
            prompt, reprompt = (
                HelpUtils.get_q_what_todo() for _ in range(2))
            
            speech_list = (
                ms_congrats,
                0.5,
                ms_end_pract_type,
                2,
                prompt
            )
        
        SessionStats.update_consecutive_correct(handler_input, True)
        ModeStats.update_mode_stats(handler_input, True)
        PlayerDict.save_player_obj(handler_input, player_obj)

        speech = get_ms_from_tuple(speech_list)
        reprompt = GenQuestions.get_same_question(handler_input)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

