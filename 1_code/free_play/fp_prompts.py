"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-16 14:52:14
 * @modify date 2020-05-27 09:53:27
 * @desc [
    FPPrompts utility class.
 ]
 */
"""

##########
# Imports
##########

from logs import log_func_name, logger
from skill_card.card_funcs import CardFuncs

from act_descriptions.act_descript_utils import DescriptUtils
from mult_questions.fp_question import FPQuestions
from free_play.fp_timestables import FPTimesTables
from mult_questions.question_attr import QuestionAttr
from mult_questions.gen_questions import GenQuestions
from helper.help_utils import HelpUtils


##########
# Prompts Utility class
##########

class FPPrompts(object):

    @staticmethod
    @log_func_name
    def get_q_fp_setup_prompt(handler_input) -> str:
        """Returns prompt for freeplay setup handlers."""
        attr = handler_input.attributes_manager.session_attributes
        if (
            attr.get('mode', None) == "free_play" and 
            attr.get('times_tables', None) not in (None, [])
        ):
            prompt = FPPrompts.get_fp_question(handler_input)

        elif (attr.get('mode', None) == "free_play"):
            prompt = FPTimesTables.get_ms_can_add_tables()
            
        else:
            prompt = FPPrompts.get_q_start_fp(handler_input)
        
        return CardFuncs.format_prompt(prompt)


    @staticmethod
    @log_func_name
    def get_q_fp_setup_reprompt(handler_input) -> str:
        """Returns reprompt for freeplay setup handlers."""
        attr = handler_input.attributes_manager.session_attributes
        if (
            attr.get('mode', None) == "free_play" and 
            attr.get('times_tables', None) not in (None, [])
        ):
            prompt = GenQuestions.get_same_question(handler_input)
        else:
            prompt = HelpUtils.get_q_what_todo()

        return CardFuncs.format_prompt(prompt)


    @staticmethod
    @log_func_name
    def get_q_start_fp(handler_input) -> str:
        """Returns message asking if user wants to start FP."""
        DescriptUtils.set_attr(handler_input, "free_play")
        
        return DescriptUtils.get_q_play_activity("free_play")


    @staticmethod
    @log_func_name
    def get_fp_question(handler_input) -> str:
        """Returns Free Play multiplication question with new parameters."""
        attr = handler_input.attributes_manager.session_attributes

        ms_question = FPQuestions.get_question(handler_input, first_question= True)
        # QuestionAttr.increment_questions_answered(handler_input, increase=False)
        return ms_question

