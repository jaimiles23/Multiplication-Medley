"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-11 15:32:01
 * @modify date 2020-05-11 22:44:46
 * @desc [
    Generates sample utterances for the Free Play Intent.

    Sample utterances include variations of slots for:
        - lower_table
        - upper_table
        - query_tables
        - num_questions
        - lower_bound
        - upper_bound
 ]
 */
"""

##########
# Constant Strings
##########

ML_COORDINATING_CONJUNCTION = [
    "and use",
    "with",
]
MS_AND = ["and"]
MS_FROM = ["from"]
MS_USE = ["use"]
MT_RANGE_JOINER = [
    "from",
    "between",
]
MS_WITH = ["with"]

##########
# Free Play
##########

ML_START = [
    "Start",
    "Begin",
    "Open",
    "Launch",
]
MS_FP = ["Free Play"]

MTT_START_FP = [
    ML_START,
    MS_FP,
]

TL_ASK_QUIZ = [
    "ask me",
    "quiz me on",
    "test me on",
]


##########
# Table Range
##########


TL_PROBLEM_SYNONYMS = [
    "times tables",
    "tables",
    "questions",
    "problems"
]

MS_LOWER = r"{lower_table}"
MS_HIGHER = r"{upper_table}"
ML_CONNECTOR = [
    "to",
    "and",
    "from",
]
ML_TABLES = [
    "",
    "tables",
    "times tables",
]

# TL_TABLE_RANGE = [
#     r"{lower_table} to {upper_table}",
#     r"the {lower_table} to {upper_table} tables",
#     r"the {lower_table} to {upper_table} times tables",
# ]

# MTT_TABLE_RANGE = [
#     ML_START,
#     MS_FP,
#     MS_AND,
#     TL_ASK_QUIZ,
#     TL_PROBLEM_SYNONYMS,
#     MT_RANGE_JOINER,
#     MS_LOWER,
#     ML_CONNECTOR,
#     MS_HIGHER,
#     ML_TABLES,
# ]

MTT_TABLE_RANGE = [
    ML_START,
    MS_FP,
    ML_COORDINATING_CONJUNCTION,
    # MS_USE,
    ML_TABLES,
    MT_RANGE_JOINER,
    MS_LOWER,
    ML_CONNECTOR,
    MS_HIGHER,
    ML_TABLES,
]


##########
# Tables Query
##########

TL_FOLLOWING = [
    "the following",
    "these",
]

TL_TABLES = [
    "times tables",
    "tables",
]

MS_TABLES_QUERY = r"{tables_query}"

# MTT_TABLE_QUERY = [
#     ML_START,
#     MS_FP,
#     ML_COORDINATING_CONJUNCTION,
#     TL_ASK_QUIZ,
#     TL_PROBLEM_SYNONYMS,
#     MS_FROM,
#     TL_FOLLOWING,
#     TL_TABLES,
#     MS_TABLES_QUERY,
# ]

MMT_WITH_TABLE_QUERY = [
    ML_START,
    MS_FP,
    ML_COORDINATING_CONJUNCTION,
    TL_FOLLOWING,
    TL_TABLES,
    MS_TABLES_QUERY,
]


##########
# Recursive function
##########

def print_utt_permutations(master_list: list):
    """Calls helper function to print permutations of master_list."""

    def helper(speech_list: list, i: int, j: int) -> str:
        """Recursively constructs all speech_list permutations & prints"""

        while i < len(master_list):
            message_list = master_list[i]
            if isinstance(message_list, str):
                speech_list.append(message_list)
                i += 1
            
            elif isinstance(message_list, (list, tuple)):
                while j < len(message_list) - 1:
                    recursive_speech_list = speech_list + [message_list[j]]
                    helper(recursive_speech_list, i + 1, 0)

                    j += 1
                speech_list.append( message_list[j])
                j = 0
                i += 1
        
        print(' '.join(speech_list))
    
    helper(speech_list = [], i = 0, j = 0)


##########
# Generate Sample Utterances
##########
"""
Create combinations of:
- freeplay
    + table range
    + table query

NOTE:
ERROR WHERE IF LISTS ARE RUN TOGETHER, WEIRD INTERLIST OVERWRITING. NEED TO COMMENT OUT ONE AT A TIME TO RUN WITHOUT 
ENTANGLING???

NOTE:
Appears to be an error with Num_questions & including so many number slots in an utternace.
Instead, keep all optional slots as own intents:
    - num_questions
    - bounds
    - AND times tables again.

Query slot must be alone. THUS, have this as an optional slot.
"""

ALL_UTTERANCE_COMBOS = [
    # ## FP
    MTT_START_FP,
    # FP + RANGE
    MTT_TABLE_RANGE,

    # # ## FP + Query
    # MTT_TABLE_QUERY,
    MMT_WITH_TABLE_QUERY
]

for combo in ALL_UTTERANCE_COMBOS:
    print_utt_permutations(combo)