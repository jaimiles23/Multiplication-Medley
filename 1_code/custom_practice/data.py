"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-23 11:39:41
 * @modify date 2020-05-27 11:31:22
 * @desc [
    Data module for Custom Practice:
        - practice types
        - first welcome
        - Need more data message
        - short welcome
        - long welcome 
        - General practice messages
        - Incorrect problems message
        - High error tables message
        - high relative error message
        - new tables message
        - finished practice message
        - complete practice
 ]
 */
"""

##########
# Imports
##########



##########
# Practice Type dict Constants
##########

PRACT_TYPES = (
    'incorrect',
    'high_err_tbl',
    'high_z_score',
    'new_tables',
)

ALLOWED_MAX_DICT_AGE = 3
HIGH_ERR_THRESHOLD = 0.20       ## Allows 4/20 questions incorrect
HIGH_Z_SCORE_ERR =  2           ## NOTE: not norm dist.
MIN_DATA_REQUIRED = 100

QUESTIONS_PER_MODE = 10


##########
# First Welcome
##########

MODE_NAME = "Custom Practice"

MS_CP_WELCOME = f"Welcome to {MODE_NAME}!"
MS_CP_WELCOME_DESIGN = "In this mode, I design a practice session just for you."
MS_CP_WRONG = "First, I ask you questions that you missed recently."
MS_CP_FREQ_ERR = "Next, I test you on tables that you mess up a lot."
MS_CP_HIGHER_TBL = "Finally, I ask questions that are harder than you're used to."
MS_START_FIRST_PRACT = "Here's the first practice."

MMT_FIRST_WELCOME = (
    MS_CP_WELCOME,
    1,
    MS_CP_WELCOME_DESIGN,
    1.5,
    MS_CP_WRONG,
    1.75,
    MS_CP_FREQ_ERR,
    1.5,
    MS_CP_HIGHER_TBL,
    2.5,
    MS_START_FIRST_PRACT
)


##########
# Need More Data
##########

MS_MORE_DATA = "You need to answer more multiplication questions before I can make a custom practice for you."
MS_ANSWERED_Q_SO_FAR = "So far you've answered {} questions."
MS_COME_BACK_AFTER = f"Please come back when you've answered {MIN_DATA_REQUIRED} questions."


##########
# Short Welcome
##########

MT_WELCOME = (
    "Welcome to",
    "Welcome back to",
    "Let's start",
)

MMT_SHORT_WELCOME = (
    MT_WELCOME,
    MODE_NAME,
)


##########
# Long Welcome
##########

MT_START_PERSONAL_PRACTICE = (
    "Let's set up your personal practice.",
    "Let's start a practice just for you.",
    "Here's your personalized practice.",
)

MMT_LONG_WELCOME = (
    MT_WELCOME,
    MODE_NAME,
    2,
    MT_START_PERSONAL_PRACTICE,
)


##########
# Practice Message - General
##########

MT_GEN_PRACT_INTRO = (
    "I noticed that",
    "It looks like",
)

MT_WRONG_ANSWER = (
    "you missed",
    "you missed",
    "you misanswered",
)

MT_SOME = (
    "a few",
    "a couple of",
    "some",
    "some",
)

MT_TIMES_TABLE_SYN = (
    "tables",
    "times tables",
)
MT_QUESTION_SYN = (
    "questions",
    "problems",
)

MT_PRACTICE = (
    "Let's practice",
    "We'll practice",
    "I'll set up a practice for",
)
MT_THOSE_PROBLEMS = (
    "these questions.",
    "those problems.",
    "those.",
    "them.",
)

MMT_PRACTICE_THOSE = (
    MT_PRACTICE,
    MT_THOSE_PROBLEMS,
)


##########
# Practice Message - Incorrect problems
##########

MT_PAST_FEW_DAYS = (
    "recently.",
    "in the past few days.",
)

MMT_INCORRECT_PROBLEMS_IN_DATES = (
    MT_GEN_PRACT_INTRO,
    MT_WRONG_ANSWER,
    MT_SOME,
    MT_QUESTION_SYN,
    MT_PAST_FEW_DAYS,
    2,
    MMT_PRACTICE_THOSE
)


##########
# Practice Message - High Error Tables
##########

## NOTE: This is a bit harsh, but need to distinguish from z-score?
MT_MOST_MISTAKES = (
    "you make a lot of mistakes",
    "you mess up questions",
)

MT_FROM_THE = (
    "from the",
    "in the",
)

MMT_INCORRECT_PROBLEMS = (
    MT_GEN_PRACT_INTRO,
    MT_MOST_MISTAKES,
    MT_FROM_THE,
)


##########
# Practice Message - High Z-Score Tables
##########

MT_WHEN_MISTAKE = (
    "when you mess up,",
    "when you make a mistake,",
)

MT_OFTEN = (
    "it's usually",
    "it's often",
)

MMT_HIGH_Z_SCORE = (
    MT_GEN_PRACT_INTRO,
    MT_WHEN_MISTAKE,
    MT_OFTEN,
    MT_FROM_THE,
)


##########
# Practice Message - New Tables
##########

MT_DOING_GOOD = (
    "You're already good",
    "You do awesome",
    "You're great",
)
MT_TABLES_PRACTICE = (
    "at the tables",
    "at the questions",
)
MT_YOU_PRACTICE = (
    "you practice.",
    "you practice a lot.",
)

MT_LETS_PRACTICE = (
    "Let's practice",
    "Let's do",
)

MT_HARDER_TABLES = (
    "some harder questions.",
    "some higher times tables.",
)

MTT_NEW_TABLES = (
    0.5,
    MT_DOING_GOOD,
    MT_TABLES_PRACTICE,
    MT_YOU_PRACTICE,
    2,
    MT_LETS_PRACTICE,
    MT_HARDER_TABLES,
)


##########
# Finished practice messages
##########

MT_YOU_ANSWERED = (
    "You answered",
    "You answered",
    "You solved",
)
MT_ALL_THE = (
    "all of the",
    "all the",
    "the",
)
MT_PROBLEM_SYNS = (
    "problems",
    "questions",
    "times tables",
)
MT_MISTAKES = (
    "you made mistakes on",
    "you messed up",
)
MT_RECENT = (
    "in the past few days.",
    "recently.",
)
MMT_FIN_INCORRECT_PROBLEMS = (
    MT_YOU_ANSWERED,
    MT_ALL_THE,
    MT_PROBLEM_SYNS,
    MT_MISTAKES,
    MT_RECENT,
)


MS_IN_ROW = f"{QUESTIONS_PER_MODE} questions correctly in a row"
MS_FROM = "from"

MT_HIGH_ERRORS = (
    "the tables you mess up often.",
    "the tables you mess up a lot.",
)

MMT_HIGH_ERROR_TABLES = (
    MT_YOU_ANSWERED,
    MS_IN_ROW,
    MS_FROM,
    MT_HIGH_ERRORS,
)

MT_HIGH_Z_SCORE = (
    "the tables you mess up the most.",
    "your most common mistake times tables.",
)

MMT_HIGH_Z_SCORE_TABLES = (
    MT_YOU_ANSWERED,
    MS_IN_ROW,
    MS_FROM,
    MT_HIGH_Z_SCORE,
)

MT_NEW_TABLES = (
    "the harder tables.",
    "the higher times tables.",
    "the harder tables I assigned you.",
)


"You completed my entire custom practice."

MT_COMPLETED = (
    "You finished",
    "You completed",
)
MT_YOUR_CP = (
    "your custom practice.",
    "the custom practice I designed for you.",
)


MMT_NEW_TABLES = (
    MT_YOU_ANSWERED,
    MS_IN_ROW,
    MS_FROM,
    MT_NEW_TABLES,
    2.25,
    MT_COMPLETED,
    MT_YOUR_CP,
)
 

##########
# To Complete Practice
##########

MT_TO_COMPLETE = (
    "To complete this practice,",
    "To finish this practice,",
)

MT_ANSWER = (
    "answer",
    "answer",
    "solve",
)

MS_NUM_IN_ROW = f"{QUESTIONS_PER_MODE} questions correctly in a row."

MMT_COMPLETE_PRACTICE = (
    1.5,
    MT_TO_COMPLETE,
    MT_ANSWER,
    MS_NUM_IN_ROW,    
)

