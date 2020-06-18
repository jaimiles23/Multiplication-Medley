"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 11:34:51
 * @modify date 2020-06-16 14:26:49
 * @desc [
    Utility class for congratulations. Following methods:
        - Get answer congrats (master method)
        - Get consecutive incorrect congrats
        - Get consecutive correct congrats
        - Get random congrats
        - Get Standard congrats
        - Get Player congrats
        - Get Buzzer
        - Get speechcon
        - get excited level message wrapper
 ]
 */
"""

##########
# Imports
##########

import random


from logs import logger, log_func_name
from mult_questions.question_attr import QuestionAttr
from players.players_dict import PlayerDict
from stats.user_stats import UserStats
from pause.pauser import Pauser
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple

from .congrat_level import CongratLevel
from .confirmation_utils import ConfirmUtils
from . import data_congrat
from aux_data.SSML_tags import (
    MW_EXCITED_LOW, MW_EXCITED_MED, MW_EXCITED_HIGH,
    MW_SPEECHCON)


##########
# Congratulations Utility class
##########

class CongratUtils(object):

    ##########
    # Overall Congrat Methods
    ##########
    @staticmethod
    @log_func_name
    def get_answer_congrats(
        handler_input, 
        player_obj: object = None, 
        survival_mode: bool = False,
        ) -> str:
        """Returns congratulations to the user for answering question."""
        attr = handler_input.attributes_manager.session_attributes

        excite_level = CongratLevel.get_excite_level(
            handler_input, player_obj = player_obj, survival_mode = survival_mode)

        consecutive_incorrect = attr.get('consecutive_incorrect', 0)
        consecutive_correct = attr.get('consecutive_correct', 0)        # updated after congrats
        consecutive_correct = (consecutive_correct + 1) if consecutive_correct else 1

        if consecutive_incorrect and (not survival_mode):
            return CongratUtils.get_consecutive_incorrect_congrats(handler_input, excite_level)
            
        elif not (consecutive_correct % 5) and (not survival_mode):
            return CongratUtils.get_consecutive_correct_congrats(handler_input, excite_level, consecutive_correct)
            
        elif (
            (random.random() < 0.75) or 
            (excite_level > 1) or 
            (survival_mode)
        ):
            return CongratUtils.get_random_congrats(
                handler_input, excite_level, survival_mode= survival_mode)
        
        else:
            return ""


    @staticmethod
    @log_func_name
    def get_consecutive_incorrect_congrats(handler_input, excite_level: int) -> str:
        """Returns congrats message for breaking consecutive incorrect."""
        ms_congrats = CongratUtils.get_random_congrats(
            handler_input, excite_level = excite_level, 
            chance_speechcon= 0.25, chance_player_congrats = 0.75)
        
        excite_wrapper = CongratUtils.get_excited_level_mw(excite_level)
        ms_broke_consecutive_incorrect = excite_wrapper.format(
            random.choice(
                data_congrat.MT_BROKE_INCORRECT_STREAK_1))
                
        speech_list = (ms_congrats, 1, ms_broke_consecutive_incorrect)
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_consecutive_correct_congrats(handler_input, excite_level: float, consecutive_correct: int) -> str:
        """Returns congrats message for consecutive correct."""
        ms_congrats = CongratUtils.get_random_congrats(
            handler_input, excite_level = excite_level,
            chance_speechcon= 0.25, chance_player_congrats = 0.75)
        
        if consecutive_correct > 5:
            consecutive_correct_ml = data_congrat.MT_CORRECT_STREAK_2
        else:
            consecutive_correct_ml = data_congrat.MT_CORRECT_STREAK_1
        excite_wrapper = CongratUtils.get_excited_level_mw(excite_level)
        ms_consecutive_correct = excite_wrapper.format(
            random.choice(
                consecutive_correct_ml).format(
                    consecutive_correct))

        speech_list = (ms_congrats, 1, ms_consecutive_correct)
        return get_ms_from_tuple(speech_list)


    ##########
    # Congrats
    ##########

    @staticmethod
    @log_func_name
    def get_random_congrats(
        handler_input, 
        excite_level: int = -1,
        chance_speechcon: float = 0.2,
        chance_player_congrats: float = 0.25,
        chance_confirmation: float = 0.4,
        chance_std_congrats: float = 0.5,
        survival_mode: bool = False,
        ):
        """Returns random congratulations from:
            - get_speechcon()               when excite > 1
            - get_player_congrats()         when excite > 1
            - get_random_confirmation()     when excite < 0
            - get_std_congrats()
            - get_buzzer()

        NOTE: speechcon & player require excite levels > 1 &
        Excite level affects chance of selection.
        """
        excite_level = CongratLevel.get_excite_level(handler_input, excite_level = excite_level)
        less_chance = 2 if survival_mode else 1

        if (        ## Speechcon
            ( excite_level >= 1) and 
            ( random.random() / excite_level <= chance_speechcon)
        ):
            return CongratUtils.get_speechcon()
        
        elif (      ## Player
            ( excite_level >= 1) and 
            ( random.random() / excite_level <= chance_player_congrats /  less_chance)
            ):
            return CongratUtils.get_player_congrats(handler_input, excite_level = excite_level)
        
        elif (      ## Confirm
            ( excite_level < 0) and
            ( random.random() / max([ (excite_level / -1.5), 1]) <= chance_confirmation)        # negative excite level increases congrats too.
            ):
            return ConfirmUtils.get_random_confirmation(handler_input, freq_player_name= 0.20)
        
        elif (      ## Std Congrats
            ( random.random() / max([ excite_level, 1]) <= chance_std_congrats) and
            ( excite_level > 0)
            ):
            return CongratUtils.get_std_congrats(handler_input, excite_level = excite_level)
        
        else:
            return CongratUtils.get_buzzer()


    @staticmethod
    @log_func_name
    def get_std_congrats(handler_input, excite_level: int = -1, punct: bool = True) -> str:
        """Returns congratulation message with level of SSML excited wrapper.

        wr_excited controls excitement wrapper:
            0 - No wrapper
            1 - Low
            2 - Medium
            3 - High
        NOTE: could add method to check if int. If not int, then randomly chooses
        b/w 2 ints?? -- probably put in other classes that call this?
        """
        excite_level = CongratLevel.get_excite_level(handler_input, excite_level= excite_level)

        congrats_statement = random.choice( data_congrat.MT_CONGRATS)
        if punct:
            congrats_statement += "!"
        mw_excite_level = CongratUtils.get_excited_level_mw(excite_level)

        return mw_excite_level.format(congrats_statement)


    @staticmethod
    @log_func_name
    def get_player_congrats(handler_input, excite_level: int = -1) -> str:
        """Returns congrats w/ player name.
        
        wr_excited controls SSML excitement wrapper:
            0 - No wrapper
            1 - Low
            2 - Medium
            3 - High
        """
        attr = handler_input.attributes_manager.session_attributes
        excite_level = CongratLevel.get_excite_level(handler_input, excite_level= excite_level)
    
        congrats_statement = random.choice( data_congrat.MT_CONGRATS)
        player_name = attr['current_player']
        speech_list = (
            congrats_statement,
            " ",
            player_name,
            "!"
        )
        mw_excite_level = CongratUtils.get_excited_level_mw(excite_level)
        return mw_excite_level.format(''.join(speech_list))


    @staticmethod
    @log_func_name
    def get_buzzer() -> str:
        """Return buzzer for correct answer."""
        return data_congrat.CORRECT_BUZZ


    @staticmethod
    @log_func_name
    def get_speechcon() -> str:
        """Returns congratulations speechcon."""
        return (
            MW_SPEECHCON.format( random.choice(
                data_congrat.MT_SPEECHCON_CONGRATS)))


    ##########
    # Message Wrapper
    ##########

    @staticmethod
    @log_func_name
    def get_excited_level_mw( excite_level) -> str:
        """Returns mw for excited level."""
        excite_level = round(excite_level)
        excite_level = excite_level if excite_level >= 0 else 0      # negative excite levels.

        return (
            data_congrat.CONGRAT_WRAPPER_DICT.get(
                excite_level, "{}"))

