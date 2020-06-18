"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 16:35:10
 * @modify date 2020-05-04 16:35:10
 * @desc [
     Data module for skill card titles.
 ]
 */
"""

##########
# Imports
##########

import aux_data.skill_data


##########
# Card Title
##########

TITLE_SKILL_NAME = aux_data.skill_data.SKILL_NAME

TITLE_FREE_PLAY = "Free Play"
TITLE_CUSTOM = "Custom Practice"
TITLE_SPEED =  "Speed Challenge"
TITLE_SURVIVAL = "Survival Mode"

CARD_TITLE_DICT = {
    'free_play' :   TITLE_FREE_PLAY,
    'custom'    :   TITLE_CUSTOM,
    'speed'     :   TITLE_SPEED,
    'survival'  :   TITLE_SURVIVAL,
}



