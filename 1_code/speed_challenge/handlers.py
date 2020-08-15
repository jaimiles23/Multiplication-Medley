"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-20 22:46:14
 * @modify date 2020-05-22 23:35:28
 * @desc [
    Handlers for speed challenge:
    - Start
    - Difficulty
    - Correct Answer
    - Wrong Answer
    - End Game
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

from logs import logger, log_func_name, log_all
from pause.pauser import Pauser
from answer_response.confirmation_utils import ConfirmUtils
from answer_response.congrat_utils import CongratUtils
from answer_response.incorrect_utils import IncorrectAnsUtils
from slots.slot_utils import SlotUtils
from skill_card.card_funcs import CardFuncs
from aux_utils.last_prompt import LastPrompt
from helper.help_utils import HelpUtils
from aux_utils.create_tuple_message_clauses import get_linear_nlg
from players.players_dict import PlayerDict
from check_answer.question_checker import QuestionChecker
from check_answer.record_wrong import WrongAnswer
from aux_utils.thanks import get_ms_thanks

from stats.session_stats import SessionStats
from stats.mode_stats import ModeStats
from stats.user_stats import UserStats

from speed_challenge.welcome_utils import SC_WelcomeUtils
from speed_challenge.sc_attr import SC_Attr
from speed_challenge.difficulty_utils import SC_Difficulty
from speed_challenge.end_utils import SC_EndGame

from mult_questions.sc_questions import SC_Questions
from mult_questions.gen_questions import GenQuestions


##########
# Welcome Handlers
##########

class SC_StartHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            is_intent_name("StartSpeedChallengeIntent")(handler_input) or
            (
                is_intent_name("AMAZON.YesIntent")(handler_input) and
                attr.get('yes', None) == 'speed'
            )
        )
    
    def handle(self, handler_input):
        logger.info("HAN    SC_StartHandler")
        speech_list = []

        SC_Attr.set_attr_start_sc(handler_input)
        player_obj = PlayerDict.load_player_obj(handler_input)
        difficulty = SlotUtils.get_resolved_value(handler_input, 'difficulty')

        if not difficulty:
            ms_welcome = SC_WelcomeUtils.get_ms_welcome(player_obj)
            q_difficulty, reprompt = (
                SC_Difficulty.get_q_sc_difficulty(player_obj) for _ in range(2))
            
            speech_list += Pauser.make_ms_pause_level_list(
                ms_welcome, 2, q_difficulty)

        elif difficulty:
            SC_Attr.set_sc_diff(handler_input, difficulty)
            ms_confirmation = ConfirmUtils.get_confirmation(True)
            ms_use_difficulty = SC_Difficulty.get_ms_using_difficulty(difficulty)

            SC_Questions.load_sc_questions(handler_input)
            ms_start_timer = SC_WelcomeUtils.get_ms_starting_time()
            question = SC_Questions.get_question(handler_input, first_question= True)
            reprompt = question

            speech_list += Pauser.make_ms_pause_level_list( 
                ms_confirmation, 0.5, ms_use_difficulty, 2, ms_start_timer, question)

            SC_Attr.save_start_time(handler_input)


        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


##########
# Set Up Handlers
##########
class SC_DifficultySetupHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            is_intent_name("SpeedChallengeDifficultyIntent")(handler_input)
        )
        ## NOTE: no next handler -- if player just provides intent, starts.
    
    def handle(self, handler_input):
        logger.info("HAN    SC_DifficultySetupHandler")
        speech_list = []

        SC_Attr.set_attr_start_sc(handler_input)
        player_obj = PlayerDict.load_player_obj(handler_input)
        difficulty = SlotUtils.get_resolved_value(handler_input, 'difficulty')
        if not difficulty:
            ms_try_again = SC_Difficulty.get_ms_not_register()
            q_difficulty, reprompt = (
                SC_Difficulty.get_q_sc_difficulty(player_obj) for _ in range(2))

            speech_list += Pauser.make_ms_pause_level_list(
                ms_try_again, 1, q_difficulty)

        if difficulty:
            SC_Attr.set_sc_diff(handler_input, difficulty)

            ms_confirm = ConfirmUtils.get_player_confirmation(handler_input)
            ms_use_difficulty = SC_Difficulty.get_ms_using_difficulty(difficulty)

            SC_Questions.load_sc_questions(handler_input)
            ms_start_timer = SC_WelcomeUtils.get_ms_starting_time()
            question = SC_Questions.get_question(handler_input, first_question= True)
            reprompt = question

            speech_list += Pauser.make_ms_pause_level_list( 
                ms_confirm, 0.5, ms_use_difficulty, 2, ms_start_timer, question)

            SC_Attr.save_start_time(handler_input)

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


