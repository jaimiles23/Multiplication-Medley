"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-11 13:59:04
 * @modify date 2020-06-16 15:52:17
 * @desc [
    Utility class to save & load the last prompt given to the user.
 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.utils import is_intent_name

from logs import log_func_name, log_all, logger
from skill_card.card_funcs import CardFuncs
from helper.help_utils import HelpUtils
from mult_questions.fp_question import FPQuestions
from mult_questions.gen_questions import GenQuestions

import aux_data.skill_data


##########
# Utility class
##########

class LastPrompt(object):
    
    ##########
    # Save prompt
    ##########
    @staticmethod
    @log_func_name
    def save_last_prompt_func(handler_input, prompt: object):
        """Saves the last prompt as a function to call."""
        attr = handler_input.attributes_manager.session_attributes
        attr['prompt_func'] = prompt
        return


    @staticmethod
    @log_func_name
    def save_last_prompt_str(handler_input, prompt: str):
        """Saves the last prompt as a string to return."""
        attr = handler_input.attributes_manager.session_attributes

        speech_tags = [
            '<speak>',
            '</speak>',
        ]
        for tag in speech_tags:
            prompt = prompt.replace(tag, '')
        
        attr['prompt_ms'] = prompt


    ##########
    # Load prompt
    ##########
    @staticmethod
    @log_func_name
    def get_last_prompt(handler_input) -> str:
        """Returns the prompt used in the previous response.
        
        first checks if existing question to be asked. If so, asks the question.

        If function saved, uses function.
        Elif str prompt saved, uses cached from response interceptor.
        Else, uses HelpUtils.get_corresponding_message.
        """
        attr = handler_input.attributes_manager.session_attributes

        ## Free Play Questions
        question = attr.get('question', None)
        flag_in_game = attr.get('mode', None) in aux_data.skill_data.MODE_ACT_DICT.keys()
        log_all(question, flag_in_game)
        if (
            question and
            flag_in_game
        ):
            prompt_user = GenQuestions.get_same_question(handler_input)

        ## Don't repeat help 
        elif is_intent_name("AMAZON.HelpIntent")(handler_input):
            prompt_user = HelpUtils.get_q_what_todo()
            
        ## Standard questions
        ## NOTE: May like to save function references in the future. 
        # saving functions may create more variety.
        # elif attr.get('prompt_func', False):
        #     prompt_user = attr['prompt_func']
        #     attr['prompt_func'] = None
        # elif attr.get('prompt_ms', False):
        #     prompt_user = attr['prompt_ms']
        #     attr['prompt_ms'] = None
        # else:
        #     prompt_user = HelpUtils.get_ms_corresponding_help(handler_input)

        else:
            prompt_user = HelpUtils.get_q_what_todo()
        
        return CardFuncs.format_prompt( prompt_user)
        
        