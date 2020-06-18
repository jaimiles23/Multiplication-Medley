"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-20 23:22:50
 * @modify date 2020-05-22 23:32:45
 * @desc [
    Data module for speed challenge. Contains data for:
    - General
    - Welcomes
    - Player personalized messages
    - Choosing difficulties
    - Timer
    - Completion
    - High score
    - Relatize Z-Score responses
 ]
 */
"""


##########
# General
##########

SC_DIFFICULTIES = (
    "normal",
    "hard",
    "advanced",
    "insane",
)

SC_DIFF_DICT = {
    "normal"    :   (0, 10),
    "hard"      :   (0, 12),
    "advanced"  :   (10, 20),
    "insane"    :   (20, 30)
}


MT_QUESTION_SYNS = (
    "questions",
    "problems",
    "times tables",
    "tables",
)

##########
# Welcomes
##########

MODE_NAME = "Speed Challenge!"


MS_SC_FIRST_WELCOME = f"Welcome to {MODE_NAME}"
MS_PURPOSE = "In this mode, you answer times tables as quickly as you can."
MS_HOW_SCORED = "I score you on how fast you answer my questions."

MMT_SC_FIRST_WELCOME = (
    MS_SC_FIRST_WELCOME,
    1.5,
    MS_PURPOSE,
    2,
    MS_HOW_SCORED,
)

MT_SHORT_WELCOME = (
    "Welcome back to",
    "Welcome to",
    "Let's start",
)
MTT_SHORT_WELCOME = (
    MT_SHORT_WELCOME,
    MODE_NAME,
)


MT_LONG_WELCOME = (
    "How quickly can you answer the ",
    "How fast can you solve the ",
)

MTT_LONG_WELCOME = (
    MT_SHORT_WELCOME,
    MODE_NAME,
    1,
    MT_LONG_WELCOME,
    MT_QUESTION_SYNS,
)


##########
# Player personalized messages
##########

MT_HIGH_SCORE = (
    "Your highscore in {} difficulty is {}.",
    "Your record in {} difficulty is {}.",
)

MT_AVERAGE_SCORE = (
    "In {} difficulty, you usually get {} .",
    "In {} difficulty, you often get around {}.",
)

MT_BEAT_IT = (
    "Let's beat that!",
    "Let's try and beat that!",
    "Let's set a new record!",

    "Can you beat it?",
    "Do you think you can beat that?",
)


##########
# Choose Difficulty
##########

MT_WHAT = (
    "What",
    "What",
    "Which",
)
MS_DIFFICULTY = "difficulty",
MT_ATTEMPT = (
    "should we play?",
    "do you want to play?",

    "should we try?",
    "do you want to try?",
)

MMT_WHAT_DIFFICULTY = (
    MT_WHAT,
    MS_DIFFICULTY,
    MT_ATTEMPT,
)

MT_CAN_USE = (
    "You can choose",
    "You can play",
)
MS_ONE_OF_FOLLOWING = "one of the following difficulties:"
MS_DIFF_LIST = "Normal, Hard, Advanced, or Insane."
MMT_CAN_USE_DIFF = (
    MT_CAN_USE,
    MS_ONE_OF_FOLLOWING,
    0.5,
    MS_DIFF_LIST
)

MS_GET_DIFF_HELP = "If you want to hear about each difficulty, ask me for help."


MT_USE = (
    "Let's use",
    "I'll set up",
    "Starting",
)
MS_DIFFICULTY_FORMAT = "{} difficulty."

MT_SORRY = (
    "Sorry,",
    "Sorry,",
    "I'm sorry,",
)
MT_NOT_REGISTER = (
    "I didn't catch that.",
    "I didn't hear you.",
    "I didn't get that.",
)
MT_RETRY = (
    "Please try again.",
    "Can you try again?",
)
MTT_TRY_AGAIN = (
    MT_SORRY,
    MT_NOT_REGISTER,
    1,
    MT_RETRY,
)

##########
# Timer
##########

MT_START_TIMER = (
    "Starting timer, now!",
    "Timer starting now!",
    "I'm starting the timer now!",
)


##########
# Completed Speed Challenge
##########

MT_COMPLETED_SC = (
    "You completed",
    "You finished",
    "You answered",
)

MS_SC_MINUTES_SECONDS_SCORE = "{} minutes and {} seconds"
MS_SC_SECONDS_SCORE = "{} seconds"

MS_FIN_SC_DIF_SEC = "{} difficulty in {}!"
MS_FIN_SC_NUMQ_SEC = "{} questions in {}!"
MS_FIN_SC_LOWTBL_UPPTBL_SEC = "my questions from the {} to {} times tables in {}!"


##########
# Speed Challenge High Score
##########
MS_FIRST_HS = "I'll set your highscore for {} difficulty as {}."

########## Beat highscore MTT
MS_YOU = "You"
MT_BEAT = (
    "beat",
    "passed",
)
MS_YOUR = "your"
MT_OLD_HS_SYNS = (
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
    MT_OLD_HS_SYNS,
    MS_OF,
)       # format with seconds, & seconds
MS_SC_SCORE_SECONDS = "{}!"


########## New High score
MS_YOUR_NEW = "Your new"
MT_HS_SYNS = (
    "high score",
    "record",
    "personal record",
)
MS_FOR_DIFF_SECONDS = "for {} difficulty is {}."


MMT_NEW_HS = (
    MS_YOUR_NEW,
    MT_HS_SYNS,
)

########## Tied HS

MT_TIE_HS = (
    "You tied your highscore of {}!",
    "That ties your highscore of {}!",
    "{}? Ha! That's your high score!",
)
MT_TIE_HS_PART_2 = (
    "Close one!",
    "Set a new one next time!",
)

##########
# Relative Z-Score responses
##########

MT_BETTER_NEXT_TIME = (
    "Let's be even faster next time.",
    "Let's get even faster next time.",
    "We can do better next time.",
    "We'll be faster next time.",
)

MT_NORM_ATTEMPT = (
    "Keep practicing and get even faster.",
    "Good game.",
    "Nice game.",
)

MT_GOOD_ATTEMPT = (
    "That's faster than usual!",
    "You're definitely getting faster!",
    "You're getting faster at this!",
    "You're getting faster each time!",
    "You get faster each time!",
)

MT_AWESOME_ATTEMPT = (
    "You were really fast this time!",
    "You're on the way to setting a new record!",
    "You almost set a new record!",
    "Keep this up, and you'll set a new high score!",
)
