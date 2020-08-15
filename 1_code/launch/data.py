"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 09:08:15
 * @modify date 2020-05-27 11:10:57
 * @desc [
    Data module for Launch Handler:
    - Welcome messages
    - Player name prompt
]
*/
"""

##########
# Imports
##########

from pause.pauser import Pauser
import aux_data.skill_data
from aux_data.SSML_tags import MW_EXCITED_LOW


##########
# Welcome Messages
##########
## NOTE: Excite wrapper should be moved to method?
MS_FIRST_WELCOME = MW_EXCITED_LOW.format(
    f"Welcome to {aux_data.skill_data.SKILL_NAME}! I have four different multiplication games to play.")

MT_WELCOME_BACK_PLAYER = (
    "Welcome back {}!",
    "Hi again {}!",
    "Good to see you again {}!",
)

MS_WELCOME_RATE_SKILL = "If you're enjoying the skill, take a minute to rate it in the app store. Thanks!"


##########
# Player Name prompt
##########

MTT_FIRST_PLAYER_NAME = (
    MW_EXCITED_LOW.format("First, let's make a player profile to track your progress."),
    2,
    "What's your name?",
)


MS_FIRST_PLAY_NAME_REPROMPT = """Tell me your name so I can make you a profile."""

