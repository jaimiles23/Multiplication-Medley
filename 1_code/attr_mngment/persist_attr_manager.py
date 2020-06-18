"""
/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 16:10:38
 * @modify date 2020-06-16 14:27:47
 * @desc [
    Utility class for loading & saving persistent attributes.
]*/"""

##########
# Imports
##########

from logs import logger, log_func_name, log_all


##########
# Utility class
##########

class PersistAttrMnger(object):
    """Methods to save and load persistent attributes."""
    
    @staticmethod
    @log_func_name
    def load_persist_attr(handler_input):
        """Loads persistent attributes from s3 bucket."""
        persist_attr = handler_input.attributes_manager.persistent_attributes
        sesh_attr = handler_input.attributes_manager.session_attributes

        ## General
        sesh_attr['logins'] = persist_attr.get('logins', 0)

        ## Player
        sesh_attr['players_dict'] = persist_attr.get('players_dict', {})
        sesh_attr['current_player'] = persist_attr.get('current_player', None)

        ## Questions
        sesh_attr['wrong_quest_by_date'] = persist_attr.get('wrong_quest_by_date', {})

        return


    @staticmethod
    @log_func_name
    def save_persist_attr(handler_input):
        """Saves persistent attributes to s3 bucket."""
        persist_attr = handler_input.attributes_manager.persistent_attributes
        sesh_attr = handler_input.attributes_manager.session_attributes

        ## General
        persist_attr['logins'] = sesh_attr['logins']

        ## Player
        persist_attr['players_dict'] = sesh_attr['players_dict']
        persist_attr['current_player'] = sesh_attr['current_player']

        ## Questions
        persist_attr['wrong_quest_by_date'] = sesh_attr['wrong_quest_by_date']
        
        handler_input.attributes_manager.save_persistent_attributes()
        return

