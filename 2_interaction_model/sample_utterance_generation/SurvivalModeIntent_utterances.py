"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 09:29:06
 * @modify date 2020-05-06 09:29:06
 * @desc [
    Generates sample utterances for Survival mode.
NOTE: Example:

Start Survival  Mode

V     Subject   OPTIONAL
]
*/
"""

##########
# Data
##########

OPTIONAL_VERBS = (
    "start",
    "begin",
    "open",
    "launch",
    "initiate",
    "set up",
)

ACT_NAME = "survival"

OPTIONAL_MODE = "Mode"


##########
# Sample utterances
##########
speech_list = []

for verb in OPTIONAL_VERBS:
    speech_list.append(verb)
    speech_list.append(ACT_NAME)
    
    print(' '.join(speech_list))
    speech_list.append( OPTIONAL_MODE)
    print(' '.join(speech_list))
    speech_list = []



