"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 17:38:39
 * @modify date 2020-05-22 23:10:33
 * @desc [
    PlayerEncoder utility class to save & load player as json object.
    - Encode player
    - Decode player

]
*/"""

##########
# Imports
##########

from logs import logger, log_func_name, log_all
from players.player_class import Player


##########
# Encoder Utility class
##########

class PlayerEncoder(object):
    """Utility class to save & load the player instance from json."""

    @staticmethod
    @log_func_name
    def encode_player_to_dict(player_instance: object) -> dict:
        """Encodes the player class as a dictionary."""

        if not isinstance(player_instance, Player):
            logger.error("encode_player_to_dict:    Passed non-player object")
        
        name = player_instance.name
        total_correct = player_instance._total_correct
        total_incorrect = player_instance._total_incorrect
        answered_tables = player_instance._answered_tables
        times_tables_info = player_instance._times_tables_info

        fp_plays = player_instance.fp_plays
        cp_plays = player_instance.cp_plays

        sm_plays = player_instance.sm_plays
        sm_high_score = player_instance._sm_high_score
        sm_average_records = player_instance._sm_average_records

        sc_plays = player_instance.sc_plays
        sc_high_score_dict = player_instance._sc_high_score_dict
        sc_average_record_dict = player_instance._sc_average_record_dict

        # log_all(sc_plays, sc_high_score_dict, sc_average_record_dict, log_level= 10)
        player_dict = {
            'player'                    :   True,
            'name'                      :   name,
            'total_correct'             :   total_correct,
            'total_incorrect'           :   total_incorrect,
            'answered_tables'           :   answered_tables,
            'times_tables_info'         :   times_tables_info,

            'fp_plays'                  :   fp_plays,
            'cp_plays'                  :   cp_plays,

            'sm_plays'                  :   sm_plays,
            'sm_high_score'             :   sm_high_score,
            'sm_average_records'        :   sm_average_records,

            'sc_plays'                  :   sc_plays,
            'sc_high_score_dict'        :   sc_high_score_dict,
            'sc_average_record_dict'    :   sc_average_record_dict,
        }
        return player_dict


    @staticmethod
    @log_func_name
    def decode_dict_to_player(player_dict: dict) -> object:
        """Returns player object with player_dict values."""

        if not isinstance(player_dict, dict):
            logger.error("decode_dict_to_player:    Passed non-dict object")
        elif 'player' not in player_dict.keys():
            logger.error("decode_dict_to_player:    Non-player object")
        
        p_name = player_dict.get('name', None)
        p_total_correct = player_dict.get('total_correct', 0)
        p_total_incorrect = player_dict.get('total_incorrect', 0)
        p_answered_tables = player_dict.get('answered_tables', [])
        p_times_tables_info = player_dict.get('times_tables_info', {})

        p_fp_plays =  player_dict.get('fp_plays', 0)
        p_cp_plays =  player_dict.get('cp_plays', 0)

        p_sm_plays =  player_dict.get('sm_plays', 0)
        p_sm_high_score = player_dict.get('sm_high_score', 0)
        p_sm_average_records = player_dict.get('sm_average_records', [])

        p_sc_plays = player_dict.get('sc_plays', 0)
        p_sc_high_score_dict = player_dict.get('sc_high_score_dict', {})
        p_sc_average_record_dict = player_dict.get('sc_average_record_dict', {})
        
        return Player(
            name= p_name,
            total_correct= p_total_correct,
            total_incorrect= p_total_incorrect,
            answered_tables= p_answered_tables,
            times_tables_info= p_times_tables_info,
            
            fp_plays= p_fp_plays,
            cp_plays= p_cp_plays,

            sm_plays= p_sm_plays,
            sm_high_score= p_sm_high_score,
            sm_average_records= p_sm_average_records,
            
            sc_plays= p_sc_plays,
            sc_high_score_dict= p_sc_high_score_dict,
            sc_average_record_dict= p_sc_average_record_dict,
        )

