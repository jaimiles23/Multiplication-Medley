"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-22 11:59:29
 * @modify date 2020-05-26 16:20:49
 * @desc [
    SC_EndGame utility methods:
    - Format score
    - Returns user score
    - Relative score message
    - High score message
    - 
 ]
 */
"""

##########
# Imports
##########

from statistics import mean, stdev
import random


from ask_sdk_core.handler_input import HandlerInput


from logs import log_func_name, logger, log_all
from answer_response.congrat_utils import CongratUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.z_score import calc_z_score

import speed_challenge.data
from aux_data.SSML_tags import (
    MW_EXCITED_LOW,
    MW_EXCITED_MED,
    )


##########
# Utility Class
##########

class SC_EndGame(object):

    ##########
    # Format MM:SS
    ##########
    @staticmethod
    @log_func_name
    def format_score_as_minutes_seconds(sc_score_time: int) -> str:
        """Returns score as string in proper MM:SS format."""
        minutes, seconds = int(sc_score_time) // 60, int(sc_score_time) % 60
        log_all(minutes, seconds)
        if minutes != 0:
            return f"{minutes} minutes and {seconds} seconds"
        else:
            return f"{seconds} seconds"


    ##########
    # Returns user's speed challenge score
    ##########
    @staticmethod
    @log_func_name
    def get_ms_game_score(handler_input, sc_score_time: int) -> str:
        """Returns message with user's Speed Challenge score."""
        ms_completed_sc = random.choice(
            speed_challenge.data.MT_COMPLETED_SC)
                
        FIN_SC_OPTIONS = (
            SC_EndGame.get_ms_scscore_dif_sec,
            SC_EndGame.get_ms_scscore_numq_sec,
            SC_EndGame.get_ms_scscore_tblrange_sec,
        )
        rand_num = random.random()
        chance_selected = 0

        for option in FIN_SC_OPTIONS:
            chance_selected += ( 1 / len(FIN_SC_OPTIONS) + 0.01)
            if rand_num <= chance_selected:
                fin_sc_func = option
                break
        
        score_time_format = SC_EndGame.format_score_as_minutes_seconds(sc_score_time)
        ms_fin_sc = fin_sc_func(handler_input, score_time_format)

        speech_list = (ms_completed_sc, ms_fin_sc)
        return MW_EXCITED_LOW.format(' '.join(speech_list))


    @staticmethod
    @log_func_name
    def get_ms_scscore_dif_sec(handler_input, score_time_format: str) -> str:
        """Returns message for sc score indicating difficulty and seconds."""
        attr = handler_input.attributes_manager.session_attributes
        sc_diff = attr['sc_difficulty']

        return speed_challenge.data.MS_FIN_SC_DIF_SEC.format(
            sc_diff, score_time_format)
    

    @staticmethod
    @log_func_name
    def get_ms_scscore_numq_sec(handler_input, score_time_format: str) -> str:
        """Returns message for sc score of num questions answered and seconds."""
        attr = handler_input.attributes_manager.session_attributes
        questions_answered = attr['questions_answered']
        return speed_challenge.data.MS_FIN_SC_NUMQ_SEC.format(
            questions_answered, score_time_format)
    

    @staticmethod
    @log_func_name
    def get_ms_scscore_tblrange_sec(handler_input, score_time_format: str) -> str:
        """Returns message for sc score with range of tables and seconds."""
        attr = handler_input.attributes_manager.session_attributes
        lower_tbl, upper_tbl = attr['sc_tables']
        return speed_challenge.data.MS_FIN_SC_LOWTBL_UPPTBL_SEC.format(
            str(lower_tbl), str(upper_tbl), score_time_format)
    

    ##########
    # Score relative to results
    ##########
    @staticmethod
    @log_func_name
    def get_ms_score_results(
        handler_input, sc_score_time: int, player_obj: object = None) -> str:
        """Returns message about the user's Speed Challenge score."""
        attr = handler_input.attributes_manager.session_attributes
        sc_difficulty = attr['sc_difficulty']
        high_score = player_obj.get_sc_high_score(sc_difficulty)
        
        log_all( sc_score_time, high_score, sc_difficulty)

        if SC_EndGame.check_new_sc_highscore(high_score, sc_score_time):

            if SC_EndGame.check_first_highscore(high_score):
                return SC_EndGame.get_ms_first_highscore(
                        sc_difficulty, sc_score_time)

            return SC_EndGame.get_ms_new_highscore(
                    sc_difficulty, high_score, sc_score_time)

        elif SC_EndGame.check_tie_sc_highscore(high_score, sc_score_time):
            return SC_EndGame.get_ms_tied_highscore(sc_score_time)

        return SC_EndGame.get_ms_relative_record(player_obj, sc_difficulty, sc_score_time)


    ########### First High score
    @staticmethod
    @log_func_name
    def check_first_highscore( high_score: float) -> bool:
        """Returns bool if first highscore in difficulty."""
        if (high_score is None):
            return True
        return False
    

    @staticmethod
    @log_func_name
    def get_ms_first_highscore(sc_difficulty: str, sc_score_time: int) -> str:
        """Returns message for first highscore in Speed Challenge difficulty."""
        score_time_format = SC_EndGame.format_score_as_minutes_seconds( sc_score_time)
        return speed_challenge.data.MS_FIRST_HS.format(
            sc_difficulty, score_time_format)


    ########## New High Score
    @staticmethod
    @log_func_name
    def check_new_sc_highscore( high_score: float, sc_score_time: int) -> bool:
        """Returns boolean if new highscore for speed challenge difficulty."""
        if (high_score is None):
            return True
        return (sc_score_time < high_score)
    

    @staticmethod
    @log_func_name
    def get_ms_new_highscore(
        sc_difficulty: str, high_score: float, sc_score_time: int) -> str:
        """Returns message for new highscore for speed challenge difficulty."""
        high_score_time_format = SC_EndGame.format_score_as_minutes_seconds( high_score)
        score_time_format = SC_EndGame.format_score_as_minutes_seconds( sc_score_time)
        
        speech_list_1 = list(speed_challenge.data.MTT_BEAT_OLD_HS)
        ms_old_hs = speed_challenge.data.MS_SC_SCORE_SECONDS.format(high_score_time_format)
        speech_list_1.append(ms_old_hs)
        speech_list_1.append(1.5)

        speech_list_2 = list(speed_challenge.data.MMT_NEW_HS)   
        ms_new_hs = speed_challenge.data.MS_FOR_DIFF_SECONDS.format(
            sc_difficulty, score_time_format)
        speech_list_2.append(ms_new_hs)

        master_speech_list = speech_list_1 + speech_list_2

        return MW_EXCITED_MED.format(
            get_ms_from_tuple(master_speech_list))
    
    
    ########## Tied High Score
    @staticmethod
    @log_func_name
    def check_tie_sc_highscore(high_score: int, sc_score_time: int) -> bool:
        """Returns boolean if tied highscore for speed challenge difficulty."""
        return (high_score == sc_score_time)
    

    @staticmethod
    @log_func_name
    def get_ms_tied_highscore(sc_score_time: int) -> str:
        """Returns message for new highscore for speed challenge difficulty."""
        score_time_format = SC_EndGame.format_score_as_minutes_seconds( sc_score_time)
        ms_tied_hs = random.choice(
                speed_challenge.data.MT_TIE_HS).format(
                    score_time_format)
        ms_close_one = random.choice(
            speed_challenge.data.MT_TIE_HS_PART_2)
        return MW_EXCITED_LOW.format(
            get_ms_from_tuple(
                [ms_tied_hs, 0.5, ms_close_one]))
    

    ########## Relative Results, AKA Z-score
    @staticmethod
    @log_func_name
    def get_ms_relative_record(
        player_obj: object, sc_difficulty: str, sc_score_time: int) -> str:
        """Returns string for the player's relative speed challenge performance."""
        sc_z_score = SC_EndGame.get_sc_performance_z_score(
            player_obj, sc_difficulty, sc_score_time)

        z_score_response_lists = (
            ( -1,   speed_challenge.data.MT_BETTER_NEXT_TIME, "{}"),
            ( 0.25, speed_challenge.data.MT_NORM_ATTEMPT,     "{}"),
            ( 1,    speed_challenge.data.MT_GOOD_ATTEMPT,     MW_EXCITED_LOW),
            ( 99,   speed_challenge.data.MT_AWESOME_ATTEMPT,  MW_EXCITED_MED),
        )

        for z_score, mt, mw in z_score_response_lists:
            if sc_z_score < z_score:
                message_tuple, ms_wrap = mt, mw
                break
        
        ms_relative_score = random.choice(message_tuple)    
        return ms_wrap.format( ms_relative_score)
    

    @staticmethod
    @log_func_name
    def get_sc_performance_z_score(
        player_obj: object, sc_difficulty: str, sc_score_time: int) -> float:
        """Returns z_score for the user's relative performance in speed challenge."""
        sc_average_records = player_obj.get_sc_average_records(sc_difficulty)
        
        if len(sc_average_records) < 2:
            return 0
        
        z_score = calc_z_score(
            data_point= sc_score_time,
            data = sc_average_records,
            )

        z_score *= -1       # inversed for time records.
        logger.debug(z_score)
        return z_score

