"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 12:43:22
 * @modify date 2020-05-23 12:28:19
 * @desc [
    Data module for helper handler with data for:
    - Help overview
    - Free play
    - Custom mode
    - Survival mode
    - Speed challenge
    - user profile
    - Todo prompts
 ]
 */
"""

##########
# Imports
##########


##########
# Help overview
##########

MT_HELP_OVERVIEW_P1 = (
    "I have",
    "I know",
)
MT_HELP_OVERVIEW_P2 = (
    "4 activities",
    "4 different activities",
    "4 games",
    "4 different games",
)
MT_HELP_OVERVIEW_P3 = (
    "to play:",
    "to explore:",
    "to practice Multiplication:",
    "to practice your Multiplication skills:",
    "for Multiplication:",
)
MT_HELP_OVERVIEW = (
    MT_HELP_OVERVIEW_P1,
    MT_HELP_OVERVIEW_P2,
    MT_HELP_OVERVIEW_P3,
    1,
)


##########
# Free Play
##########

MS_FP_TIMES_TABLES = "Tell me what Times tables you want to practice."

MS_FP_OVERVIEW = "In free play, you can customize what you want to practice."
MS_FP_STD_PARAMS = """You can add or set tables to practice, 
and tell me how many problems to ask you."""


##########
# Custom Mode
##########
MS_CP_INTRO = "In Custom Mode, I'll design a practice session just for you."
MS_CP_WRONG = "First, I'll ask you questions that you messed up in the last few days."
MS_CP_FREQ_ERR = "Next, I'll ask questions that you tend to make mistakes on more often."
MS_CP_HIGHER_TBL = "Once you're finished, I'll ask questions times tables you don't practice as often."

MMT_CUSTOM_PRACTICE = (
    MS_CP_INTRO,
    1,
    MS_CP_WRONG,
    1.5,
    MS_CP_FREQ_ERR,
    1.5,
    MS_CP_HIGHER_TBL,
)

##########
# Survival Mode
##########

MS_SURVIVAL_MODE = "In Survival Mode, you see how many questions you can answer in a row before making a mistake."
MS_HARD_QUESTIONS = "I'll keep making the questions harder until you mess up!"
MS_HEAR_RECORD = "If you want to hear your record, try saying: 'What's my record for survival mode?'"

MTT_SURVIVAL_MODE = (
    MS_SURVIVAL_MODE,
    1,
    MS_HARD_QUESTIONS,
    1.5,
    MS_HEAR_RECORD,
)

##########
# Speed Challenge
##########
MS_SC_INTRO = "In Speed Challenge, I time how fast you can answer my questions."
MS_SC_DIFF = "Pick one of the four levels for different times tables."
MS_SC_NORM = "On Normal, I'll ask you questions from the 0 to 10's times tables."
MS_SC_HARD = "On Hard, I'll use the 0 to 12's tables."
MS_SC_ADVANCED = "Advanced jumps to the 10's to 20's times tables."
MS_SC_INSANE = "And Insane ranges all the way from the 20 to 30's tables."
MS_SC_RECORD = "If you want to hear your record"
MS_TRY_SAYING = "try saying: 'What's my record for speed challenge normal difficulty?'"

MMT_SPEED_CHALLENGE = (
    MS_SC_INTRO,
    1,
    MS_SC_DIFF, 
    2,
    MS_SC_NORM,
    1,
    MS_SC_HARD,
    1,
    MS_SC_ADVANCED,
    1,
    MS_SC_INSANE,
    2.25,
    MS_SC_RECORD,
    1,
    MS_TRY_SAYING
)


##########
# User profile
##########

MS_HELP_CREATE_USER_PROFILE = """I need your name to create a user profile."""

MS_PROFILE_TRACK = """I use your profile to track what questions you get right, 
and what problems you struggle on."""

MS_PROFILE_RECOMMEND = """This helps me make recommendations on what you should practice."""

MT_HELP_USER_PROFILE = (
    MS_HELP_CREATE_USER_PROFILE,
    1,
    MS_PROFILE_TRACK,
    1,
    MS_PROFILE_RECOMMEND,
)


##########
# Todo prompts
##########

MS_WHAT_TODO_PROPER = "What do you want to do?"
MT_WHAT_TODO = (
    MS_WHAT_TODO_PROPER,
    MS_WHAT_TODO_PROPER,
    "What did you want to do?",
)

##########
# miscellaneous
##########

MS_FIRST_PLAY_NAME_REPROMPT = """Tell me your name so I can make a profile."""

