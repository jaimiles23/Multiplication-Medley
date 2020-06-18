"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-22 14:10:44
 * @modify date 2020-05-22 14:15:53
 * @desc [
    Auxiliary method to tell the player thank you for playing.

    Called at the end of activities & when exiting the skill.
 ]
 */
"""
##########
# Imports
##########

import aux_data.skill_data
from aux_data.SSML_tags import MW_EXCITED_LOW


##########
# Get Thanks message func
##########

def get_ms_thanks(handler_input, mode: bool = False, excite: bool = True) -> str:
    """Returns message "Thank you for playing!"""
    mode_name = handler_input.attributes_manager.session_attributes.get('mode', None)
    mode_name = aux_data.skill_data.MODE_ACT_DICT.get(mode_name, None)

    if (not mode) or (not mode_name):
        ms_thanks = MS_THANKS
    else:
        
        ms_thanks = MS_MODE_THANKS.format(mode_name)
    
    if excite:
        ms_thanks = MW_EXCITED_LOW.format(ms_thanks)
    return ms_thanks


##########
# Data
##########
MS_THANKS = "Thanks for playing!"

MS_MODE_THANKS = "Thanks for playing {}!"