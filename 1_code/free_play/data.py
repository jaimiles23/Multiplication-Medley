"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-07 23:09:05
 * @modify date 2020-05-13 17:06:48
 * @desc [
    Data module for free play mode. Contains
    - Slots that can be provided in free play mode
    
    And messages for:
    - Auxiliary clauses
    - Times table range.
    - Add Times tables to practice
    - Existing tables
    - Number questions
    - Answered questions
    - Table Bounds
    - Welcome
    - Stop Playing
    - Times Table input
    - Times table query intent
    - Times Table Range intent
    - Answered all questions
    - Free Play parameters


    TODO: Add documentation for each section.
 ]
 */
"""


##########
# Imports
##########

from aux_data.SSML_tags import (
    MW_SLOW1, MW_SLOW2, MW_SLOW3, MW_SLOW4, MW_SLOW5
)


##########
# FreePlay slots
##########

OPTIONAL_SLOTS = (
    'num_questions',
    'lower_bound',
    'upper_bound',
)
TIMES_TABLE_SLOTS = (
    "lower_table",
    "upper_table",
    "tables_query",
)

FP_PARAMS = (
    "times_tables",
    "num_questions",
    "lower_bound",
    "upper_bound",
)


##########
# Auxiliary clauses
##########
MT_I_WILL = (
    "I'll",
    "I'll",
    "I'll",
    "I will",
)
MT_CAN = (
    "I can",
    "If you'd like, I can",
    "You can",
    "You can tell me to",
)



##########
# Use Times table range/query.
##########
"""NOTE: CHANGE ACRONYM FROM TL TO MT - message tuple.
"""
MS_USE = "use"

MT_USE_PROBLEMS = (
    "take questions",
    "ask questions",
    "ask you questions",
    "use problems",
    "use questions",
)

MS_FROM = "from"
MS_BETWEEN = "between"

MT_TABLE_RANGE = (
    "the {}'s and {}'s tables.",
    "the {}'s and {}'s times tables.",
)
MT_USE_TABLES = (
    "the following tables:",
    "the following times tables:",
)
MT_USE_SINGLE_TABLE = (
    "The {}'s times table.",
    "the {}'s table.",
)

MMT_USE_PROBLEMS_START = (
    MT_I_WILL,
    MT_USE_PROBLEMS,
)

MT_NOTE = (
    "Sorry,",
)
MT_MISUNDERSTOOD = (
    "I may have not understood",
    "I may have messed up",
)
MT_MISUNDERSTOOD2 = (
    "what you said.",
    "the times tables you said.",
)
MMT_MISTAKE_PARSING = (
    MT_NOTE,
    MT_MISUNDERSTOOD,
    MT_MISUNDERSTOOD2,
)

MT_IF_WRONG = (
    "If I misunderstood you,",
    "If I was wrong,",
    "If I messed up,",
)
MT_TRY_USING_AND = (
    f"please say {MW_SLOW2.format('and')}, in between each times tables.",
)
MMT_WRONG = (
    MT_IF_WRONG,
    MT_TRY_USING_AND,
)


##########
# Can Add Times Tables to practice
##########
MT_ADD_TABLES = (
    "Include",
    "Add",
)
MS_MORE = "more"
MT_TABLE_SYNYONMS = [
    "times tables",
    "tables",
]
MT_TABLE_SYNYONMS_SINGULAR = [
    "times table",
    "table",
]
MT_TO_PRACTICE = (
    "to your practice.",
    "to your practice tables.",
    "to the times tables."
)

MMT_CAN_ADD_TIMES_TABLES = (
    MT_CAN,
    MT_ADD_TABLES,
    MS_MORE,
    MT_TABLE_SYNYONMS,
    MT_TO_PRACTICE,
)

MT_FOLLOWING_TABLES = (
    "the following tables",
    "these tables"
)

MMT_EXAMPLE_ADD_TIMES_TABLES = (
    ## Add Try Saying() func.
    MT_ADD_TABLES,
    MT_FOLLOWING_TABLES,
    ## Add random numbers
)
MT_INCLUDING_TABLES = (
    "I will add the",
    "I am adding the"
)

##########
# Existing Tables
##########
MT_USE = (
    "use",
    "set_up",
)

MTT_EXISTING_TABLES = (
    MT_I_WILL,
    MT_USE,
    MT_USE_TABLES,    
)


##########
# Num questions
##########

MT_ASK_QUESTIONS = (
    "ask you",
    "ask",
    "quiz you on",
    "test you on",
)

MT_NUMBER = (
    "any number of",
    "a number of",
    "a certain number of",
    "whatever number of",
)

MT_QUESTIONS = (
    "questions.",
    "multiplication questions.",
    "times table questions.",
)

MMT_NUM_QUESTIONS = (
    MT_CAN,
    MT_ASK_QUESTIONS,
    MT_NUMBER,
    MT_QUESTIONS,
)

MMT_SET_QUESTIONS = (
    MT_I_WILL,
    MT_ASK_QUESTIONS

)


MT_ASK_ME_QUESTIONS = (
    "Ask me",
    "Quiz me on",
    "Test me on",
)

##########
# Answered Questions
##########

MS_ANSWERED = "You answered {}"

MMT_ANSWERED_QUESTIONS = (
    MS_ANSWERED,
    MT_QUESTIONS
)


##########
# Table bounds
##########
MS_CHANGE_UPPER_LOW_BOUNDS = "change the lower and upper bounds of the"


MT_LOWER_BOUND = (
    "I won't ask questions below {}",
    "I'll ask questions above {}",
)

MT_UPPER_BOUND = (
    "I won't ask questions above {}",
    "I'll ask questions below {}",
)

MT_CHANGE = (
    "set the",
    "change the",
)

MT_BOUND_TO = "to {}."


##########
# Welcome
##########
MS_FP_WELCOME = "Welcome to Free Play"
MS_FP_FIRST_WELCOME = f"{MS_FP_WELCOME}, where you set up your own practice!"

MS_FP_INCLUDE_PARAMS = f"""{MS_FP_WELCOME}.
You can also say the tables you want to practice when starting Free Play."""


##########
# Stop Playing
##########
MT_STOP_PLAYING = (
    "We'll stop playing",
    "Let's stop",
    "We can stop",
)
MS_FP = "free play."

MMT_STOP_FP = (
    MT_STOP_PLAYING,
    MS_FP
)


##########
# Get Times Tables input prompt
##########
MT_INTERROGATIVE = (
    "What",
    "What",
    "What",
    "Which",
)
MT_TABLES = (
    "multiplication tables",
    "times tables",
    "tables",
    "problems",
)
MT_PRACTICE = (
    "do you want to practice?",
    "do you wanna practice?",
    "should we practice?",
    "should I ask you?",
)

MMT_WHAT_TABLES_PRACTICE = (
    MT_INTERROGATIVE,
    MT_TABLES,
    MT_PRACTICE,
)


##########
# Times Table Query intent
##########
MT_USE_FOLLOWING = (
    "use the following",
)

# MT_START_TABLE_REQUEST = (
#     "Ask questions",
#     "Ask me questions",
#     "Use problems",
#     "Quiz me on problems", 
# )

# MT_USE_TABLES = (
#     "from the following",
# )


MMT_QUERY_TABLES_SETUP = (
    MT_USE_FOLLOWING,
    MT_TABLE_SYNYONMS,
)


##########
# Times Table Range intent
##########
MT_FROM = (
    "from the",
)
MT_TIMES_TABLES = (
    "times tables",
    "tables",
)

MT_RANGE_TABLES = (
    "between {} and {}.",
)


##########
# Answered All Questions
##########

"That's the X problems you asked for."

MT_DET = (
    "Those are",
    "That's",
)
MS_NUM = "the {}"

MT_PROBLEM_SYNS = (
    "questions",
    "problems",
)
MT_REQUESTED = (
    "you asked for.",
    "you wanted,",
)


##########
# Free Play Parameters
##########

MS_ASK_NUM_Q = "I'm asking you {} questions"
MS_ASK_Q = "I'm asking you questions"

MS_FROM_TABLES = "from the following tables: "

MS_LOWER_BOUND = "I won't ask questions below {}."
MS_UPPER_BOUND = "I won't ask questions above {}."
MS_LOWER_UPPER_BOUND = "I won't ask questions below {} and questions above {}."

