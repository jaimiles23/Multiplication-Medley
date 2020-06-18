"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 23:27:59
 * @modify date 2020-06-16 23:19:52
 * @desc [
    PlayerDict utility class. Contains methods to:
    - Create new player
    - Loading player
    - save player.
]
*/
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput

from players.player_class import Player
from players.player_encoder import PlayerEncoder
from logs import logger, log_func_name


##########
# PlayerDict Utility Class
##########

class PlayerDict(object):
    """Methods for accessing player class through session attributes."""

    ##########
    # Create New Player
    ##########
    @staticmethod
    @log_func_name
    def create_new_player(handler_input, player_name: str) -> None:
        """Creates new player and adds it to the players_dict"""
        attr = handler_input.attributes_manager.session_attributes
        players_dict = attr.get('players_dict', {})

        if player_name in players_dict.keys():
            logger.warning("create_new_player: Player already found.")
            return
        
        new_player = Player(player_name)
        new_player_dict = PlayerEncoder.encode_player_to_dict(new_player)
        players_dict[player_name] = new_player_dict

        attr['players_dict'] = players_dict   
        return


    ##########
    # Load/Save Player obj
    ##########
    @staticmethod
    @log_func_name
    def load_player_obj(handler_input) -> object:
        """Loads player object from players_dict"""
        attr = handler_input.attributes_manager.session_attributes
        players_dict = attr.get('players_dict', {})
        current_player = attr.get('current_player', None)

        if not current_player:
            logger.warning("load_player_obj: No player object")
            return Player(name="")
        elif current_player not in players_dict.keys():
            logger.warning("load_player_obj: Player not found.")
            return Player(name="")
        
        player_dict_format = players_dict[current_player]
        player_obj = PlayerEncoder.decode_dict_to_player(player_dict_format)
        return player_obj


    @staticmethod
    @log_func_name
    def save_player_obj(handler_input, player_obj: object):
        """Saves player_object in players_dict"""
        attr = handler_input.attributes_manager.session_attributes
        players_dict = attr.get('players_dict', {})
        player_name = player_obj.name

        if player_name == "":
            logger.warning("save_player_obj:    Discarded empty player obj.")
            return
        
        player_dict_format = PlayerEncoder.encode_player_to_dict( player_obj)
        players_dict[ player_name] = player_dict_format
        
        attr['players_dict'] = players_dict
        return

