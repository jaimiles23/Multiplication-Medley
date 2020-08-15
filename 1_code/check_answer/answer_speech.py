"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-14 11:31:58
 * @modify date 2020-06-16 15:53:59
 * @desc [
     Utility class to get answer message.
]*/"""

##########
# Imports
##########

from logs import logger, log_func_name
from aux_utils.create_tuple_message_clauses import get_linear_nlg

from mult_questions.question_attr import QuestionAttr
from slots.slot_utils import SlotUtils
import check_answer.data


##########
# General Utility Methods
##########

class GetAnswerSpeech(object):

    @staticmethod
    @log_func_name
    def get_ms_answer(handler_input, include_correct_ans: bool = True) -> str:
        """Returns message of what the answer is.

        Format: Num1 * Num2 = Num3"""
        table_1, table_2 = QuestionAttr.get_question_tables(handler_input, integers=True)
        user_answer = SlotUtils.get_slot_val_by_name(handler_input, 'answer')
        answer = str(table_1 * table_2) + '.'

        ms_question = check_answer.data.MS_QUESTION.format(
            table_1, table_2)
        
        speech_list = [
            ms_question, 
            check_answer.data.MT_EQUALS,
            answer,
        ]
        if include_correct_ans:
            ms_ans = check_answer.data.MS_NOT_ANS.format(
                user_answer)
            speech_list.append(ms_ans)
            
        return get_linear_nlg(speech_list)
        



