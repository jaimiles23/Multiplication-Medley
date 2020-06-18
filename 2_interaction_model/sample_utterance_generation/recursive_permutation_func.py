"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 09:34:44
 * @modify date 2020-05-12 09:34:44
 * @desc [
    Sample of recursive function to print all permutations of utterances.
 ]
 */
 """

##########
# Recursively generate permutations
##########

def print_utterance_permutations(master_list: list):
    """Calls helper function to recursively create speech lists with
    all permutations of clauses from master list."""

    def helper(speech_list: list, i: int):
        """Recursively creates speechlists to construct all clause permutations."""
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
                speech_list.append( clause[j])
            
            i += 1
        print(' '.join(speech_list))
    

    helper(speech_list = [], i = 0)

