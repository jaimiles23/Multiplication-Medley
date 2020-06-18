"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-20 23:11:16
 * @modify date 2020-05-22 23:33:29
 * @desc [
    SC_Welcome Utils. Methods to provide various welcome messages for the activity.
 ]
 */
"""

##########
# Imports
##########

from statistics import mean
import random


from logs import log_func_name, logger, log_all
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from players.players_dict import PlayerDict
from speed_challenge.end_utils import SC_EndGame

import speed_challenge.data
from aux_data.SSML_tags import (
    MW_EXCITED_LOW,
)


##########
# SurvivalSpeechUtils
##########

class SC_WelcomeUtils(object):

    @staticmethod
    @log_func_name
    def get_ms_welcome(player_obj: object) -> str:
        """Returns appropriate welcome message for speed challenge."""
        sc_plays = player_obj.sc_plays
        random_num = random.random()

        if sc_plays == 0:
            ms_welcome = SC_WelcomeUtils.get_ms_first_welcome()
        
        elif sc_plays == 1:
            ms_welcome = SC_WelcomeUtils.get_ms_long_welcome()
        
        elif (sc_plays > 5) and (random_num < 0.25):
            ms_welcome = SC_WelcomeUtils.get_ms_high_score_welcome( player_obj)
        
        elif (sc_plays > 5) and (random_num < 0.5):
            ms_welcome = SC_WelcomeUtils.get_ms_average_score_welcome( player_obj)
        
        elif random_num < 0.8:
            ms_welcome = SC_WelcomeUtils.get_ms_short_welcome()
        
        else:
            ms_welcome = SC_WelcomeUtils.get_ms_long_welcome()
        
        return MW_EXCITED_LOW.format(ms_welcome)


    @staticmethod
    @log_func_name
    def get_ms_first_welcome() -> str:
        """Returns welcome message for the first Speed Challenge play."""
        return get_ms_from_tuple(
            speed_challenge.data.MMT_SC_FIRST_WELCOME)
    

    @staticmethod
    @log_func_name
    def get_ms_long_welcome() -> str:
        """Returns long form of welcome message for Speed Challenge."""
        return get_ms_from_tuple(
            speed_challenge.data.MTT_LONG_WELCOME) + '?'
    
    
    @staticmethod
    @log_func_name
    def get_ms_high_score_welcome(player_obj: object) -> str:
        """Returns welcome message that includes user's highscore."""
        mode_hs = None
        for difficulty in speed_challenge.data.SC_DIFFICULTIES:
            mode_hs = player_obj.get_sc_high_score(difficulty)
            if mode_hs is not None: 
                break
        if (difficulty is None) or (mode_hs is None):
            log_all(difficulty, mode_hs, log_level= 40)
            logger.error("get_ms_high_score_welcome: Found no difficulty or hs.")
            return SC_WelcomeUtils.get_ms_short_welcome()
        
        mode_hs = SC_EndGame.format_score_as_minutes_seconds(mode_hs)

        ms_high_score = random.choice(
            speed_challenge.data.MT_HIGH_SCORE).format(
                difficulty, mode_hs)
        ms_beat_it = random.choice(
            speed_challenge.data.MT_BEAT_IT)
        
        speech_list = (ms_high_score, 1, ms_beat_it)
        return get_ms_from_tuple(speech_list)
    

    @staticmethod
    @log_func_name
    def get_ms_average_score_welcome(player_obj: object) -> str:
        """Returns welcome message telling the player's average time."""

        average_records = None
        for difficulty in speed_challenge.data.SC_DIFFICULTIES:
            average_records = player_obj.get_sc_average_records(difficulty)
            if average_records is not None: 
                break

        if (difficulty is None) or (average_records is None):
            log_all(difficulty, average_records, log_level= 40)
            logger.error("get_ms_high_score_welcome: Found no difficulty or average_records.")
            return SC_WelcomeUtils.get_ms_short_welcome()

        avg_score = int(mean(average_records))
        avg_score = SC_EndGame.format_score_as_minutes_seconds(avg_score)

        ms_average_score = random.choice(
            speed_challenge.data.MT_AVERAGE_SCORE).format(
                difficulty, avg_score)
        ms_beat_it = random.choice(
            speed_challenge.data.MT_BEAT_IT)

        speech_list = (ms_average_score, 1, ms_beat_it)
        return get_ms_from_tuple(speech_list)
    
    
    @staticmethod
    @log_func_name
    def get_ms_short_welcome() -> str:
        """Returns short welcome message."""
        return get_ms_from_tuple(
            speed_challenge.data.MTT_SHORT_WELCOME)

    
    @staticmethod
    @log_func_name
    def get_ms_starting_time() -> str:
        """Returns message that timer started."""
        return MW_EXCITED_LOW.format(
            random.choice( speed_challenge.data.MT_START_TIMER))


