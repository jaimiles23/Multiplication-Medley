"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-20 15:14:23
 * @modify date 2020-06-16 23:41:03
 * @desc [
    Mode Speech class that contains utility methods for:
    - Mode Intro
    - Survival Challenge
    - Speed Challenge
    - Can tell records
    - No records available.

    NOTE:
    May consider using median instead of mean for 'average' results of Speed Challenge and Survival Mode.

    However, mean's lack of robustness may be beneficial??
    Outliers are more likely in the slow direction (external causes),
    which will increase congratulation message to user.
 ]
 */
"""

##########
# Imports
##########

from statistics import mean
import random


from logs import logger, log_func_name, log_all
from players.players_dict import PlayerDict
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.try_saying import get_ms_try_saying

import stats.data_speech
import skill_card.data
import speed_challenge.data

from speed_challenge.end_utils import SC_EndGame


##########
# Mode Speech
##########

class ModeSpeech(object):

    ##########
    # Mode Intro
    ##########
    @staticmethod
    @log_func_name
    def get_ms_mode_intro(mode: str) -> str:
        """Returns message for mode introduction."""
        ms_mode_intro = random.choice( 
            stats.data_speech.MT_MODE_INTRO)
        mode_name = skill_card.data.CARD_TITLE_DICT[mode]
        return ms_mode_intro.format(mode_name)


    ##########
    # Survival Mode
    ##########
    @staticmethod
    @log_func_name
    def get_ms_sm_stats(player_obj: object, mode: str) -> list:
        """Returns message for user's survival mode stats."""
        ms_mode_intro = ModeSpeech.get_ms_mode_intro(mode)
        ms_average_score = ModeSpeech.get_ms_sm_average_score(player_obj)
        ms_high_score = ModeSpeech.get_ms_sm_high_score(player_obj)

        ms_catch = ModeSpeech.catch_no_records(ms_average_score, ms_high_score)
        if ms_catch:
            return ms_catch

        speech_list = [ms_mode_intro, ms_average_score, ms_high_score]
        return speech_list


    @staticmethod
    @log_func_name
    def get_ms_sm_average_score(player_obj: object) -> str:
        """Returns message for the users average SM score."""
        try:
            sm_avg_results = [int(num) for num in player_obj._sm_average_records]
            sm_avg = int( mean(sm_avg_results))
            
        except Exception as e:
            logger.warning(f"get_ms_sm_average_score: {e}")
            return None
        
        return random.choice(
            stats.data_speech.MT_SM_AVG_SCORE).format(sm_avg)


    @staticmethod
    @log_func_name
    def get_ms_sm_high_score( player_obj: object) -> str:
        """Returns message for the users SM high score."""
        sm_high_score = player_obj._sm_high_score
        return random.choice(
            stats.data_speech.MT_SM_HIGH_SCORE).format(sm_high_score)


    ##########
    # Speed Challenge
    ##########
    @staticmethod
    @log_func_name
    def get_ms_sc_stats(player_obj: object, sc_difficulty: str, mode: str) -> list:
        """Returns list of messages for user's speed challenge statistics."""
        ms_intro = ModeSpeech.get_ms_mode_intro( mode)
        ms_difficulty = stats.data_speech.MS_SC_DIFFICULTY.format(sc_difficulty)
        ms_average_score = ModeSpeech.get_ms_sc_average_score(player_obj, sc_difficulty)
        ms_high_score = ModeSpeech.get_ms_sc_high_score(player_obj, sc_difficulty)

        ms_catch = ModeSpeech.catch_no_records(ms_average_score, ms_high_score)
        if ms_catch:
            return ms_catch

        speech_list = [ms_intro, ms_difficulty, ms_average_score, 0.5, ms_high_score]
        return speech_list


    @staticmethod
    @log_func_name
    def get_ms_sc_what_difficulty() -> list:
        """Returns list of messages asking user to specify difficulty."""
        ms_what_diff = ModeSpeech.get_ms_sc_indicate_difficulty()
        ms_try_saying = get_ms_try_saying()
        ms_example = ModeSpeech.get_ms_sc_example_request_sc_diff_stats()

        speech_list = [ms_what_diff, 1, ms_try_saying, ms_example]
        return speech_list


    @staticmethod
    @log_func_name
    def get_ms_sc_average_score(player_obj, sc_difficulty: str) -> str:
        """Returns message of user's average score speed challenge difficulty."""
        try:
            sc_average_results = player_obj.get_sc_average_records(sc_difficulty)
            sc_avg = int(mean(sc_average_results))
            sc_avg_mm_ss_format = SC_EndGame.format_score_as_minutes_seconds(sc_avg)

        except Exception as e:
            logger.warning(f"get_ms_sc_average_score:   {e}")
            return None

        return random.choice(
            stats.data_speech.MT_SC_AVG_TIME).format(sc_avg_mm_ss_format)


    @staticmethod
    @log_func_name
    def get_ms_sc_high_score(player_obj: object, sc_difficulty: str) -> str:
        """Returns message of user's highscore on speed challenge difficulty."""
        try:
            sc_high_score = player_obj.get_sc_high_score(sc_difficulty)
            sc_high_score_mm_ss_format = SC_EndGame.format_score_as_minutes_seconds(sc_high_score)

        except Exception as e:
            logger.warning(f"get_ms_sc_average_score:   {e}")
            return None

        return random.choice(
            stats.data_speech.MT_SC_HIGH_SCORE).format(sc_high_score_mm_ss_format)


    @staticmethod
    @log_func_name
    def get_ms_sc_indicate_difficulty() -> str:
        """Returns message that can tell stats for a difficulty."""
        return stats.data_speech.MS_WHAT_SC_DIF


    @staticmethod
    @log_func_name
    def get_ms_sc_example_request_sc_diff_stats() -> str:
        """Returns example message to request difficult stats."""
        ex_sc_diff = random.choice( speed_challenge.data.SC_DIFFICULTIES)
        return stats.data_speech.MS_SC_DIF_EXAMPLE.format( ex_sc_diff)


    ##########
    # Can tell records
    ##########
    @staticmethod
    @log_func_name
    def get_ms_can_tell_record() -> str:
        """Returns message that can tell user statistics."""
        return get_ms_from_tuple(
            stats.data_speech.MMT_CAN_TELL_STATS)


    @staticmethod
    @log_func_name
    def get_example_hear_records() -> str:
        """Returns example message to hear mode records.""" 
        speech_list = [
            get_ms_try_saying(),
            ]

        for item in stats.data_speech.MMT_EXAMPLE_RECORDS:
            speech_list.append(item)
        
        return get_ms_from_tuple(speech_list)
    

    ##########
    # No records
    ##########
    @staticmethod
    @log_func_name
    def catch_no_records(ms_average: str, ms_high_score: str) -> str:
        """Catch method incase no records exist for the mode.

        NOTE: Lazy implementation. needs improvement."""

        if (ms_average is None) or (ms_high_score is None):
            logger.warning("catch_no_records")
            return ("You haven't played yet.", )
        
        return False


