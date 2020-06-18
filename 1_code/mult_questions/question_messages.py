"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 17:29:38
 * @modify date 2020-05-25 16:40:55
 * @desc [
    AllQuestionIntros util class for messages that are not class specific.
    Methods to get message for:
    - First question
    - Interrogative Questions
    - Question intros
    - retry question
    - 
 ]
 */
"""

##########
# Imports
##########

import random

from logs import logger, log_func_name
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from pause.pauser import Pauser

from mult_questions.gen_questions import GenQuestions
import mult_questions.data


##########
# Survival Mode Questions
##########

class AllQuestionIntros(object):
    
    ##########
    # First Question
    ##########
    @staticmethod
    @log_func_name
    def get_first_question_intro() -> str:
        """Returns introduction for the first free play question asked."""        
        return get_ms_from_tuple( 
            mult_questions.data.MMT_FIRST_QUESTION) + "."


    ##########
    # Interrogative Questions
    ##########
    @staticmethod
    @log_func_name
    def get_question_intro_as_interrogative(handler_input) -> str:
        """Returns interrogative form of question"""
        attr = handler_input.attributes_manager.session_attributes
        attr['interrogative_question'] = True

        return random.choice( 
            mult_questions.data.MT_QUESTION_INTRO)


    ##########
    # Question Intros
    ##########
    @staticmethod
    @log_func_name
    def get_ms_intro_question_num(handler_input) -> str:
        """Returns message with the question number."""
        attr = handler_input.attributes_manager.session_attributes
        speech_list = []
        ms_num_question = get_ms_from_tuple(mult_questions.data.MMT_PROBLEM_NUM)
        questions_answered = attr['questions_answered'] + 1

        speech_list.append( ms_num_question)
        speech_list.append( str(questions_answered) + '.')
        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_intro_long() -> str:
        """Returns message with long question introduction."""
        return random.choice(
            mult_questions.data.MT_LONG_INTRO)


    ##########
    # Retry Question
    ##########
    @staticmethod
    @log_func_name
    def get_retry_question(handler_input) -> str:
        """Returns the same question to retry."""
        question = GenQuestions.get_same_question(handler_input)
        
        ms_retry = AllQuestionIntros.get_ms_retry_question(handler_input)
        speech_list = (ms_retry, question)
        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_retry_question(handler_input) -> str:
        """Returns message to retry the question."""
        attr = handler_input.attributes_manager.session_attributes
        consecutive_incorrect = attr.get('consecutive_incorrect', 0)

        if consecutive_incorrect == 1:
            mt = mult_questions.data.MT_FIRST_RETRY
        else:
            mt = mult_questions.data.MT_MULT_RETRY
        return random.choice(mt)

