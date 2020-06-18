"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-14 23:34:56
 * @modify date 2020-06-16 14:25:30
 * @desc [
    Utility class for getting congrat level. Methods for:
        - get excite level
        - manage excite level
        - calculate excite level
        - get level for consecutive correct
 ]
 */
"""

##########
# Imports
##########

import random


from logs import log_func_name, logger
from mult_questions.question_attr import QuestionAttr
from players.players_dict import PlayerDict
from stats.user_stats import UserStats


##########
# Congrat Levels
##########

class CongratLevel(object):

    @staticmethod
    @log_func_name
    def get_excite_level(
        handler_input, 
        excite_level: int = -1, 
        player_obj: object = None,
        survival_mode: bool = False,
        ):
        """Returns excitement level.

        If excitement level is not -1, will return existing excite level.
        Else, calculates and manages excite level."""
        if excite_level != -1:
            return excite_level

        excite_level = CongratLevel.calculate_excite_level(
            handler_input, player_obj = player_obj, survival_mode = survival_mode)
        return CongratLevel.manage_excite_level(excite_level)


    @staticmethod
    @log_func_name
    def manage_excite_level(excite_level: int) -> int:
        """Wrapper cleaned congrat level. 

        Includes some random variation and enforces max."""
        if (random.random() <= 0.05):        # arbitrary chance to increase
            logger.debug("manage_excite_level:   arb increase.")
            excite_level += 1

        if excite_level >= 3:
            excite_level = random.choice([2, 2, 3])     # Reduce chance of high excite.
        elif excite_level == 0:
            excite_level += 0.01    # avoid ZeroDivisionError
        
        logger.debug(excite_level)
        return excite_level


    @staticmethod
    @log_func_name
    def calculate_excite_level(
        handler_input, 
        player_obj: object = None,
        survival_mode: bool = False) -> int:
        """Returns congratulations level to return to the user.

        Conditions checked:
        - Consecutive incorrect
        - Consecutive correct
        - If user has high (f) error on table
        - Table difficulty vs average table difficulty
        """
        attr = handler_input.attributes_manager.session_attributes
        
        consecutive_incorrect = attr.get('consecutive_incorrect', 0)
        consecutive_correct = attr.get('consecutive_correct', 0)
        consecutive_correct = (consecutive_correct + 1) if consecutive_correct is not None else 1
        excite_level = 0

        if consecutive_incorrect and (not survival_mode):
            return consecutive_incorrect - (1 - random.random())

        elif ((consecutive_correct) % 5 == 0) and (not survival_mode):
            return CongratLevel.get_level_consecutive_correct(consecutive_correct)
        
        tables = QuestionAttr.get_question_tables(handler_input, integers= False)
        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)
        
        ## Check table error frequency
        higher_f_error = UserStats.get_higher_table_error_freq(
            handler_input, player_obj = player_obj, tables = tables)
        logger.debug(f"higher_f_error   {higher_f_error}")

        if higher_f_error >= 1.5:       ## Arbitrary value. NOTE: Revist.
            return higher_f_error
        
        ## Check Relative Table difficulty
        higher_table_difficulty = UserStats.get_higher_table_difficulty(
            handler_input, player_obj = player_obj, tables = tables)
        logger.debug(f"higher_table_difficulty  {higher_table_difficulty}")
        if higher_table_difficulty > 1.5:
            return higher_table_difficulty
        
        return excite_level


    @staticmethod
    @log_func_name
    def get_level_consecutive_correct(consecutive_correct: int) -> int:
        """Returns excitement level for consecutive correct.
        
        Random chance for different levels."""
        excitement_level = random.choice([
            1, 1, 2, (consecutive_correct) // 10
            ])
        return excitement_level