##########
# Game Play
##########
class SC_CorrectAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'speed' and 
            is_intent_name("AnswerIntent")(handler_input) and 
            QuestionChecker.check_answer(handler_input)
        )
    
    def handle(self, handler_input):
        logger.info("HAN    SC_CorrectAnswerHandler")
        
        ## TODO: Check sc attr and if anything needs to be incremented??
        player_obj = PlayerDict.load_player_obj(handler_input)
        UserStats.update_player_stats(
            handler_input, correct = True, player_obj = player_obj)

        question = SC_Questions.get_question(handler_input)
        reprompt = question

        SessionStats.update_consecutive_correct(handler_input, correct= True)
        ModeStats.update_mode_stats(handler_input, correct= True)

        speech = question
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


class SC_WrongAnswerHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'speed' and 
            is_intent_name("AnswerIntent")(handler_input) and 
            not QuestionChecker.check_answer(handler_input)
        )
    
    def handle(self, handler_input):
        logger.info("HAN    SC_WrongAnswerHandler")
        speech_list = []

        player_obj = PlayerDict.load_player_obj(handler_input)
        UserStats.update_player_stats(
            handler_input, correct = False, player_obj= player_obj)

        ms_incorrect_buzz = IncorrectAnsUtils.get_buzzer()
        question = GenQuestions.get_same_question(handler_input)
        reprompt = question

        speech_list += Pauser.make_ms_pause_level_list(
            ms_incorrect_buzz, 0.5, question)

        SessionStats.update_consecutive_correct(handler_input, correct=False)
        ModeStats.update_mode_stats(handler_input, correct=False)
        WrongAnswer.record_wrong_question(handler_input)

        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)


########## 
# End Game
##########
class SC_FinishedChallengeHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            attr.get('mode', None) == 'speed' and 
            SC_Attr.check_no_questions(handler_input) and
            is_intent_name("AnswerIntent")(handler_input) and
            QuestionChecker.check_answer(handler_input)
        )
    
    def handle(self, handler_input):
        logger.info("HAN    SC_FinishedChallengeHandler")
        speech_list = []

        SC_Attr.save_end_time(handler_input)
        sc_score_time = SC_Attr.get_sc_total_time(handler_input)

        player_obj = PlayerDict.load_player_obj(handler_input)
        
        SessionStats.update_consecutive_correct(handler_input, correct=True)
        ModeStats.update_mode_stats(handler_input, correct=True)
        UserStats.update_player_stats(
            handler_input, correct= True, player_obj= player_obj)
        
        ms_congrats = CongratUtils.get_player_congrats(handler_input, 2)
        ms_complete_time = SC_EndGame.get_ms_game_score(handler_input, sc_score_time)
        ms_score_results = SC_EndGame.get_ms_score_results(
            handler_input, sc_score_time= sc_score_time, player_obj= player_obj)
        ms_thanks = get_ms_thanks(handler_input, mode=True, excite=True)
        prompt, reprompt = (
            HelpUtils.get_q_what_todo() for _ in range(2))
        
        speech_list = (
            ms_congrats,
            1,
            ms_complete_time,
            1.5,
            ms_score_results,
            1.75,
            ms_thanks,
            4,
            prompt,
        )

        SC_Attr.log_sc_stats(handler_input)
        ModeStats.translate_mode_stats_to_sesh(handler_input)
        UserStats.update_player_sc_stats(
            handler_input, sc_score_time= sc_score_time, player_obj= player_obj)
        SC_Attr.set_attr_end_sc(handler_input)
        PlayerDict.save_player_obj(handler_input, player_obj)

        speech = get_linear_nlg(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)   
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

