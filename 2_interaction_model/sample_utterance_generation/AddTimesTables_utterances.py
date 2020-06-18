"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 10:10:27
 * @modify date 2020-05-12 10:10:27
 * @desc [
    Generates sample utterances for adding times tables to Free Play.
 ]
 */
"""

##########
# Add problems data
##########

TL_ADD = [
    "Add",
    "Include",
]
TL_FOLLOWING = [
    "the following",
    "these",
]

TL_TABLES = [
    "times tables",
    "tables",
]

MS_TABLES_QUERY = r"{tables_query}"

MTT_ADD_TABLES = [
    TL_ADD,
    TL_FOLLOWING,
    TL_TABLES,
    MS_TABLES_QUERY,
]

##########
# Recursive Function
##########

def print_utterance_permutations(master_list: list):
    """Prints all clause permutations from the master list."""

    def helper(speech_list, i):
        """Recursively creates speech_lists to hold all utterance permutations."""

        while i < len(master_list):
            clause = master_list[i]

            if isinstance(clause, str):
                speech_list.append(clause)

            elif isinstance(clause, (list, tuple)):
                j = 0
                while j < len(clause) - 1:
                    recursive_speech_list = speech_list + [clause[j]]
                    helper(recursive_speech_list, i + 1)
                    j += 1
                
                speech_list.append(clause[j])
            
            i += 1
        print(' '.join(speech_list))
    
    helper([], 0)


print_utterance_permutations(MTT_ADD_TABLES)


        
                


