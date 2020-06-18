"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 09:08:30
 * @modify date 2020-05-12 09:08:30
 * @desc [
    Generate sample utterances for the NumQuestionsIntent.
]
*/
"""
##########
# Imports
##########

##########
# Data
##########

TL_ASK_QUIZ = [
    "ask me",
    "quiz me on",
    "test me on",
]

##########
# Num Questions
##########

MT_QUESTIONS = [
    r"{num_questions} questions",
    r"{num_questions} multiplication questions",
    r"{num_questions} times table questions",
]

MMT_NUM_QUESTIONS = [
    TL_ASK_QUIZ,
    MT_QUESTIONS,
]

MT_SET = (
    "set",
    "make"
)
MT_DET = (
    "the",
    "",
)
MT_QUESTIONS2 = (
    "questions",
    "number of questions",
)
ML_TO = ["to"]
ML_NUM_QUESTIONS = [r"{num_questions}"]

MMT_SET_QUESTIONS = (
    MT_SET,
    MT_DET,
    MT_QUESTIONS2,
    ML_TO,
    ML_NUM_QUESTIONS,
)


##########
# Generate Utterances
##########

def print_ms_permutations(
    master_list: list,
    speech_list: list = [],
    i: int = 0,
    j: int = 0,
    ):
    """prints all permutations of the master list."""
    while i < len(master_list):
        message_list = master_list[i]

        while j < len(message_list) - 1:
            speech_list_for_recursion = speech_list + [message_list[j]]
            print_ms_permutations(master_list, speech_list_for_recursion, i + 1, 0)
            j += 1
        
        speech_list.append( message_list[j])    # Otherwise, continues execution func w/o using that this message_list
        j = 0
        i += 1

    print( ' '.join(speech_list))


# print_ms_permutations(MMT_NUM_QUESTIONS)
print_ms_permutations(MMT_SET_QUESTIONS)
