""""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 09:23:10
 * @modify date 2020-05-12 09:23:10
 * @desc [
    Generates sample utterances for the SetBoundsIntent.
 ]
 */
"""

##########
# Imports
##########


##########
# Bounds 
##########
MT_MAKE = [
    "Set",
    "Make",
    "Change",
]

MT_BOUNDS = [
    r"the bounds from {lower_bound} to {upper_bound}",
    r"the lower bound to {lower_bound}",
    r"the upper bound to {upper_bound}",
]

MMT_BOUNDS = (
    MT_MAKE,
    MT_BOUNDS
)

##########
# Generate utterances
##########

def print_ms_permutations(master_list: list):
    """Calls helper function to recursively create speech lists with
    all permutations of clauses from master list."""

    def helper(speech_list: list, i: int, j: int):
        while i < len(master_list):
            message_list = master_list[i]

            while j < len(message_list) - 1:
                recursive_speech_list = speech_list + [message_list[j]]
                helper(recursive_speech_list, i + 1, 0)

                j += 1
            
            speech_list.append( message_list[j])
            j = 0
            i += 1
        speech = ' '.join(speech_list)
        print( speech)
    

    helper([], 0, 0)


print_ms_permutations(MMT_BOUNDS)

