"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-13 21:41:51
 * @modify date 2020-05-26 19:09:15
 * @desc [
    QuestionAttr utility class to manage session attributes. methods for:
    - General
    - 
 ]
 */
"""

##########
# Imports
##########

from logs import log_func_name, logger


##########
# Question attr.
##########

class QuestionAttr(object):

    ##########
    # General
    ##########

    @staticmethod
    @log_func_name
    def increment_questions_answered(handler_input, increase: bool = True) -> None:
        """Increments questions asked."""
        attr = handler_input.attributes_manager.session_attributes
        questions_answered = attr.get('questions_answered', 0)

        if increase:
            questions_answered += 1
        else:
            questions_answered -= 1
        
        attr['questions_answered'] = questions_answered
        return
    

    @staticmethod
    @log_func_name
    def save_question(handler_input, question: tuple) -> None:
        """Saves current question."""
        attr = handler_input.attributes_manager.session_attributes
        attr['question'] = question
    

    @staticmethod
    @log_func_name
    def get_question_tables(handler_input, integers: bool = True) -> tuple:
        """Returns tuple of the question's times tables.
        
        Optional intergers argument determines if returned as ints or strs."""
        attr = handler_input.attributes_manager.session_attributes
        question = attr.get('question', None)

        if question:
            table_1, table_2 = question[0], question[1]
        else:
            table_1, table_2 = None, None

        if integers and (table_1 is not None):
            table_1, table_2 = int(table_1), int(table_2)
        if (not integers) and (table_1 is not None):
            table_1, table_2 = str(table_1), str(table_2)
            
        return (table_1, table_2)

