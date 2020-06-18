"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-14 11:56:25
 * @modify date 2020-05-26 09:58:34
 * @desc [
   UserStats utility class to manage statistics. Methods for:
   - User stats
   - Mode stats
   - User table stats
 ]
 */
"""

##########
# Imports
##########

from statistics import mean, stdev

from logs import log_func_name, logger, log_all

from players.players_dict import PlayerDict
from mult_questions.question_attr import QuestionAttr
from aux_utils.z_score import calc_z_score

import stats.data
from stats.mode_stats import ModeStats


##########
# AnswerPlayerAttr Utility Class
##########

class UserStats(object):

    @staticmethod
    @log_func_name
    def update_player_stats(handler_input, correct: bool, player_obj: object = None) -> None:
        """Updates the user profile statistics.
        
        Increments the correct / incorrect counters.
        Updates the average tables and the info for each times table."""
        attr = handler_input.attributes_manager.session_attributes
        tables = attr['question']

        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)

        player_obj.increment_answer_counter(correct)
        player_obj.update_average_table(tables)
        player_obj.update_times_tables_info_dict(tables, correct)

        PlayerDict.save_player_obj(handler_input, player_obj)
        return


    ##########
    # Mode stats
    ##########
    @staticmethod
    @log_func_name
    def update_player_fp_stats(handler_input, player_obj: object) -> None:
        """Updates player statistics for free play mode."""
        attr = handler_input.attributes_manager.session_attributes
        mode = attr.get('mode', None)
        correct, _ = ModeStats.get_mode_stats(handler_input, mode = mode)

        return None


    @staticmethod
    @log_func_name
    def update_player_cp_stats(
        handler_input, player_obj: object = None) -> None:
        """Updates the player's Custom practice Statistics."""
        correct, incorrect = ModeStats.get_mode_stats(handler_input, 'custom')
        if correct > 3:
            player_obj.cp_plays += 1
        
        return None


    @staticmethod
    @log_func_name
    def update_player_sc_stats(
        handler_input, sc_score_time: int, player_obj: object = None) -> None:
        """Updates the player's Speed Challenge stats."""
        attr = handler_input.attributes_manager.session_attributes
        sc_difficulty = attr['sc_difficulty']

        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)

        player_obj.set_sc_high_score(sc_difficulty, sc_score_time)
        player_obj.update_sc_average_record(sc_difficulty, sc_score_time)
        player_obj.sc_plays += 1
        
        return None


    @staticmethod
    @log_func_name
    def update_player_sm_stats(handler_input, player_obj: object = None) -> None:
        """Updates the player's Survival Mode stats."""
        attr = handler_input.attributes_manager.session_attributes
        mode = attr.get('mode', None)
        correct, _ = ModeStats.get_mode_stats(handler_input, mode= mode)

        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)
        
        if correct > player_obj.get_sm_high_score():
            player_obj.set_sm_high_score(correct)
        
        player_obj.update_sm_records(correct)
        player_obj.sm_plays += 1
        PlayerDict.save_player_obj(handler_input, player_obj)

        return None


    ##########
    # User Table statistics
    ##########

    @staticmethod
    @log_func_name
    def get_higher_table_error_freq(
        handler_input, 
        player_obj: object = None,
        tables: tuple = None
        ) -> float:
        """Returns z_score for the highest error tables."""
        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)
        if tables is None:
            tables = QuestionAttr.get_question_tables(handler_input, integers=False)
        
        times_tables_info = player_obj.get_times_table_info()
        times_tables_mean_err_list = []
        
        for table in times_tables_info.keys():
            table_mean = float(times_tables_info[table]['mean'])
            table_data = times_tables_info[table]['table_data']

            if len(table_data) > stats.data.SUF_TABLE_DATA:
                times_tables_mean_err_list.append(1 - table_mean)   # inversed, so errors are higher.
        
        ## Exit if not enough data.
        if len(times_tables_mean_err_list) <= stats.data.SUF_ERR_LIST:
            return 0
        
        question_tables_err =  []
        for table in tables:
            table = str(table)
            table_info = float( times_tables_info[table]['mean'])
            table_info = (1 - table_info)   # inverse mean.
            question_tables_err.append( table_info)
        
        max_table_err = max(question_tables_err)
        z_score = calc_z_score(
            data_point= max_table_err,
            data= times_tables_mean_err_list,
        )

        return ( z_score)


    @staticmethod
    @log_func_name
    def get_higher_table_difficulty(
        handler_input, 
        player_obj: object = None,
        tables: tuple = None,
        answered_tables: list = None
        ) -> float:
        """Returns z_score for the table with the highest difficulty.
        
        Difficulty is a constructed measure dependent on greatness of tables, 
        e.g., 6 > 5."""
        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)
        if tables is None:
            tables = QuestionAttr.get_question_tables(handler_input, integers=True)
        if answered_tables is None:
            answered_tables = player_obj.get_answered_tables(integers = True)
            
        inflated_mean_table = mean(answered_tables) + 1
        higher_table = max( [int(table) for table in tables])

        z_score = calc_z_score(
            data_point= higher_table,
            data_mean = inflated_mean_table,
            data=  answered_tables,
            required_data_length= stats.data.SUF_ANSWERED_TABLES
        )
        return z_score
