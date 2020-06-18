"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-07 23:09:05
 * @modify date 2020-05-25 16:27:16
 * @desc [
   Contains handlers for the Free_Play mode:
   - Start
   - Set Times Tables
   - Add Times Tables
   - Set Number Questions
   - Set Table Bounds
   - Tell Parameters
   - Answer Question - TODO: Refactor into answer correctly and answer wrong
   - Answered Requested Questions
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
from fallback.fallback_utils import FallbackUtils

from mult_questions.question_attr import QuestionAttr
from mult_questions.gen_questions import GenQuestions
from mult_questions.fp_question import FPQuestions
from mult_questions.question_messages import AllQuestionIntros
from check_answer.question_checker import QuestionChecker
from check_answer.record_wrong import WrongAnswer
from stats.session_stats import SessionStats
from stats.mode_stats import ModeStats
from stats.user_stats import UserStats
from players.players_dict import PlayerDict

from free_play.fp_attr import FreePlayAttr
from free_play.fp_logic import FreePlayLogic
from free_play.fp_num_questions import FPNumQuestions
from free_play.fp_speech import FPSpeech
from free_play.fp_timestables import FPTimesTables
from free_play.fp_upp_lower_bounds import FPUpperLowerBounds
from free_play.fp_prompts import FPPrompts
import free_play.data


##########
# SetUp
##########

class FP_StartHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      attr = handler_input.attributes_manager.session_attributes
      return (
         is_intent_name("StartFreePlayIntent")(handler_input) or
         (
            is_intent_name("AMAZON.YesIntent")(handler_input) and
            attr.get('yes', None) == 'free_play'
         ))
   
   def handle(self, handler_input):
      logger.info("HAN  FP_StartHandler")
      attr = handler_input.attributes_manager.session_attributes
      speech_list = []

      ## Set attr & get slots
      FreePlayAttr.set_attr_free_play(handler_input)

      ## Get table_input to start game.
      lower_table, upper_table, tables_query = (
         FreePlayAttr.get_times_table_input_slots( handler_input))
      FreePlayAttr.set_attr_times_tables( 
         handler_input, lower_table, upper_table, tables_query)
      
      ## Logic check
      retry_query = attr.get('inform_query_tables_format', False)
      tables_provided = FreePlayLogic.check_tables_provided(lower_table, upper_table, tables_query)
      tables_exist = FreePlayLogic.check_tables_exist(handler_input)

      log_all(retry_query, tables_exist)

      ## Confirmation
      if tables_provided or tables_exist:

         if retry_query:
            ms_potential_mistake = FPTimesTables.get_ms_potential_mistake_parsing_query()
            speech_list += Pauser.make_ms_pause_level_list( ms_potential_mistake, 2)
         else:
            ms_confirm = ConfirmUtils.get_confirmation(punct= True)
            speech_list += Pauser.make_ms_pause_level_list( ms_confirm, 1)
         
         if tables_provided:
            ms_using_tables = (
               FPTimesTables.get_ms_using_tables_from_input( lower_table, upper_table, tables_query))
         elif tables_exist:
            ms_using_tables = None  # Create method to use existing tables.
         speech_list += Pauser.make_ms_pause_level_list( ms_using_tables, 2)

         if retry_query:
            ms_retry_query = FPTimesTables.get_ms_can_retry_query_format()
            speech_list += Pauser.make_ms_pause_level_list( ms_retry_query, 3.5)
            FreePlayAttr.reset_attr_query_format(handler_input)
         
         ms_first_problem = FPQuestions.get_question(handler_input, first_question=True)
         speech_list.append( ms_first_problem)

         reprompt = FPQuestions.get_rephrased_question(handler_input)
      
      if not tables_provided:
         ms_welcome = FPSpeech.get_ms_welcome(handler_input)
         q_times_tables, reprompt = (
            FPTimesTables.get_q_times_tables_input() for _ in range(2))
         q_times_tables = CardFuncs.format_prompt( q_times_tables)

         speech_list += Pauser.make_ms_pause_level_list( 
            ms_welcome, 1.5, q_times_tables)
      
      ModeStats.translate_mode_stats_to_sesh(handler_input)

      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title(handler_input)
      card_text = CardFuncs.clean_card_text(speech)
      return (
         handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)


class FP_SetTimesTablesHandler(AbstractRequestHandler):
   """This class is used to change the Times Tables
   at any point (midgame or before game setup).
   """
   def can_handle(self, handler_input):
      return is_intent_name("SetTimesTablesIntent")(handler_input)
   
   def handle(self, handler_input):
      logger.info("HAN  FP_SetTimesTablesHandler")
      attr = handler_input.attributes_manager.session_attributes
      speech_list = []

      ## Get & Set slots
      lower_table, upper_table, tables_query = (
         FreePlayAttr.get_times_table_input_slots(handler_input))

      ## Logic checks
      retry_query = attr.get('inform_query_tables_format', False)
      tables_provided = FreePlayLogic.check_tables_provided(lower_table, upper_table, tables_query)

      if tables_provided:
         FreePlayAttr.set_attr_free_play(handler_input)
         FreePlayAttr.set_attr_times_tables(handler_input,
            lower_table, upper_table, tables_query)

         if retry_query:
            ms_potential_mistake = FPTimesTables.get_ms_potential_mistake_parsing_query()
            speech_list += Pauser.make_ms_pause_level_list( ms_potential_mistake, 2)
         else:
            ms_confirm = ConfirmUtils.get_random_confirmation(handler_input)
            speech_list.append( ms_confirm)

         ms_using_tables = (
            FPTimesTables.get_ms_using_tables_from_input(lower_table, upper_table, tables_query))
         speech_list += Pauser.make_ms_pause_level_list( ms_using_tables, 2)

         if retry_query:
            ms_retry_query = FPTimesTables.get_ms_can_retry_query_format()
            speech_list += Pauser.make_ms_pause_level_list( ms_retry_query, 3.5)
            FreePlayAttr.reset_attr_query_format(handler_input)

         prompt = FPPrompts.get_q_fp_setup_prompt(handler_input)
         reprompt = FPPrompts.get_q_fp_setup_reprompt(handler_input)
         speech_list.append( prompt)
         
      ## Ask for times_tables slots
      else:
         q_times_tables, reprompt = (
            FPTimesTables.get_q_times_tables_input() for _ in range(2))
         q_times_tables = CardFuncs.format_prompt( q_times_tables)
         speech_list.append( q_times_tables)
         reprompt = LastPrompt.get_last_prompt(handler_input)
      
      ModeStats.translate_mode_stats_to_sesh(handler_input)

      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title(handler_input)
      card_text = CardFuncs.clean_card_text(speech)
      return (
         handler_input.response_builder
            .speak( speech)
            .ask( reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)


class FP_AddTimesTablesHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      return is_intent_name("AddTimesTablesIntent")(handler_input)

   def handle(self, handler_input):
      logger.info("HAN  FP_AddTimesTablesHandler")
      attr = handler_input.attributes_manager.session_attributes
      speech_list = []

      lower_table, upper_table, tables_query = (
         FreePlayAttr.get_times_table_input_slots(handler_input))
      retry_query = attr.get('inform_query_tables_format', False)

      if not tables_query:
         ms_can_add = FPTimesTables.get_ms_can_add_tables()
         speech_list += Pauser.make_ms_pause_level_list(ms_can_add, 2.5)

      else:
         FreePlayAttr.add_to_attr_times_tables(
            handler_input, lower_table, upper_table, tables_query)
            
         if retry_query:
            ms_potential_mistake = FPTimesTables.get_ms_potential_mistake_parsing_query()
            speech_list += Pauser.make_ms_pause_level_list( ms_potential_mistake, 2)
         
         ms_added_tables = FPTimesTables.get_ms_added_tables(tables_query)
         speech_list += Pauser.make_ms_pause_level_list( ms_added_tables, 1.5)

         if retry_query:
            ms_retry_query = FPTimesTables.get_ms_can_retry_query_format()
            speech_list += Pauser.make_ms_pause_level_list( ms_retry_query, 3.5)
            FreePlayAttr.reset_attr_query_format(handler_input)

      ## May like to add only if tables query??
      prompt = FPPrompts.get_q_fp_setup_prompt(handler_input)
      reprompt = FPPrompts.get_q_fp_setup_reprompt(handler_input)
      speech_list.append( prompt)

      ModeStats.translate_mode_stats_to_sesh(handler_input)
      
      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title(handler_input)
      card_text = CardFuncs.clean_card_text(speech)
      return (
         handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)


class FP_SetNumberQuestionsHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      return is_intent_name("SetNumberQuestionsIntent")(handler_input)
   
   def handle(self, handler_input):
      logger.info("HAN  FP_SetNumberQuestionsHandler")
      speech_list = []

      FreePlayAttr.set_attr_free_play(handler_input)   # reset questions asked.
      num_questions = SlotUtils.get_slot_val_by_name(handler_input, 'num_questions')

      if num_questions is None:
         ms_can_set_questions = FPNumQuestions.get_ms_can_set_num_questions()
         prompt, reprompt = (
            FPNumQuestions.get_q_num_questions() for _ in range(2))
         speech_list += Pauser.make_ms_pause_level_list( ms_can_set_questions, 2, prompt)
      
      else:
         FreePlayAttr.set_attr_num_questions(handler_input, num_questions)

         ms_confirm = ConfirmUtils.get_random_confirmation(handler_input)
         ms_ask_num_questions = FPNumQuestions.get_ms_ask_num_questions(handler_input)
         prompt = FPPrompts.get_q_fp_setup_prompt(handler_input)
         reprompt = FPPrompts.get_q_fp_setup_reprompt(handler_input)

         speech_list += Pauser.make_ms_pause_level_list(
            ms_confirm, ms_ask_num_questions, 2, prompt)

      ModeStats.translate_mode_stats_to_sesh(handler_input)

      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title( handler_input)
      card_text = CardFuncs.clean_card_text( speech)
      return (
         handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard(card_title, card_text))
            .response)


class FP_SetTableBoundsHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      return is_intent_name("SetTableBoundsIntent")(handler_input)
   
   def handle(self, handler_input):
      logger.info("HAN  FP_SetTableBoundsHandler")
      speech_list = []

      lower_bound, upper_bound = FreePlayAttr.get_table_bound_slots(handler_input)
      FreePlayAttr.set_table_bounds(handler_input, lower_bound, upper_bound)
      bounds_provided = FreePlayLogic.check_table_bounds_provided(lower_bound, upper_bound)
      
      if bounds_provided:
         confirm = ConfirmUtils.get_random_confirmation(handler_input)
         ms_adjusted_table_bounds = FPUpperLowerBounds.get_ms_set_table_bounds(
            lower_bound, upper_bound)
         prompt = FPPrompts.get_q_fp_setup_prompt(handler_input)
         reprompt = FPPrompts.get_q_fp_setup_reprompt(handler_input)

         # QuestionAttr.increment_questions_answered(handler_input, increase=False)
         ## New question, but not counted as answered.

         speech_list += Pauser.make_ms_pause_level_list(
            confirm, 1, ms_adjusted_table_bounds, 2, prompt)
      
      else:
         ms_can_change_bounds = FPUpperLowerBounds.get_ms_can_change_table_bounds()
         prompt, reprompt = (
            FPUpperLowerBounds.get_q_change_bounds() for _ in range(2))
         speech_list += Pauser.make_ms_pause_level_list(
            ms_can_change_bounds, 2.5, prompt)

      ModeStats.translate_mode_stats_to_sesh(handler_input)

      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title(handler_input)
      card_text = CardFuncs.clean_card_text(speech)
      return (
         handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)


class FP_ParametersHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      attr = handler_input.attributes_manager.session_attributes
      return (
         attr.get('mode', None) == 'free_play' and
         is_intent_name("FreePlayParametersIntent")(handler_input)
      )  
      
   def handle(self, handler_input):
      logger.info("HAN  FP_ParametersIntent")
      speech_list = []

      ms_confirm = ConfirmUtils.get_confirmation(True)
      ms_fp_params = FPSpeech.get_ms_fp_parameters(handler_input)

      prompt, reprompt = (
         LastPrompt.get_last_prompt(handler_input) for _ in range(2))
      
      speech_list += Pauser.make_ms_pause_level_list(
         ms_confirm, 1, ms_fp_params, 2.5, prompt)
      
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
# Answer
##########

class FP_AnswerQuestionHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      attr = handler_input.attributes_manager.session_attributes
      return (
         attr.get('mode', None) == 'free_play' and
         is_intent_name("AnswerIntent")(handler_input)
      )
   
   def handle(self, handler_input):
      logger.info("HAN  FP_AnswerQuestionHandler")
      speech_list = []
      
      player_obj = PlayerDict.load_player_obj(handler_input)
      answer = SlotUtils.get_slot_val_by_name(handler_input, 'answer')
      if not answer:
         return FallbackUtils.return_unknown_slot_response(handler_input)

      correct = QuestionChecker.check_answer(handler_input)
      UserStats.update_player_stats(                     # so table always exists
         handler_input, correct, player_obj= player_obj)
      
      if correct:

         ms_congrats = CongratUtils.get_answer_congrats(handler_input, player_obj= player_obj)
         ms_question = FPQuestions.get_question(handler_input)
         reprompt = FPQuestions.get_rephrased_question(handler_input)

         logger.debug(ms_congrats)

         if ms_congrats != "":
            speech_list += Pauser.make_ms_pause_level_list(
               ms_congrats, 1, ms_question)
         else:
            speech_list.append(ms_question)
            
      else:
         WrongAnswer.record_wrong_question(handler_input)
         ms_incorrect = IncorrectAnsUtils.get_buzz_and_incorrect()
         ms_retry_question = AllQuestionIntros.get_retry_question(handler_input)
         reprompt = GenQuestions.get_same_question(handler_input)

         speech_list += Pauser.make_ms_pause_level_list(
            ms_incorrect, 1, ms_retry_question)
      
      SessionStats.update_consecutive_correct(handler_input, correct)
      ModeStats.update_mode_stats(handler_input, correct)

      logger.debug(speech_list)
      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title(handler_input)
      card_text = CardFuncs.clean_card_text(speech)
      return (
         handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)


class FP_AnsweredRequestedQuestionsHandler(AbstractRequestHandler):
   def can_handle(self, handler_input):
      attr = handler_input.attributes_manager.session_attributes
      return (
         attr.get('mode', None) == "free_play" and
         is_intent_name("AnswerIntent")(handler_input) and

         FreePlayLogic.check_asked_requested_questions(handler_input) and
         QuestionChecker.check_answer(handler_input)
      )
   
   def handle(self, handler_input):
      logger.info("HAN  FP_AnsweredRequestedQuestionsHandler")
      attr = handler_input.attributes_manager.session_attributes
      speech_list = []

      correct = QuestionChecker.check_answer(handler_input)
      UserStats.update_player_stats(handler_input, correct)

      ms_congrats = CongratUtils.get_player_congrats(handler_input, 2)

      num_questions = attr.get('num_questions', '')
      ms_answered_all_questions = FPSpeech.get_ms_answered_all_questions(num_questions)

      prompt, reprompt = (
         HelpUtils.get_q_what_todo() for _ in range(2))
      prompt = CardFuncs.format_prompt( prompt)

      speech_list += Pauser.make_ms_pause_level_list(
         ms_congrats, 1, ms_answered_all_questions, 3, prompt)
     
      SessionStats.update_consecutive_correct(handler_input, correct)
      ModeStats.update_mode_stats(handler_input, correct)
      ModeStats.translate_mode_stats_to_sesh(handler_input)
      FreePlayAttr.set_attr_end_fp(handler_input)

      speech = ' '.join(speech_list)
      card_title = CardFuncs.get_card_title(handler_input)
      card_text = CardFuncs.clean_card_text(speech)
      return (
         handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)

