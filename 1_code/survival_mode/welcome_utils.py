"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 09:56:46
 * @modify date 2020-06-16 23:45:16
 * @desc [
    SM_WelcomeUtils with methods to get appropriate welcome message.
 ]
 */
"""

##########
# Imports
##########

from statistics import mean
import random


from logs import log_func_name, logger
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from players.players_dict import PlayerDict


import survival_mode.data
from aux_data.SSML_tags import (
    MW_EXCITED_LOW,
)
## TODO: Add MW_Excited to either individual or all welcomes. not sure yet.


##########
# SurvivalSpeechUtils
##########

class SM_WelcomeUtils(object):

    @staticmethod
    @log_func_name
    def get_ms_welcome(handler_input) -> str:
        """Returns appropriate welcome message for survival mode."""
        player = PlayerDict.load_player_obj(handler_input)
        sm_plays = player.sm_plays
        random_num = random.random()

        if sm_plays == 0:
            ms_welcome = SM_WelcomeUtils.get_ms_first_welcome()

        elif sm_plays == 1:
            ms_welcome = SM_WelcomeUtils.get_ms_long_welcome()
        
        elif (sm_plays > 5) and (random_num < 0.25):
            ms_welcome = SM_WelcomeUtils.get_ms_high_score_welcome(player)

        elif (sm_plays > 5) and (random_num < 0.5):
            ms_welcome = SM_WelcomeUtils.get_ms_average_score_welcome(player)

        elif random_num < 0.8:
            ms_welcome = SM_WelcomeUtils.get_ms_short_welcome()

        else:
            ms_welcome = SM_WelcomeUtils.get_ms_long_welcome()
        
        return MW_EXCITED_LOW.format(ms_welcome)


    @staticmethod
    @log_func_name
    def get_ms_first_welcome() -> str:
        """Returns welcome message for the first welcome."""
        return (get_ms_from_tuple(
            survival_mode.data.MMT_FIRST_WELCOME))


    @staticmethod
    @log_func_name
    def get_ms_long_welcome() -> str:
        """Returns long-form of re-appearing welcome message."""
        return get_ms_from_tuple(
            survival_mode.data.MMT_LONG_WELCOME,
            str_joiner= '')


    @staticmethod
    @log_func_name
    def get_ms_high_score_welcome(player: object) -> str:
        """Returns welcome message with the player's highscore on survival mode."""
        high_score = player.get_sm_high_score()
        ms_high_score = random.choice( 
            survival_mode.data.MT_HIGH_SCORE).format( high_score)
        
        speech_list = (
            SM_WelcomeUtils.get_ms_short_welcome(), 
            ms_high_score,
            SM_WelcomeUtils.get_ms_beat_record_ending(),
        )
        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_average_score_welcome(player: object) -> str:
        """Returns welcome message with the player's average score on survival mode."""
        average_questions = mean(player.get_sm_avg_records())
        ms_average_score = random.choice(
            survival_mode.data.MT_AVERAGE_SCORE).format( average_questions)

        speech_list = (
            SM_WelcomeUtils.get_ms_short_welcome(), 
            ms_average_score,
            SM_WelcomeUtils.get_ms_beat_record_ending(),
        )

        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_short_welcome() -> str:
        """Returns short welcome message for survival mode."""
        return get_ms_from_tuple( 
            survival_mode.data.MMT_SHORT_WELCOME,
            str_joiner='')


    ##########
    # Auxiliary methods
    ##########
    @staticmethod
    @log_func_name
    def get_ms_beat_record_ending() -> str:
        """Returns the ending to beat the old record."""
        speech_list = (
            " ",
            survival_mode.data.MT_QUESTION_SYN,
            ". ",
            survival_mode.data.MT_BEAT_IT
            )
        return get_ms_from_tuple( speech_list, str_joiner='')

