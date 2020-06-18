"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-08 11:24:55
 * @modify date 2020-06-16 15:52:05
 * @desc [
    Utility function to combine a list of items into a string.
 ]
 */
"""

def get_str_from_list(message_list: list, cc: str = "and", punct: bool = True) -> str:
    """Returns list as a formatted string for speech.
    
    message list: [list] of the components to be joined.
    cc: [str] coordinating conjunction to place at end of list.
    punct: bool - indicates if should include punctuation at end of list.
    """
    speech_list = []

    if not message_list:
        return ''
    elif len(message_list) == 1:
        message = str(message_list[0])
        if punct:
            message += "."
        return message

    for i in range(len(message_list)):
        if i == len(message_list) - 1:
            speech_list.append(' and ')
        
        speech_list.append( str(message_list[i]))
        if i != len(message_list) - 1:
            speech_list.append(', ')

    if punct:
        speech_list.append('.')
    return ''.join(speech_list)

