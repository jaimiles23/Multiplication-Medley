"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 16:26:07
 * @modify date 2020-05-04 16:26:07
 * @desc [
    Card Funcs to clean simple card:
    - get card title
    - clean card text
    - format prompt to the user.
]
*/
"""

##########
# Imports
##########

import re

from ask_sdk_core.handler_input import HandlerInput

from logs import logger, log_func_name
import skill_card.data as data


##########
# Utility class
##########

class CardFuncs(object):
    """Contains utility methods related to the skill card.
        - get_card_title
        - clean_card_text
        - format_prompt
    """

    @staticmethod
    @log_func_name
    def get_card_info(handler_input, speech: str) -> (str, str):
        """Returns tuple of (card_title, card_text) for skill card."""
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)
        
        return (card_title, card_text)


    @staticmethod
    @log_func_name
    def get_card_title(handler_input) -> str:
        """Returns the card title for the select activity.
        """
        attr = handler_input.attributes_manager.session_attributes

        mode = attr.get('mode', None)
        card_title = data.CARD_TITLE_DICT.get(
            mode, data.TITLE_SKILL_NAME)
        return card_title


    @staticmethod
    @log_func_name
    def clean_card_text(speech: str) -> str:
        """Returns cleaned text for the skill card

        Removes all SSML tags and double spaces."""
        if not speech:
            return ""
        
        logger.debug(f"pre-processed:   {speech}")
        clean_ssml_regex = r"<.*?>"
        card_text = re.sub(clean_ssml_regex, '', speech)

        card_text = card_text.replace('  ', ' ')
        logger.debug(f'cleaned text:    {card_text}')

        card_text = CardFuncs.format_mult_operator(card_text)
        return card_text


    @staticmethod
    @log_func_name
    def format_prompt(prompt: str) -> str:
        """Adds new line characters to separate prompt from rest of text.
        """
        prompt_format = '\n' * 2
        return (prompt_format + prompt)


    @staticmethod
    @log_func_name
    def format_mult_operator(card_text: str) -> str:
        """Changes 'times' to 'x' for skillcard.

        For pronunciation, Alexa speech, multiplication
        questions must be formatted as 9 times 9.
        This changes instances of 'times' to 'x'.
        """
        operator = " times "
        mult_op_loc = card_text.find(operator)
        if mult_op_loc == -1:
            return card_text
        
        try:
            digit_1_loc = mult_op_loc - 1
            digit_2_loc = mult_op_loc + 1
            int(card_text[digit_1_loc])
            int(card_text[digit_2_loc])
        
        except (ValueError, IndexError):
            logger.warning(f"mult operator not in equation: \n{card_text}")
            return card_text
        
        card_text = card_text.replace(operator, " x ")
        return card_text

