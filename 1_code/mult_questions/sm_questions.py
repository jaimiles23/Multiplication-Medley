"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 12:49:57
 * @modify date 2020-05-20 21:22:27
 * @desc [
   SMQuestions utility class with methods to get survival mode questions.
   Methods for:
   - get_question (master method)
   - Sample question
   - Question introduction
   - 
 ]
 */
"""

##########
# Imports
##########

from math import sqrt
from statistics import mean
import random


from logs import logger, log_func_name, log_all

from mult_questions.question_attr import QuestionAttr
from mult_questions.gen_questions import GenQuestions
from mult_questions.question_messages import AllQuestionIntros
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from stats.user_stats import UserStats
from players.players_dict import PlayerDict
from answer_response.confirmation_utils import ConfirmUtils

import mult_questions.data_sm


##########
# Survival Mode Questions
##########

class SMQuestions(object):

   ##########
   # overall method
   ##########
   @staticmethod 
   @log_func_name
   def get_question(handler_input, first_question: bool = False, player_obj: object = None) -> str:
      """Returns a question for survival mode."""
      if not first_question:
         QuestionAttr.increment_questions_answered(handler_input)
      
      ## Get new question
      flag_get_new_question = True
      while flag_get_new_question:
         new_question = SMQuestions.get_sampled_num(handler_input)

         if not GenQuestions.check_same_question(handler_input, new_question):
            flag_get_new_question = False

      ## Save question
      QuestionAttr.save_question(handler_input, new_question)

      ## Messages
      ms_question_intro = SMQuestions.get_ms_question_intro(
         handler_input, first_question= first_question, player_obj = player_obj)
      ms_question = GenQuestions.format_question(new_question)

      speech_list = ( ms_question_intro, ms_question)
      return get_ms_from_tuple(speech_list)


   ##########
   # Sample Question
   ##########
   @staticmethod
   @log_func_name
   def get_sampled_num(handler_input) -> tuple:
      """Returns tuples of times table question for the user.

      Uses random.gaus() to take two randomly selected numbers.
      numbers are capped at sm_upper.
      """
      @log_func_name
      def get_rand_gauss_num(upper: int)-> int:
         """Returns integer sampled from normal distribution.
         
         Uses a center at 2/3 the max number."""
         sm_center = (upper / 1.1)
         variation = (sqrt(upper) - 1) * 1.5

         gauss_dist_num = float('inf')
         while (gauss_dist_num > upper) or (gauss_dist_num < 0):
            gauss_dist_num = int(
               random.gauss( sm_center, variation))
            
            if (gauss_dist_num < sm_center // 2.5) and (random.random() < 0.33):
               ## norm dist with variation showing high chance of low nums... 
               ## still want wide spread, so chance to re-roll.
               gauss_dist_num = float('inf')
         
         return gauss_dist_num
      

      attr = handler_input.attributes_manager.session_attributes
      sm_upper = attr.get('sm_upper', 5)
      num_1, num_2 = (
         get_rand_gauss_num(sm_upper) for _ in range(2))

      log_all(sm_upper, num_1, num_2)
      return (num_1, num_2)
   

   ##########
   # Question introduction
   ##########
   @staticmethod
   @log_func_name
   def get_ms_question_intro(handler_input, first_question: bool, player_obj: object = None) -> str:
      """Returns message for the question introduction.
      
      NOTE: No confirmation in this mode."""
      attr = handler_input.attributes_manager.session_attributes

      flag_double_digits = attr.get('flag_double_digits', False)
      flag_upper_hit_avg = attr.get('flag_upper_hit_avg', False)
      flag_cntr_hit_avg = attr.get('flag_cntr_hit_avg', False)

      sm_upper = int(attr.get('sm_upper', 0))
      sm_center = int(sm_upper / 1.1)
      questions_answered = attr.get('questions_answered', 0)

      if first_question:
        return AllQuestionIntros.get_first_question_intro()

      elif (sm_upper == 10) and flag_double_digits:
         attr['flag_double_digits'] = False
         return SMQuestions.get_ms_upper_as_ten()
      
      ## Load objs to avoid repetitive loads.
      if not player_obj:
         player_obj = PlayerDict.load_player_obj(handler_input)
      answered_tables = player_obj.get_answered_tables(integers = True)
      inflated_average_table = int(mean(answered_tables)) + 2  ## Note a truth average

      log_all(sm_upper, sm_center, inflated_average_table, questions_answered)

      if (sm_upper == inflated_average_table - 2) and flag_upper_hit_avg:     ## when sm_upper is uninflated_average.
         attr['flag_upper_hit_avg'] = False
         return SMQuestions.get_ms_upper_as_average_table()
      
      elif (sm_center == inflated_average_table ) and flag_cntr_hit_avg:
         attr['flag_cntr_hit_avg'] = False
         return SMQuestions.get_ms_freq_average_table()
      
      return SMQuestions.get_ms_relative_difficulty(
         handler_input, player_obj = player_obj, answered_tables= answered_tables)


   @staticmethod
   @log_func_name
   def get_ms_upper_as_ten() -> str:
      """Returns introduction that times tables can now be double digits."""
      return random.choice(
         mult_questions.data_sm.MT_UPPER_AS_TEN)


   @staticmethod
   @log_func_name
   def get_ms_upper_as_average_table() -> str:
      """Returns message that sm_upper now reaching average table."""
      return random.choice(
         mult_questions.data_sm.MT_UPPER_AS_AVG_TABLE)


   @staticmethod
   @log_func_name
   def get_ms_freq_average_table() -> str:
      """Returns message that the center of truncnorm is still on average table. 
      AKA - starting to be outside user's comfort level."""
      return random.choice(
         mult_questions.data_sm.MT_FREQ_AVG_TABLE)


   @staticmethod
   @log_func_name
   def get_ms_relative_difficulty(
      handler_input, 
      player_obj: object = None,
      answered_tables: list = None,
   ) -> str:
      """Returns message depending on z_score from higher table diff."""
      z_score = UserStats.get_higher_table_difficulty(
         handler_input, player_obj= player_obj, answered_tables= answered_tables)
      z_score = int( z_score)

      random_num = random.random()
      if (z_score < - 1) and (random_num < z_score * -0.23):
         return SMQuestions.get_low_z_score_question()

      elif (z_score in (-1, 0, 1)) and (random_num <= 0.55):
         return SMQuestions.get_normal_question()
      
      elif (z_score > 1) and (random_num < z_score * 0.23):
         return SMQuestions.get_high_z_score_question()
      
      else:
         return SMQuestions.get_no_question_intro()


   @staticmethod
   @log_func_name
   def get_low_z_score_question() -> str:
      """Returns message for the negative z_score difficulty."""
      return random.choice(
         mult_questions.data_sm.MT_EASY_QUESTIONS)


   @staticmethod
   @log_func_name
   def get_normal_question() -> str:
      """Returns message for normal difficulty questions."""
      return random.choice(
         mult_questions.data_sm.MT_NORMAL_QUESTIONS)


   @staticmethod
   @log_func_name
   def get_high_z_score_question() -> str:
      """Returns message for high z_score difficulty."""
      return random.choice(
         mult_questions.data_sm.MT_HARD_QUESTIONS)


   @staticmethod
   @log_func_name
   def get_no_question_intro() -> str:
      """Function used for logging purposes."""
      return ""
