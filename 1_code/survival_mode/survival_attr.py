"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 09:56:46
 * @modify date 2020-05-26 16:27:22
 * @desc [
    SM_Attr utility class for survival mode to:
    - set starting attributes
    - increment attributes
    - reset attrs
    - check player survival mode stats
    - get survival mode score z-score.
 ]
 */
"""

##########
# Imports
##########

from math import sqrt
from statistics import mean, stdev

from logs import log_func_name, logger
from slots.slot_utils import SlotUtils
from players.players_dict import PlayerDict
from aux_utils.z_score import calc_z_score


##########
# Survival Mode Attributes
##########

class SM_Attr(object):

    ##########
    # Start Attrs
    ##########
    @staticmethod
    @log_func_name
    def set_attr_start_survival_mode(handler_input) -> None:
        """Sets attributes for starting survival mode."""
        attr = handler_input.attributes_manager.session_attributes
        attr['mode'] = 'survival'
        attr['help_pointer'] = 'survival_mode'

        attr['questions_answered'] = 0
        attr['question'] = (0, 0)
        attr['consecutive_correct'] = 0

        attr['sm_upper'] = 6        # arbitrary.    

        attr['flag_double_digits']  = True
        attr['flag_upper_hit_avg']  = True
        attr['flag_cntr_hit_avg']   = True
        return None
    

    ##########
    # Increment
    ##########
    @staticmethod
    @log_func_name
    def increment_sm_upper(handler_input) -> None:
        """Increments sm_upper for survival mode."""
        attr = handler_input.attributes_manager.session_attributes
        questions_answered = attr['questions_answered']
        sm_upper = attr.get('sm_upper')

        if not (questions_answered % int( sqrt(sm_upper) * 1.5)):     # increment slower as higher.
            sm_upper += 1
        
        attr['sm_upper'] = sm_upper
        return
    

    @staticmethod
    @log_func_name
    def log_stats(handler_input) -> None:
        """logs the user's survival mode stats."""
        attr = handler_input.attributes_manager.session_attributes
        questions_answered =  attr['questions_answered'] 
        question = attr['question']
        
        logger.info(f"SM Score: {questions_answered}")
        logger.info(f"SM_last_question: {question}")
        return
    

    ##########
    # End Attrs
    ##########
    @staticmethod
    @log_func_name
    def set_attr_end_survival_mode(handler_input) -> None:
        """Sets attributes when survival mode is finished."""
        attr = handler_input.attributes_manager.session_attributes
        reset_attrs = (
            'mode',
            'help_pointer',

            'question',
            'questions_answered',
            
            'consecutive_correct',
            'consecutive_incorrect',

            'flag_double_digits',
            'flag_upper_hit_avg',
            'flag_cntr_hit_avg',
        )
        for reset_at in reset_attrs:
            attr[reset_at] = 0
        
        return None


    ##########
    # Player Survival Mode stats
    ##########

    @staticmethod
    @log_func_name
    def check_sm_highscore(sm_high_score: int, sm_score: int) -> bool:
        """Returns boolean indicating if new Survival mode high score."""
        return int(sm_score) > int(sm_high_score)


    @staticmethod
    @log_func_name
    def check_sm_tie_highscore(sm_high_score: int, sm_score: int) -> bool:
        """Returns boolean indicating if tied Survival Mode high score."""
        return int(sm_high_score) == int(sm_score) and (sm_high_score != 0)
    

    @staticmethod
    @log_func_name
    def check_first_highscore(sm_high_score: int, sm_score: int) -> bool:
        """Returns boolean indicating if first highscore."""
        return (sm_high_score == 0)
        

    @staticmethod
    @log_func_name
    def get_sm_z_score(handler_input, sm_score: int, player_obj: object = None) -> bool:
        """Returns z_score for the Survival mode score."""
        if not player_obj:
            player_obj = PlayerDict.load_player_obj(handler_input)
        
        sm_average_records = [int(num) for num in player_obj._sm_average_records]
        
        z_score = calc_z_score(
            data_point= sm_score,
            data = sm_average_records
        )
        return z_score

