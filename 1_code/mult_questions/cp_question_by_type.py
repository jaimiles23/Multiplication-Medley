"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-25 10:25:01
 * @modify date 2020-05-26 09:30:24
 * @desc [
    CP_QuestionByType utility class to get custom practice questions, per practice type.
    Methods for:
    - Incorrect 
    - High Error tables
    - High Z score tables
    - New Tables
 ]
 */
"""

##########
# Imports
##########

import random


from logs import log_func_name, logger

from custom_practice.cp_utils import CP_Utils
import custom_practice.data


##########
# Custom Practice Questions
##########
## TODO: need last question boolean sesh attr to check if last question. 
## This will be most helpful for incorrect problems, but used elsewhere too. 

class CP_QuestionByType(object):

    @staticmethod
    @log_func_name
    def get_question_type(
        handler_input, 
        player_object: object, 
        practice_type: str) -> str:
        """Returns problem based on the practice type passed."""
        TYPE_QUESTION_DICT = {
            custom_practice.data.PRACT_TYPES[0]     :   CP_QuestionByType.get_question_incorrect_problems,
            custom_practice.data.PRACT_TYPES[1]     :   CP_QuestionByType.get_question_high_err_table,
            custom_practice.data.PRACT_TYPES[2]     :   CP_QuestionByType.get_question_high_z_score,
            custom_practice.data.PRACT_TYPES[3]     :   CP_QuestionByType.get_question_new_tables,
        }
        
        return TYPE_QUESTION_DICT[practice_type](handler_input, player_object)


    ##########
    # Incorrect Questions
    ##########
    @staticmethod
    @log_func_name
    def get_question_incorrect_problems(handler_input, player_object) -> tuple:
        """Returns question from incorrect problems.
        
        NOTE: Question only removed when answered correctly."""
        attr = handler_input.attributes_manager.session_attributes
        wrong_quest_by_date = attr['wrong_quest_by_date']
        logger.debug(wrong_quest_by_date)
        date_key = CP_Utils.get_oldest_date(wrong_quest_by_date)
        logger.debug(date_key)
        
        oldest_date_dict = wrong_quest_by_date[date_key]
        logger.debug(oldest_date_dict)
        table_1 = random.choice( list( oldest_date_dict.keys()))
        logger.debug(table_1)

        table_1_dict = oldest_date_dict[table_1]
        logger.debug(table_1_dict)
        table_2 = random.choice( list( table_1_dict.keys()))
        logger.debug(table_2)

        return table_1, table_2


    ##########
    # High Error Tables
    ##########
    """
    NOTE: I think that all CP questions except incorrect problems can use the same 
    retrieval method. Keeping separate for now as i make different considerations
    for each method.
    """
    @staticmethod
    @log_func_name
    def get_question_high_err_table(handler_input, player_object) -> tuple:
        """Returns question from high error tables problems."""
        attr = handler_input.attributes_manager.session_attributes
        times_tables = attr['times_tables']

        num_1 = int(random.choice(times_tables))
        lower_bound = 0
        upper_bound = 12 if (num_1 <= 12) else num_1

        num_2 = random.choice( range(lower_bound, upper_bound))
        return (num_1, num_2)


    ##########
    # High Z Score Tables
    ##########
    @staticmethod
    @log_func_name
    def get_question_high_z_score(handler_input, player_object) -> tuple:
        """Returns question from table with high z_scores."""
        attr = handler_input.attributes_manager.session_attributes
        times_tables = attr['times_tables']

        num_1 = int(random.choice(times_tables))
        lower_bound = 0
        upper_bound = 12 if (num_1 <= 12) else num_1

        num_2 = random.choice( range(lower_bound, upper_bound))
        return (num_1, num_2)


    ##########
    # New Tables
    ##########
    @staticmethod
    @log_func_name
    def get_question_new_tables(handler_input, player_object) -> tuple:
        """Returns question from new times tables."""
        attr = handler_input.attributes_manager.session_attributes
        times_tables = attr['times_tables']

        num_1 = int(random.choice(times_tables))
        lower_bound = 0
        upper_bound = 12 if (num_1 <= 12) else num_1

        num_2 = random.choice( range(lower_bound, upper_bound))
        return (num_1, num_2)

