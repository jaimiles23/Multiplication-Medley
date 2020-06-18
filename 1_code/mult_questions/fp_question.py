""""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 13:29:40
 * @modify date 2020-05-25 16:40:45
 * @desc [
    FPQuestions utility class. methods for  for:
    - Overall (master method)
    - Rephrase questions
    - get multiplication question
 ]
 */
"""

##########
# Imports
##########

import random


from logs import log_func_name, logger
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from free_play.fp_logic import FreePlayLogic
from skill_card.card_funcs import CardFuncs

from mult_questions.question_attr import QuestionAttr
from mult_questions.gen_questions import GenQuestions
from mult_questions.question_messages import AllQuestionIntros
import mult_questions.data


##########
# Free Play Problems Utility class
##########

class FPQuestions(object):
    ##########
    # Overall
    ##########
    @staticmethod
    @log_func_name
    def get_question(handler_input, first_question: bool = False) -> str:
        """Asks the user a multiplication question within customized barriers"""
        attr = handler_input.attributes_manager.session_attributes

        if not first_question:
            QuestionAttr.increment_questions_answered(handler_input)

        question_tables = FPQuestions.get_multiplication_question(handler_input)
        QuestionAttr.save_question(handler_input, question_tables)
        question = GenQuestions.format_question(question_tables)

        if (random.random() < 0.05) and (not first_question):
            ms_confirm = random.choice( mult_questions.data.MT_CONFIRM) + ' '
        else:
            ms_confirm = ''

        if first_question:
            ms_intro = AllQuestionIntros.get_first_question_intro()

        elif random.random() < 0.4:
            ms_intro = AllQuestionIntros.get_question_intro_as_interrogative(handler_input)
        else:
            ms_intro = FPQuestions.get_rand_question_intro(handler_input)

        ## Punct for interrogative
        if attr.get('interrogative_question', False):
            punct = '?'
            attr['interrogative_question'] = False
        else:
            punct = ''
        
        speech_list = (ms_confirm, ms_intro, ' ', question, punct)
        speech = ''.join(speech_list)
        return CardFuncs.format_prompt(speech)


    ##########
    # Rephrased
    ##########
    @staticmethod
    @log_func_name
    def get_rephrased_question(handler_input) -> str:
        """Returns rephrased question"""
        speech_list = []
        question = GenQuestions.get_same_question(handler_input)
        
        if random.random() < 0.5:
            ms_intro = AllQuestionIntros.get_question_intro_as_interrogative(handler_input)
            punct = '?'
        else:
            ms_intro = FPQuestions.get_rand_question_intro(handler_input)
            punct = ':'
        
        speech_list = (ms_intro, ' ', question, punct)
        return ''.join(speech_list)


    ##########
    # Multiplication question
    ##########
    @staticmethod
    @log_func_name
    def get_multiplication_question(handler_input, integer: bool = False) -> tuple:
        """Returns tuple of times tables for question to user."""
        attr = handler_input.attributes_manager.session_attributes
        times_tables = attr['times_tables']

        lower_bound = attr.get('lower_bound', None)
        upper_bound = attr.get('upper_bound', None)
        lower_bound = int(lower_bound) if lower_bound else 0
        upper_bound = int(upper_bound) if upper_bound else max(times_tables)

        num_1 = random.choice( times_tables)
        num_2 = random.randint( lower_bound, upper_bound)
        if not integer:
            num_1, num_2 = str(num_1), str(num_2)
        return (num_1, num_2)


    ##########
    # Question Speech
    ##########
    @staticmethod
    @log_func_name
    def get_rand_question_intro(handler_input) -> str:
        """Returns message for the question's intro."""
        rand_percent = random.random()

        if rand_percent < 0.25:
            return AllQuestionIntros.get_ms_intro_question_num(handler_input)
        
        elif rand_percent < 0.6:
            return AllQuestionIntros.get_ms_intro_long()
        
        return ' '

