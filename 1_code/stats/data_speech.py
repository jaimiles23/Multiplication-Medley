"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-20 15:15:17
 * @modify date 2020-05-23 00:22:35
 * @desc [
    Data module for the mode statistics speech lib. Data for:
    - Intro
    - Survival Mode
    - Speed Challenge
    - Can tell stats
    - Examples
 ]
 */
"""


##########
# Intro
##########

MT_MODE_INTRO = (
    "In {},",
)

##########
# Survival Mode
##########


MT_SM_AVG_SCORE = (
    "You usually answer {} questions,",
    "You typically answer around {} questions,",
)

MT_SM_HIGH_SCORE = (
    "and your best score is {}!",
    "and your personal record is {}!",
)



##########
# Speed Challenge
##########

MS_SC_DIFFICULTY = "on {} difficulty,"

MT_SC_AVG_TIME = (
    "you usually take around {}.",
    "you typically take around {}.",
)

MT_SC_HIGH_SCORE = (
    "Your best score is {}!",
    "Your personal record is {}!",
)

## Specify Difficulty
MS_WHAT_SC_DIF = "What Speed Challenge difficulty should I tell you about?"
MS_SC_DIF_EXAMPLE = "What's my record for Speed Challenge on {} difficulty?"


##########
# Can tell stats
##########

MT_CAN_TELL = (
    "I can tell you",
    "I know your",
)
MT_RECORD = (
    "record for",
    "personal record for",
)
MT_BOTH_MODES = (
    "Speed Challenge and Survival Mode.",
    "Survival Mode and Speed Challenge."
)

MMT_CAN_TELL_STATS = (
    MT_CAN_TELL,
    MT_RECORD,
    MT_BOTH_MODES,
)


##########
# Example
##########

MS_WHAT = "What's my"

MT_MODES = (
    "Speed Challenge on normal difficulty.",        # needs extra argument.
    "Survival Mode.",
)

MMT_EXAMPLE_RECORDS = (
    MS_WHAT,
    MT_RECORD, 
    MT_MODES
)

