"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 12:51:38
 * @modify date 2020-05-27 12:26:36
 * @desc [
    GenQuestions utility class for general question methods
 ]
 */
"""

##########
# Imports
##########

from logs import logger, log_func_name, log_all


from mult_questions.question_attr import QuestionAttr


##########
# GenQuestions
##########

class GenQuestions(object):
    @staticmethod
    @log_func_name
    def format_question(question: tuple) -> str:
        """Formats the question for Alexa <speak>"""
        try:
            for q in question:
                int(q)
        except Exception as e:
            logger.error(f"format_question:  Asking non-int tables  {e}")

        speech_list = (
            " ",
            str(question[0]),
            " times ",
            str(question[1]),
        )
        return ''.join(speech_list)


    @staticmethod
    @log_func_name
    def get_same_question(handler_input) -> str:
        """Returns the same question to the user."""
        question = QuestionAttr.get_question_tables(handler_input, integers=False)

        question = GenQuestions.format_question(question)
        return question
    

    @staticmethod
    @log_func_name
    def check_same_question(handler_input, new_question: tuple) -> bool:
        """Returns boolean representing if same question asked to the user."""
        old_question_1, old_question_2 = QuestionAttr.get_question_tables(handler_input, integers=True)
        log_all(old_question_1, old_question_2, new_question[0], new_question[1])

        return (
            new_question[0] == old_question_1 and 
            new_question[1] == old_question_2
            )

