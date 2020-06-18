"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 11:48:39
 * @modify date 2020-06-16 14:26:21
 * @desc [
    Data module for CongratUtils:
        - Congrat wrapper dict for SSML wrappers for excitement level
        - Buzzer
        - Standard Congrats
        - Speechcon
        - Broke incorrect streak
        - Correct streaks
 ]
 */
"""

##########
# Imports
##########

from aux_data.SSML_tags import (
    MW_EXCITED_LOW, MW_EXCITED_MED, MW_EXCITED_HIGH
    )


##########
# Excited Wrapper
##########

CONGRAT_WRAPPER_DICT = {
    0   :   "{}",
    1   :   MW_EXCITED_LOW,
    2   :   MW_EXCITED_MED,
    3   :   MW_EXCITED_HIGH,
}


##########
# Buzzer
##########

CORRECT_BUZZ = """<audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_positive_response_01"/>"""

##########
# Standard Congrats
##########

MT_CONGRATS = (
    "Absolutely",
    "Ace",
    "Affirmative",
    "All right",
    "Awesome",
    "Cool",
    "Excellent",
    "Fantastic", 
    "Good",
    "Great",
    "Nice",
    "Right on",
    "Super",
    "Swell",
    "Terrific",
    "Yeah",
)


##########
# Speechcon
##########

MT_SPEECHCON_CONGRATS = (
    "absolutely",
    "agreed",
    "attagirl",
    "ay",
    "bada bing bada boom",
    "bam",
    "bing",
    "bingo",
    "booya",
    "bravo",
    "cha ching",
    "ding",
    "ding ding ding",
    "dynomite",
    "excellent",
    "good",
    "great",
    "high five",
    "hip hip hooray",
    "hurray",
    "inconceivable",
    "legendary",
    "mamma mia",
    "my goodness",
    "indeed",
    "righto",
    "roger",
    "splendid",
    "stunning",
    "swish",
    "yeah",
    "you bet",
    "yay",
    "yahoo",
    "wow",    
)


##########
# Incorrect Streak
##########

MT_BROKE_INCORRECT_STREAK_1 = (
    "That's right!",
    "That's correct!",
)


##########
# Correct Streak
##########

MT_CORRECT_STREAK_1 = (
    "That's {} in a row!",
    "{} in a row! You're on a roll!",
)

MT_CORRECT_STREAK_2 = (
    "Whoa. {} in a row. Keep going!",
    "{} in a row! How far can you go!",
)
