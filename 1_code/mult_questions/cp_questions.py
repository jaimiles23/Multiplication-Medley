"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-25 14:00:52
 * @modify date 2020-05-26 14:33:19
 * @desc [
    CP_Questions utility class to ask questions for each Practice type. Methods for:
    - Overall (master method)
    - question intros
    - 
 ]
 */
"""

##########
# Imports
##########

import random

from logs import log_func_name, logger
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from skill_card.card_funcs import CardFuncs


from custom_practice.cp_utils import CP_Utils
import custom_practice.data

from mult_questions.question_attr import QuestionAttr
from mult_questions.gen_questions import GenQuestions
from mult_questions.question_messages import AllQuestionIntros
from mult_questions.cp_question_by_type import CP_QuestionByType
import mult_questions.data
import mult_questions.data_cp


##########
# Custom Practice Utility class
##########

class CP_Questions(object):

    ##########
    # Overall
    ##########
    @staticmethod
    @log_func_name
    def get_question(
        handler_input,
        player_object: object,
        practice_type: str,
        first_question: bool = False,
    ) -> str:
        """Asks the user a multiplication question based on custom practice type."""
        attr = handler_input.attributes_manager.session_attributes
        if not first_question:
            QuestionAttr.increment_questions_answered(handler_input)
        
        flag_get_new_question = True
        while flag_get_new_question:
            new_question = CP_QuestionByType.get_question_type(
                handler_input, player_object, practice_type)

            if ( 
                not GenQuestions.check_same_question(handler_input, new_question) or 
                practice_type == custom_practice.data.PRACT_TYPES[0]    # can repeat on incorrect from date.
            ):
                flag_get_new_question = False
        
        ## Message Intro
        ms_intro = CP_Questions.get_ms_question_intro(
            handler_input, player_object, practice_type, first_question, new_question)

        ## Save Question
        QuestionAttr.save_question(handler_input, new_question)     # NOTE: Save question after for duplicates on incorrect-problems.
        ms_question = GenQuestions.format_question(new_question)

        ## Punct for interrogative
        if attr.get('interrogative_question', False):
            punct = '?'
            attr['interrogative_question'] = False
        else:
            punct = ''

        speech_list = ( ms_intro, ' ', ms_question, punct)
        speech = ''.join(speech_list)
        return CardFuncs.format_prompt(speech)


    ##########
    # Question intros
    ##########
    @staticmethod
    @log_func_name
    def get_ms_question_intro(
        handler_input, 
        player_object: object,
        practice_type: str, 
        first_question: bool,
        question: tuple,
    ) -> str:
        """Returns message for beginning of question."""

        if first_question:
            return AllQuestionIntros.get_first_question_intro()
        
        elif (
            practice_type == custom_practice.data.PRACT_TYPES[0] and
            GenQuestions.check_same_question(handler_input, question) 
        ):
            return CP_Questions.get_ms_practice_incorrect_problem_more()

        random_num = random.random()
        if random_num < 0.4:
            return AllQuestionIntros.get_question_intro_as_interrogative(handler_input)
        
        elif random_num < 0.7:
            return AllQuestionIntros.get_ms_intro_long()
        
        ## NOTE: numbering can be confusing with different practices.
        # elif random_num < 0.7:
        #     return AllQuestionIntros.get_ms_intro_question_num(handler_input)
        
        else:
            return ''


    @staticmethod
    @log_func_name
    def get_ms_practice_incorrect_problem_more() -> str:
        """Returns message that user needs to practice incorrect problem more."""
        return get_ms_from_tuple(
            mult_questions.data_cp.MMT_PRACTICE_SAME_PROBLEM )

