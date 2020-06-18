"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-11 11:52:10
 * @modify date 2020-05-13 17:15:45
 * @desc [
    FPNumQuestions Utility class for asking and answering number of questions.
 ]
 */
"""

##########
# Imports
##########

import random

from answer_response.congrat_utils import CongratUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.try_saying import get_ms_try_saying
from logs.log_decorators import log_func_name
import free_play.data


##########
# NumQuestions Object
##########

class FPNumQuestions(object):

    @staticmethod
    @log_func_name
    def get_ms_ask_num_questions(handler_input) -> str:
        """Returns message how many questions will ask user."""
        attr = handler_input.attributes_manager.session_attributes
        num_questions = attr['num_questions']
        
        speech_list = list( free_play.data.MMT_SET_QUESTIONS)
        speech_list.append( num_questions)
        speech_list.append( random.choice(
            free_play.data.MT_QUESTIONS))
            
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_can_set_num_questions() -> str:
        """Returns message that can set the number of questions."""
        ms_can_ask = get_ms_from_tuple( free_play.data.MMT_NUM_QUESTIONS)
        return ms_can_ask


    @staticmethod
    @log_func_name
    def get_q_num_questions() -> str:
        """Returns prompt asking how many questions to ask."""
        ms_try_saying = get_ms_try_saying()
        ms_ask_me = random.choice( free_play.data.MT_ASK_ME_QUESTIONS)
        random_num = str(random.randint(3, 10))
        ms_questions = random.choice( free_play.data.MT_QUESTIONS)

        speech_list = [
            ms_try_saying, ms_ask_me, random_num, ms_questions,
        ]
        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_num_questions_answered(handler_input) -> str:
        """Returns message how many questions the user answered."""
        attr = handler_input.attributes_manager.session_attributes
        questions_answered = attr.get('questions_answered', 0)

        ms_answered_qs = get_ms_from_tuple( free_play.data.MMT_ANSWERED_QUESTIONS)
        ms_answered_qs = ms_answered_qs.format( questions_answered)
        speech_list = (
            ms_answered_qs,
        )
        return ''.join(speech_list)

