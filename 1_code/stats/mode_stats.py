"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-14 12:36:55
 * @modify date 2020-05-26 15:24:43
 * @desc [
    ModeStats class used to update mode stats to session stats.
 ]
 */
"""

##########
# Imports
##########

from logs import log_func_name, logger


##########
# Class Utility Methods
##########

class ModeStats(object):

    ##########
    # Update Mode stats
    ##########
    @staticmethod
    @log_func_name
    def update_mode_stats(handler_input, correct: bool) -> None:
        """Updates mode_stats depending on correct."""
        attr = handler_input.attributes_manager.session_attributes
        mode = attr['mode']
        mode_stats = attr.get('mode_stats', dict())

        if mode not in mode_stats.keys():
            mode_stats[mode] = [0, 0]
        
        mode_correct, mode_incorrect = mode_stats[mode]
        if correct:
            mode_correct = int(mode_correct) + 1
        else:
            mode_incorrect = int(mode_incorrect) + 1
        
        mode_stats[mode] = [mode_correct, mode_incorrect]
        attr['mode_stats'] = mode_stats
        return
    

    @staticmethod
    @log_func_name
    def get_mode_stats(handler_input, mode: str) -> tuple:
        """Returns a tuple (int, int) of the mode statistics."""
        attr = handler_input.attributes_manager.session_attributes
        mode_stats = attr.get('mode_stats', dict())

        if mode not in mode_stats.keys():
            logger.warning(f"get_mode_stats   {mode} not found in keys.")
            return (0, 0)

        mode_correct, mode_incorrect = mode_stats[mode]
        return (int(mode_correct), int(mode_incorrect))


    ##########
    # Mode Stats -> Sesh Stats
    ##########
    @staticmethod
    @log_func_name
    def translate_mode_stats_to_sesh(handler_input) -> None:
        """Translates mode statistics to overall session statistics.
        
        Index documentation for both data structures:
        index[0] = answers_correct, index[1] = answers_incorrect.
        """
        attr = handler_input.attributes_manager.session_attributes
        session_stats = attr.get('session_stats', [0, 0])
        mode_stats = attr.get('mode_stats', {})

        session_correct = int(session_stats[0])
        session_incorrect =  int(session_stats[1])

        for _, v in mode_stats.items():
            mode_correct, mode_incorrect = int(v[0]), int(v[1])
            session_correct += mode_correct
            session_incorrect += mode_incorrect
        
        attr['session_stats'] = [session_correct, session_incorrect]
        attr['mode_stats'] = {}
        return
    
