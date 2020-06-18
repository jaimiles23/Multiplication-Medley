"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-07 11:12:39
 * @modify date 2020-05-07 20:30:31
 * @desc [
    Data module for the act description. Includes descriptions for:
        - General acts
        - Free Play
        - Custom Practice
        - Speed Challenge
        - Survival Mode
        - Dictionay to access each description
        - Prompt to play activity
 ]
 */
"""

##########
# Imports
##########

from aux_data.SSML_tags import MW_EXCITED_LOW


##########
# General Descript
##########

MS_GEN_PRACT_1 = "I have 2 practice activities:"
MS_GEN_PRACT_2 = "Free Play and Custom Practice,"
MS_GEN_COMP_1 = "and 2 competitive activities:"
MS_GEN_COMP_2 = "Speed Challenge and Survival Mode."

MS_START_OR_ASK = "I can start an activity, or you can ask me about one to learn more."

MMT_GEN_DESCRIPT = (
    MS_GEN_PRACT_1, 
    1, 
    MS_GEN_PRACT_2,  
    1,
    MS_GEN_COMP_1,  
    1, 
    MS_GEN_COMP_2,   
    2,
    MS_START_OR_ASK,
)


##########
# Free Play
##########
MS_FP_INTRO = "In Free Play, you get to pick what you want to practice."
MS_FP_TABLES = """You can choose the times tables, """
MS_FP_QUESTIONS = """and how many questions I'll ask."""
# MS_BOUNDS = """and the lower and upper range of the tables."""
# MS_FP_UTTERANCE = "To start, you can say: Start Freeplay, and ask me 10 questions from the 4's times table."

#Master Message Tuple
MMT_FREE_PLAY = (
    MS_FP_INTRO,
    1,
    MS_FP_TABLES,
    MS_FP_QUESTIONS,
    # 2,
    # MS_FP_UTTERANCE,
)


##########
# Custom Practice
##########
MS_CP_INTRO = "In Custom Practice, I ask questions based on your user profile."

MS_CP_FORMAT_1 = "First, I ask questions that you recently messed up."
MS_CP_FORMAT_2 = "Next, I check if you make mistakes more often on a certain times tables."
MS_CP_FORMAT_3 = "If you're not making many mistakes, I'll ask tougher questions than you're used to."

MMT_CUSTOM_PRACTICE = (
    MS_CP_INTRO,
    1,
    MS_CP_FORMAT_1,
    1,
    MS_CP_FORMAT_2,
    1,
    MS_CP_FORMAT_3,
)


##########
# Speed Challenge
##########

MS_SC_INTRO = """In Speed Challenge, I time how fast you can answer all questions in a range of times tables."""
## May like to change to a ~ 30 questions from a range of Times Tables.

MS_SC_LEVELS = "There are 4 levels:"
MS_SC_NORMAL = "In Normal mode, I ask questions from the times tables 0 to 10."
MS_SC_HARD = "In Hard mode, I ask questions from 0 to 12."
MS_SC_ADVANCED = "Advanced mode, I ask from 10 to 20, and "
MS_SC_INSANE = "in Insane mode, from 20 to 30."

MMT_SPEED_CHALLENGE = (
    MS_SC_INTRO,
    2,
    MS_SC_LEVELS,
    1,
    MS_SC_NORMAL,
    1,
    MS_SC_HARD,
    1,
    MS_SC_ADVANCED,
    MS_SC_INSANE,
)


##########
# Survival Mode
##########

MS_SM_INTRO = "In Survival Mode, I test how many multiplication questions you can answer in a row."
MS_SM_SCAFFOLD = "But watch out! I start with easy questions and get harder until you mess up!"

MMT_SURVIVAL_MODE = (
    MS_SM_INTRO,
    1,
    MW_EXCITED_LOW.format(MS_SM_SCAFFOLD)
)


##########
# Description Dictionary
##########

DESCRIPT_DICT = {
    'free_play' :   MMT_FREE_PLAY,
    'custom'    :   MMT_CUSTOM_PRACTICE,
    'speed'     :   MMT_SPEED_CHALLENGE,
    'survival'  :   MMT_SURVIVAL_MODE
}


##########
# Prompt to play activity
##########

MT_WANT = (
    "Do you wanna",
    "Do you want to",
    "Want to",
    "Wanna",
)
MT_PLAY = (
    "try",
    "play",
    "start",
)

MMT_WANT_TO_PLAY = (
    MT_WANT,
    MT_PLAY,
)

