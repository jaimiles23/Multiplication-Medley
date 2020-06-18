"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-08 12:20:45
 * @modify date 2020-05-15 10:46:49
 * @desc [
    FreePlayLogic utility class to guide Handler logic:
    - Check table input
    - number questions
    - 
 ]
 */
"""

##########
# Imports
##########

from logs import log_func_name, logger


##########
# FreePlayLogic Utility class
##########

class FreePlayLogic(object):

    ##########
    # Check Table Input
    ##########

    @staticmethod
    @log_func_name
    def check_tables_provided(lower_table: str, upper_table: str, tables_query: list) -> bool:
        """Boolean if times table input provided by the user."""
        flag_tables_provided = False

        if lower_table is not None and upper_table is not None:
            flag_tables_provided = True
        elif tables_query is not None:
            flag_tables_provided = True
            
        return flag_tables_provided
    

    @staticmethod
    @log_func_name
    def check_tables_exist(handler_input) -> bool:
        """Returns boolean indicating if the tables already existed."""
        attr = handler_input.attributes_manager.session_attributes
        times_tables = attr.get('times_tables', None)

        flag_tables_exist = False
        if times_tables is not None and len(times_tables) > 0:
            flag_tables_exist = True
        
        return flag_tables_exist


    @staticmethod
    @log_func_name
    def check_num_questions(handler_input) -> bool:
        """Returns boolean if num_questions were specified."""
        attr = handler_input.attributes_manager.session_attributes
        num_questions = attr.get('num_questions', 0)
        return (num_questions is not None)
    
    
    @staticmethod
    @log_func_name
    def check_table_bounds_provided(lower_bound: int, upper_bound: int) -> bool:
        """Checks if the range of times tables were provided."""
        return (
            (lower_bound is not None) or 
            (upper_bound is not None)
        )


    ##########
    # Number Questions
    ##########

    @staticmethod
    @log_func_name
    def check_first_question(handler_input) -> bool:
        """Returns boolean indicating if first answer in Free Play mode."""
        attr = handler_input.attributes_manager.session_attributes
        questions_answered = attr.get('questions_answered', 0)
        return (int(questions_answered) == 1)


    @staticmethod
    @log_func_name
    def check_asked_requested_questions(handler_input) -> bool:
        """Checks the number of questions asked to the user."""
        attr = handler_input.attributes_manager.session_attributes
        num_questions = attr.get('num_questions', None)
        questions_answered = attr.get('questions_answered', 0)

        if not num_questions:
            return False
        
        logger.debug(questions_answered)
        logger.debug(num_questions)
        return (int(questions_answered) + 1 == int(num_questions))

