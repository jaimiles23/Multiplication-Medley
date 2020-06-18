"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-13 22:22:55
 * @modify date 2020-06-16 15:58:04
 * @desc [
     QuestionChecker class. Returns boolean if user answer was correct.
 ]
 */
"""

##########
# Imports
##########

from logs import log_func_name, logger
from slots.slot_utils import SlotUtils

from mult_questions.question_attr import QuestionAttr


##########
# Question Checker
##########

class QuestionChecker(object):

    @staticmethod
    @log_func_name
    def check_answer(handler_input) -> bool:
        """Returns boolean if user answer is correct."""
        table_1, table_2 = QuestionAttr.get_question_tables(handler_input, True)
        answer = SlotUtils.get_slot_val_by_name(handler_input, 'answer')
        
        if not answer:
            logger.warning("check_answer: No answer found.")
            return False

        return (table_1 * table_2 == int(answer))

