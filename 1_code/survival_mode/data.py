"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 09:56:46
 * @modify date 2020-06-16 23:43:24
 * @desc [
     Data module for survival mode. Contains data for:
     - Mode Name
     - Welcome
     - Scores
     - Z-score response lists
     - Survival Mode High Scores
 ]
 */
"""

##########
# Imports
##########


##########
# Mode Name
##########
MODE_NAME = "Survival Mode"


##########
# Survival Welcome
##########

MMT_FIRST_WELCOME = (
    f"Welcome to {MODE_NAME}.",
    1,
    f"In {MODE_NAME}, answer as many questions as you can, without making a mistake.",
    2,
    "But watch out! The questions get harder until you mess up!",
)


##########  Short Welcome

MT_SHORT_WELCOME = (
    "Welcome back to",
    "Welcome to",
    "Loading",
)
MMT_SHORT_WELCOME = (
    MT_SHORT_WELCOME,
    " ",
    MODE_NAME,
    "!"
)

##########  Long Welcome

MT_HOW_MANY = (
    "How many",
)

MT_QUESTION_SYN = (
    "questions",
    "problems",
    "times tables",
    "tables",
)

MT_SOLVE = (
    "can you get right?",
    "can you get?",
    "can you do?",
    "can you answer?",
)

MMT_LONG_WELCOME = (
    MT_SHORT_WELCOME,
    " ",
    MODE_NAME,
    "!",
    " ",
    MT_HOW_MANY,
    " ",
    MT_QUESTION_SYN,
    " ",
    MT_SOLVE,
)

##########  Scores
MT_HIGH_SCORE = (
    "Your high score is {}",
    "Your record is {}",
)

MT_AVERAGE_SCORE = (
    "You usually get to {}",
    "On average, you get to {}",
)

MT_BEAT_IT = (
    "Let's beat that!",
    "Let's try and beat that!",
    "Let's try and do better than that!",
    "Let's set a new record!",

    "Can you beat that?",
    "Do you think you can do better?",
)

##########
# SM Score
##########

MT_PROBLEM_SCORE = (
    "You got through {} questions!",
    "You answered {} questions!",
    "You made it through {} questions!",
    "You answered {} questions correctly!",
)


##########
# Z-score response lists
##########

MT_BETTER_NEXT_TIME = (
    "Let's try and get higher next time.",
    "Let's get a higher score next time.",
    "We can do better next time.",
    "We'll do better next time.",
)

MT_NORM_ATTEMPT = (
    "Keep practicing and get even better.",
    "Good game.",
    "Nice game.",
)

MT_GOOD_ATTEMPT = (
    "That's better than usual!",
    "You're definitely improving!",
    "You're getting better at this!",
    "You're getting further each time!",
    "You get better each time!",
)

MT_AWESOME_ATTEMPT = (
    "You got really far this time!",
    "You're on the way to setting a new record!",
    "You almost set a new record!",
    "Keep this up, and you'll set a new high score!",
)


##########
# Survival Mode High score
##########
MS_FIRST_HS = "I'll set your Survival Mode highscore as {} questions."

## Beat highscore MTT
MS_YOU = "You"
MT_BEAT = (
    "beat",
    "passed",
)
MS_YOUR = "your"
MT_HIGH_SCORE_SYNS = (
    "old highscore",
    "highscore",

    "old record",
    "record",
)
MS_OF = "of"
MTT_BEAT_OLD_HS = (
    MS_YOU,
    MT_BEAT,
    MS_YOUR,
    MT_HIGH_SCORE_SYNS,
    MS_OF,
)       # format with problem, & chance of questions. syns


# MT_NEW_HS = (         # not used right now.
#     "I'll set your new highscore as {}.",
#     "Your new high score is {}.",
#     "Your new record is {}."
# )

MT_TIE_HS = (
    "You tied your highscore of {}!",
    "You tied your highscore of {} questions!",
    "{} questions? Ha! That's your high score!",
)



