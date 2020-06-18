"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-14 11:51:47
 * @modify date 2020-05-14 12:43:48
 * @desc [
    SessionStats used for updating consecutive correct & incorrect.
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

class SessionStats(object):

    ##########
    # Consecutive Correct & Incorrect
    ##########
    @staticmethod
    @log_func_name
    def update_consecutive_correct(handler_input, correct: bool) -> None:
        """Tracks the number of consecutive correct & incorrect answers."""
        attr = handler_input.attributes_manager.session_attributes
        consecutive_correct = attr.get('consecutive_correct', 0)
        consecutive_incorrect = attr.get('consecutive_incorrect', 0)
        
        if correct:
            consecutive_correct += 1
            consecutive_incorrect = 0
        elif not correct:
            consecutive_incorrect += 1
            consecutive_correct = 0
        
        attr['consecutive_correct'] = consecutive_correct
        attr['consecutive_incorrect'] = consecutive_incorrect
        return


    
