"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 09:58:55
 * @modify date 2020-05-12 09:58:55
 * @desc [
    Generates sample utterances for setting the times tables.
 ]
 */
"""

MS_USE = "Use",

TL_SET = [
    "Set the",
    "Change the",
]
MS_TO = "to"
ML_START_RANGE = [
    "from",
    "between",
    "to",
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
MS_HIGH = r"{upper_table}"
ML_JOINER = [
    "to",
    "and"
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

MTT_TABLE_RANGE = [
    TL_SET,
    TL_PROBLEM_SYNONYMS,
    ML_START_RANGE,
    MS_LOWER,
    ML_JOINER,
    MS_HIGH,
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

MTT_TABLE_QUERY = [
    TL_SET,
    TL_PROBLEM_SYNONYMS,
    MS_TO,
    TL_FOLLOWING,
    TL_TABLES,
    MS_TABLES_QUERY,
]

MTT_SHORT_QUERY = [
    MS_USE,
    TL_FOLLOWING,
    TL_TABLES,
    MS_TABLES_QUERY,
]


##########
# Recursive Helper function
##########

def print_ms_permutations(master_list: list):
    """prints all permutations from the clauses in masterlist."""

    def helper(speech_list: list, i: int):
        """Recursively called to construct all permutations from speechlist.

        prints speech_list @ end."""
        
        while i < len(master_list):
            clause = master_list[i]

            if isinstance(clause, str):
                speech_list.append( clause)
            
            elif isinstance(clause, (list, tuple)):
                j = 0
                while j < len(clause) - 1:
                    select_clause = clause[j]
                    recursive_speech_list = speech_list + [select_clause]

                    helper(recursive_speech_list, i + 1)
                    j += 1
                
                speech_list.append( clause[j])

            i += 1

        speech = ' '.join(speech_list).strip()
        print(speech)
    

    helper([], 0)


print_ms_permutations(MTT_TABLE_RANGE)
print_ms_permutations(MTT_TABLE_QUERY)
print_ms_permutations(MTT_SHORT_QUERY)



