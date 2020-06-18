"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-24 13:53:20
 * @modify date 2020-06-16 14:27:57
 * @desc [
    Utility class to manage session attributes.
 ]
 */
"""

##########
# Imports
##########

from datetime import date

from logs import logger, log_func_name, log_all
from aux_utils.time_encoder import TimeEncoder


##########
# Session attr util class.
##########

class SessionAttrMnger(object):

    @staticmethod
    @log_func_name
    def load_session_attr(handler_input) -> None:
        """Loads all necessary session attributes."""
        sesh_attr = handler_input.attributes_manager.session_attributes
        
        ## Today
        current_date = date.today()
        current_date_str = TimeEncoder.convert_date_to_str( current_date)
        sesh_attr['today'] = current_date_str

        return
    

    @staticmethod
    @log_func_name
    def set_pointer_attr(handler_input) -> None:
        """Sets next_pointer when not current player."""
        attr = handler_input.attributes_manager.session_attributes
        if attr['current_player'] == None:
            attr['next_handler'] = 'create_profile'
        
        return

