"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-23 11:39:37
 * @modify date 2020-06-16 17:12:19
 * @desc [
    Utility class for Custom Practice attributes. Methods to:
        - Mode attributes
        - Update last question attr
        - Get the table mean error list
        - Determine practice tables
        - Determine practice type
        - Manage incorrect questions

TODO List:
    - Refactor this code. Practice type methods likely in a different class.
    at the very least, make order more sequential, e.g., determine practice type before quesitons.
 ]
 */
"""


##########
# Imports
##########

from math import sqrt
from statistics import mean, stdev


from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from mult_questions.question_attr import QuestionAttr
from aux_utils.z_score import calc_z_score

from custom_practice.cp_utils import CP_Utils
import custom_practice.data


##########
# Custom Practice Attributes
##########

class CP_Attr(object):

    ##########
    # Start & End
    ##########
    @staticmethod
    @log_func_name
    def set_attr_start_cp(handler_input) -> None:
        """Sets sesh attributes for starting custom practice."""
        attr = handler_input.attributes_manager.session_attributes

        attr['mode'] = 'custom'
        attr['help_pointer'] = 'custom_practice'
        attr['last_question'] = False

        attr['times_tables'] = []

        attr['cp_consecutive_correct'] = -1     # increment to 0 on start handler  
        attr['consecutive_correct'] = 0

        attr['tbl_list_mean_errs'] = []
        return None
    

    @staticmethod
    @log_func_name
    def set_attr_new_practice(handler_input) -> None:
        attr = handler_input.attributes_manager.session_attributes
        attr['times_tables'] = []
        attr['last_question'] = False
        
        ## Both increment 1 on handler.
        attr['cp_consecutive_correct'] = -1
        attr['consecutive_correct'] = -1

        attr['tbl_list_mean_errs'] = []
        return None


    @staticmethod
    @log_func_name
    def set_attr_end_cp(handler_input) -> None:
        """Sets sesh attributes for ending custom practice."""
        attr = handler_input.attributes_manager.session_attributes

        reset_cp_attrs = (
            'mode',
            'help_pointer',
            'tbl_list_mean_errs',
            'times_tables',
            'cp_consecutive_correct',
            'last_question'
        )
        for cp_at in reset_cp_attrs:
            attr[cp_at] = 0
        
        return None


    ##########
    # Practice Type
    ##########
    @staticmethod
    @log_func_name
    def save_practice_type(handler_input, practice_type: str) -> None:
        """Saves the practice type as a session attribute."""
        attr = handler_input.attributes_manager.session_attributes
        attr['practice_type'] = practice_type
        return None


    ##########
    # Last question
    ##########
    @staticmethod
    @log_func_name
    def update_last_question_attr(handler_input, correct: bool) -> None:
        """Updates last question boolean session attribute.
        
        NOTE: Only call when question is correct."""
        attr = handler_input.attributes_manager.session_attributes
        if attr.get('mode', None) != 'custom':
            return None
        
        practice_type = attr.get('practice_type', None)
        if practice_type == custom_practice.data.PRACT_TYPES[0] and correct:
            attr['last_question'] = (not CP_Attr.check_more_than_one_incorrect_question(handler_input))
        
        elif practice_type != custom_practice.data.PRACT_TYPES[0]:
            CP_Attr.adjust_cp_consec_correct(handler_input, correct)
            
            next_consec_correct = int(attr['cp_consecutive_correct']) + 1
            max_questions = custom_practice.data.QUESTIONS_PER_MODE
            log_all( next_consec_correct, max_questions)
            
            attr['last_question'] = next_consec_correct == max_questions  

        return None


    @staticmethod
    @log_func_name
    def check_more_than_one_incorrect_question(handler_input) -> bool:
        """Returns boolean if > 1 incorrect question to practice.

        NOTE: Question removed when correct, 
        so if only 1 question, it is last question.
        """
        attr = handler_input.attributes_manager.session_attributes
        wrong_quest_by_date = attr['wrong_quest_by_date']
        logger.debug(wrong_quest_by_date)

        if len(wrong_quest_by_date.keys()) > 1:
            return True
        
        date_key = list(wrong_quest_by_date.keys())[0]
        date_dict = wrong_quest_by_date[date_key]
        if len(date_dict.keys()) > 1:
            return True
        
        table1_key = list(date_dict.keys())[0]
        table1_dict = date_dict[table1_key]

        if len(table1_dict.keys()) > 1:
            return True
        
        table2_key = list(table1_dict.keys())[0]
        table2_val = table1_dict[table2_key]

        if CP_Utils.reduce_num_incorrect(table2_val) == 1:
            return False

        return True


    @staticmethod
    @log_func_name
    def check_last_question(handler_input) -> bool:
        """Checks if last question for session attribute."""
        attr = handler_input.attributes_manager.session_attributes
        return attr.get('last_question', False)


    ##########
    # Tbl mean err list
    ##########
    @staticmethod
    @log_func_name
    def set_tbl_mean_err_list_attr(handler_input, player_obj: object) -> None:
        """Sets table mean error list as a session attribute.

        List of tuples, [(times_table, mean_error),]
        Sorted in descending order by mean error.
        """
        attr = handler_input.attributes_manager.session_attributes

        times_tables_info = player_obj.get_times_table_info()
        tbl_list_mean_errs = []

        table_keys = list(times_tables_info.keys())
        for table in table_keys:
            mean_err = (1 - times_tables_info[table]['mean'])
            tbl_err = (table, mean_err)

            tbl_list_mean_errs.append(tbl_err)
        
        tbl_list_mean_errs.sort(key= lambda x: x[1], reverse= True)
        attr['tbl_list_mean_errs'] = tbl_list_mean_errs
        
        logger.info(tbl_list_mean_errs)
        return None


    ##########
    # Get tables to practice
    ##########
    @staticmethod
    @log_func_name
    def get_top_high_err_tables(handler_input) -> list:
        """Returns list of the top 3 high error tables."""
        attr = handler_input.attributes_manager.session_attributes

        tbl_list_mean_errs = attr['tbl_list_mean_errs']
        tables_to_practice = []

        for i in range(3):
            if tbl_list_mean_errs[i][1] > custom_practice.data.HIGH_ERR_THRESHOLD:
                tables_to_practice.append( tbl_list_mean_errs[i][0])
        tables_to_practice.sort()
        logger.debug(tables_to_practice)
        return tables_to_practice
    

    @staticmethod
    @log_func_name
    def get_top_z_score_err_tables(handler_input) -> list:
        """Returns list of the top 3 z-score error tables."""
        attr = handler_input.attributes_manager.session_attributes

        tbl_list_mean_errs = attr['tbl_list_mean_errs']
        tbl_means = [ num[1] for num in tbl_list_mean_errs]
        tables_to_practice = []

        tbl_mean_err = mean(tbl_means)
        tbl_mean_stdev = stdev(tbl_means, xbar = tbl_mean_err)

        for i in range(3):
            table, table_err = tbl_list_mean_errs[i]

            tbl_z_score = calc_z_score(
                data_point = table_err,
                data_mean= tbl_mean_err,
                data_stdev= tbl_mean_stdev,
            )

            if tbl_z_score > custom_practice.data.HIGH_Z_SCORE_ERR:
                tables_to_practice.append( table )
        
        tables_to_practice.sort()
        logger.debug( tbl_list_mean_errs)
        logger.debug( tables_to_practice)
        return tables_to_practice


    ##########
    # Practice Type 
    ##########
    @staticmethod
    @log_func_name
    def adjust_cp_consec_correct(handler_input, correct: bool) -> None:
        """Increments consecutive correct for custom practice."""
        attr = handler_input.attributes_manager.session_attributes
        cp_consecutive_correct = attr.get('cp_consecutive_correct', -1)
        ## Add 1 on start handler, becomes zero.

        if correct:
            cp_consecutive_correct += 1
        else:
            cp_consecutive_correct = 0

        attr['cp_consecutive_correct'] = cp_consecutive_correct
        return None


    @staticmethod
    @log_func_name
    def set_pract_type_attr(handler_input, player_obj: object, pract_type: str) -> None:
        """Master function to set attributes for passed practice type."""
        PRACT_TYPE_AND_ATTR = {
            custom_practice.data.PRACT_TYPES[0]    :   CP_Attr.set_pract_incorrect_questions_attr,
            custom_practice.data.PRACT_TYPES[1]    :   CP_Attr.set_pract_high_err_attr,
            custom_practice.data.PRACT_TYPES[2]    :   CP_Attr.set_pract_high_z_score_attr,
            custom_practice.data.PRACT_TYPES[-1]   :   CP_Attr.set_pract_new_tables_attr,
        }
        return PRACT_TYPE_AND_ATTR[pract_type](handler_input, player_obj)


    @staticmethod
    @log_func_name
    def set_pract_incorrect_questions_attr(handler_input, player_obj: object) -> None:
        """Sets attributes for incorrect question practice.
        
        NOTE: None yet??
        """
        attr = handler_input.attributes_manager.session_attributes

        return None


    @staticmethod
    @log_func_name
    def set_pract_high_err_attr(handler_input, player_obj: object) -> None:
        """Sets attributes for high error table practice."""
        attr = handler_input.attributes_manager.session_attributes

        CP_Attr.set_tbl_mean_err_list_attr(handler_input, player_obj)
        tbl_list_mean_errs = attr['tbl_list_mean_errs']
        practice_tables = []
        
        for i in range(3):
            table, mean_err = tbl_list_mean_errs[i]
            if mean_err > custom_practice.data.HIGH_ERR_THRESHOLD:
                practice_tables.append( table)
        
        attr['times_tables'] = practice_tables
        return None


    @staticmethod
    @log_func_name
    def set_pract_high_z_score_attr(handler_input, player_obj: object) -> None:
        """Sets attributes for high z-score practice."""
        attr = handler_input.attributes_manager.session_attributes

        CP_Attr.set_tbl_mean_err_list_attr(handler_input, player_obj)
        tbl_list_mean_errs = attr['tbl_list_mean_errs']
        

        tbl_means_only = [val[1] for val in tbl_list_mean_errs]
        total_err_mean = mean(tbl_means_only)
        total_err_stdev = stdev(tbl_means_only, xbar= total_err_mean)

        practice_tables = []
        for i in range(3):
            table, mean_err = tbl_list_mean_errs[i]

            tbl_z_score = calc_z_score(
                data_point= mean_err,
                data_mean= total_err_mean,
                data_stdev= total_err_stdev,
            )

            if tbl_z_score > custom_practice.data.HIGH_Z_SCORE_ERR:
                practice_tables.append( table)
        
        attr['times_tables'] = practice_tables
        return None


    @staticmethod
    @log_func_name
    def set_pract_new_tables_attr(handler_input, player_obj: object) -> None:
        """Sets attributes for new tables practice."""
        attr = handler_input.attributes_manager.session_attributes
        answered_tables = player_obj.get_answered_tables()

        avg_tbl = mean(answered_tables)
        tbl_stdev = stdev(answered_tables, xbar = avg_tbl)

        table_1, table_2 = int(avg_tbl + tbl_stdev), int(avg_tbl +  2 * tbl_stdev)

        practice_tables = []
        for table in range(table_1, table_2 + 1):
            practice_tables.append(table)

            if len(practice_tables) > 3:
                break
        
        attr['times_tables'] = practice_tables
        return None


    ##########
    # Incorrect Question attribute mngment
    ##########
    @staticmethod
    @log_func_name
    def remove_question_from_incorrect_questions(handler_input) -> None:
        """Removes the question from the incorrect questions.
        
        Also checks if dictionary is empty and deletes.
        """
        attr = handler_input.attributes_manager.session_attributes
        wrong_quest_by_date = attr['wrong_quest_by_date']

        date_key = CP_Utils.get_oldest_date(wrong_quest_by_date)
        date_dict = wrong_quest_by_date[date_key]

        table_1, table_2 = QuestionAttr.get_question_tables(handler_input, integers = False)
        
        log_all( date_dict, table_1, table_2)
        
        table_1_dict = date_dict[table_1]
        num_incorrect = table_1_dict[table_2]
        log_all(table_1_dict, num_incorrect)

        ## Reduce counts of incorrect.
        num_incorrect = CP_Utils.reduce_num_incorrect(num_incorrect)

        ## Resave dictionaries.
        table_1_dict[table_2] = num_incorrect
        date_dict[table_1] = table_1_dict
        wrong_quest_by_date[date_key] = date_dict

        log_all(table_1_dict, date_dict, wrong_quest_by_date)

        ## Should refactor into many different methods.
        logger.debug(num_incorrect)
        if num_incorrect == 1:      # already asked, so delete & any unnecessary dicts
            CP_Attr.del_dict_key(table_1_dict, key = table_2)

            if len(table_1_dict.keys()) == 0:
                CP_Attr.del_dict_key(date_dict, table_1)
            
                if len(date_dict.keys()) == 0:
                    CP_Attr.del_dict_key(wrong_quest_by_date, key = date_key)
                    
        logger.debug(wrong_quest_by_date)
        attr['wrong_quest_by_date'] = wrong_quest_by_date
        return


    @staticmethod
    @log_func_name
    def del_dict_key(dict_to_del: dict, key) -> dict:
        """Util method to del key from dictionary and return dict.

        Key type may be int or str in ISO date format."""
        logger.debug(key)
        logger.debug(dict_to_del)

        del dict_to_del[key]

        return dict_to_del

