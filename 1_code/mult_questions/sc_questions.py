"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-21 15:57:13
 * @modify date 2020-05-21 22:29:45
 * @desc [
    SC_Questions for speed challenge questions. Methods for:
    - Get question
    - Load/generate Speed challenge questions
    - 
    

NOTE:
- No question intros are used, so only returning a formatted question.
- Generate & store the list of questions at the beginning, to avoid duplicates.
 ]
 */
"""


##########
# Imports
##########

import random

from logs import log_all, log_func_name, logger
from mult_questions.gen_questions import GenQuestions
from mult_questions.question_attr import QuestionAttr

import speed_challenge.data


##########
# Speed Challenge Questions
##########

class SC_Questions(object):

    ##########
    # Get question
    ##########
    @staticmethod
    @log_func_name
    def get_question(handler_input, first_question: bool = False) -> str:
        """Returns question for the user."""
        attr = handler_input.attributes_manager.session_attributes

        if not first_question:
            QuestionAttr.increment_questions_answered(handler_input)

        sc_questions = attr['sc_questions']
        question = sc_questions.pop()

        attr['sc_questions'] = sc_questions
        QuestionAttr.save_question(handler_input, question)

        return GenQuestions.format_question(question)
    

    ##########
    # Load/Generate sc_questions
    ##########
    @staticmethod
    @log_func_name
    def load_sc_questions(handler_input) -> None:
        """Generates all sc questions, shuffles, and saves as a session attribute."""
        attr = handler_input.attributes_manager.session_attributes
        sc_questions = SC_Questions.generate_questions(handler_input)

        random.shuffle(sc_questions)
        attr['sc_questions'] = sc_questions
        return


    @staticmethod
    @log_func_name
    def generate_questions(handler_input) -> list:
        """Generates list of questions to ask user in speed challenge."""
        lower_table, upper_table = SC_Questions.get_tables_range(handler_input)
        table_questions = list()
        num_questions = 3

        for table in range(lower_table, upper_table + 1):
            lower_range = range(lower_table, table + 1)
            upper_range = range(table + 1, upper_table + 1)

            rand_num = random.randint(0, int( (table - lower_table) / 2))
            rand_num = rand_num if rand_num <= num_questions else num_questions

            num_upp_q = num_questions - rand_num
            num_low_q = rand_num

            if num_upp_q > len(upper_range):
                difference = num_upp_q - len(upper_range)
                num_upp_q -= difference
                num_low_q += difference

            if num_low_q > len(lower_range):
                difference = num_low_q - len(lower_range)
                num_low_q -= difference
                num_upp_q += difference

            lower_questions = random.sample( lower_range, num_low_q)
            upper_questions = random.sample( upper_range, num_upp_q)
            table_questions.append(lower_questions)
            table_questions.append(upper_questions)
        
        sc_questions = list()
        times_table = lower_table
        for i in range(len(table_questions)):
            for table in table_questions[i]:
                sc_questions.append( (times_table, table))
            
            times_table = int((i + 1) / 2) + lower_table

        return sc_questions


    @staticmethod
    @log_func_name
    def get_tables_range(handler_input):
        """Returns the table range to generate questions."""
        attr = handler_input.attributes_manager.session_attributes
        sc_difficulty = attr['sc_difficulty']

        lower_range, upper_range = speed_challenge.data.SC_DIFF_DICT[sc_difficulty]
        attr['sc_tables'] = lower_range, upper_range
        
        return (lower_range, upper_range)

