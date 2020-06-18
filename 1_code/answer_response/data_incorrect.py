"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-15 15:46:26
 * @modify date 2020-06-16 14:25:20
 * @desc [
    Data module for when the user gets an answer incorrect.
 ]
 */
"""

##########
# Imports
##########

from aux_data.SSML_tags import MW_SPEECHCON


##########
# Buzzer
##########
INCORRECT_BUZZ = """<audio src="soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_negative_response_01"/>"""


##########
# Incorrect Answer
##########

MT_INCORRECT = (
   "That's not right!",
   "That's not it!",
   "Nope!",
   "No!",
   MW_SPEECHCON.format("Yikes!"),
   MW_SPEECHCON.format("Yikes!"),
)

