"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 15:10:52
 * @modify date 2020-06-16 15:11:39
 * @desc [
     get_ms_from_tuple is an auxiliary function to create a message from a Master Message Tuple (MMT).

     The MMT is a tuple of clauses that can be linearly sampled from to create a message. 
     Randomly sampling from each clause tuple creates variety in the user experience and maintains the meaning.
     
     Refer to the discussion on Clause construction in the README.md
     
    NOTE: 
    - Consider is_instance(data, (tuple, list)) vs has_attr(__iter__)??
]*/
"""


##########
# Imports
##########

import random


from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name
from pause.pauser import Pauser


##########
# Create Message from Tuple of Message Clauses
##########

@log_func_name
def get_ms_from_tuple(tuple_message_clause: tuple, str_joiner: str = ' ') -> str:
    """Returns message constructed from tuple message clause.
    
    Constructs the message with different methods per data type.
    ##  Data type       Method
        Tuple/list      random.choice()
        str             append
        int             Pauser.get_p_level()
    """
    def get_clause(tup_data) -> str:
        """Helper func: returns clause from tup_data using recursion."""
        if not tup_data:
            return ''

        elif isinstance(tup_data, str):
            return tup_data

        elif isinstance(tup_data, (int, float)):
            return Pauser.get_p_level(tup_data)
            
        elif isinstance(tup_data, (tuple, list)):

            if isinstance(tup_data[0], str):
                ## List of strings, return choice.
                return random.choice(tup_data)

            else:   
                # Use Tuples in tuple to create message
                speech_list = []
                for clause_list in tup_data:
                    clause = get_clause(clause_list)
                    speech_list.append(clause)

                return str_joiner.join(speech_list)
        else:
            logger.warning(f"get_clause: Unrecognized data type {tup_data}")
    

    logger.debug(tuple_message_clause)
    speech_list = []

    for tup_data in tuple_message_clause:
        clause = get_clause(tup_data)
        speech_list.append( clause)
    
    # logger.debug(speech_list)
    return str_joiner.join(speech_list)

