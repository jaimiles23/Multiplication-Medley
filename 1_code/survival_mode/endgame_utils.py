"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-19 13:09:36
 * @modify date 2020-05-20 22:21:52
 * @desc [
    SMEndGame utility class for ending survival mode.
    - game score
    - score results
    - 
 ]
 */
"""

##########
# Imports
##########

import random


from ask_sdk_core.handler_input import HandlerInput


from logs import log_func_name, logger
from stats.mode_stats import ModeStats
from players.players_dict import PlayerDict
from survival_mode.survival_attr import SM_Attr
from answer_response.congrat_utils import CongratUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple

import survival_mode.data
from aux_data.SSML_tags import (
    MW_EXCITED_LOW,
    MW_EXCITED_MED)


##########
# Utility Class
##########

class SMEndGame(object):

    @staticmethod
    @log_func_name
    def get_ms_game_score(handler_input) -> str:
        """Returns a message with the user's Survival Mode score."""
        attr = handler_input.attributes_manager.session_attributes
        mode = attr.get('mode', None)
        
        correct, _ = ModeStats.get_mode_stats(handler_input, mode= mode)
        
        ms_problems_correct = random.choice(
            survival_mode.data.MT_PROBLEM_SCORE).format(correct)
        return MW_EXCITED_LOW.format( ms_problems_correct)


    ##########
    # Message of score relative to performance.
    ##########
    @staticmethod
    @log_func_name
    def get_ms_score_results(handler_input, player_obj: object = None) -> str:
        """Returns message about the user's relative SM score."""
        attr = handler_input.attributes_manager.session_attributes

        mode = attr.get('mode', None)
        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)
        sm_high_score = player_obj.get_sm_high_score()
        sm_score, _ = ModeStats.get_mode_stats(handler_input, mode= mode)

        if SM_Attr.check_sm_highscore(sm_high_score, sm_score):

            if SM_Attr.check_first_highscore(sm_high_score, sm_score):
                return SMEndGame.get_ms_first_highscore(sm_score)
            
            return SMEndGame.get_ms_new_highscore(sm_score, sm_high_score)

        elif SM_Attr.check_sm_tie_highscore(sm_high_score, sm_score):
            return SMEndGame.get_ms_tied_highscore(sm_high_score)

        else:
            return SMEndGame.get_ms_relative_attempt_success(
                handler_input, sm_score, player_obj= player_obj)


    @staticmethod
    @log_func_name
    def get_ms_first_highscore(sm_score: int) -> str:
        """Returns message for first SM highscore."""
        ms_first_hs = survival_mode.data.MS_FIRST_HS.format( sm_score)
        return MW_EXCITED_LOW.format(ms_first_hs)


    @staticmethod
    @log_func_name
    def get_ms_new_highscore(sm_score: int, sm_high_score: int) -> str:
        """Returns message that new highscore for survival mode."""
        speech_list = list(survival_mode.data.MTT_BEAT_OLD_HS)

        speech_list.append( str(sm_high_score))
        speech_list.append( random.choice(
            survival_mode.data.MT_QUESTION_SYN))
        
        ms_new_sm_high_score = get_ms_from_tuple(speech_list)

        return MW_EXCITED_MED.format(ms_new_sm_high_score)


    @staticmethod
    @log_func_name
    def get_ms_tied_highscore(sm_high_score: int) -> str:
        """Returns message that user tied SM highscore."""
        ms_tied_hs = ( random.choice( 
            survival_mode.data.MT_TIE_HS)
                .format( sm_high_score))
        return MW_EXCITED_LOW.format( ms_tied_hs)


    @staticmethod
    @log_func_name
    def get_ms_relative_attempt_success(
        handler_input, sm_score: int, player_obj: object = None) -> str:
        """Returns message about the relative success (z-score) of the sm_score."""
        sm_z_score = SM_Attr.get_sm_z_score(handler_input, sm_score, player_obj)

        ## Tuple(float, tuple, str):
        # conditional z_score, message list, & message wrappers
        z_score_response_lists = (
            ( -1,   survival_mode.data.MT_BETTER_NEXT_TIME, "{}"),
            ( 0.25, survival_mode.data.MT_NORM_ATTEMPT,     "{}"),
            ( 1,    survival_mode.data.MT_GOOD_ATTEMPT,     MW_EXCITED_LOW),
            ( 99,   survival_mode.data.MT_AWESOME_ATTEMPT,  MW_EXCITED_MED),
        )

        for z_score, mt, mw in z_score_response_lists:
            if sm_z_score < z_score:
                message_tuple, ms_wrap = mt, mw
                break
        
        ms_relative_score = random.choice(message_tuple)    
        return ms_wrap.format( ms_relative_score)

