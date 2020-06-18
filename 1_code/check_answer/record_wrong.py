"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-24 13:17:55
 * @modify date 2020-06-16 15:57:56
 * @desc [
    Utility class with methods to record wrong answers.
    
NOTE: The CURRENT dictionary structure for incorrect problems is as follows:

```python3
wrong_quest_by_date = {
    date1   :   {
        table_1   :   {
            table_2 :   int_incorrect,
            table_3 :   int_incorrect,
        },
        2nd_table   :   {
            table_1 :   int_incorrect,
            table_2 :   int_incorrect,
        },
    }
    date2   :   {
        table_1 :   {
            table_2 :   int_incorrect,
        },
    }
}
```

4 layer dictionary: all questions, specific dates, 1st table in problem, and 2nd table.
The last integer value is the number of times that problem was incorrect.

NOTE: This data structure should be changed to be: (1) User-specific, (2) have greater efficiency.
Refer to notes in README 
]
*/
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput


from logs import logger, log_func_name, log_all
from mult_questions.question_attr import QuestionAttr


##########
# Utility class to record wrong answers.
##########

class WrongAnswer(object):

    @staticmethod
    @log_func_name
    def record_wrong_question(handler_input) -> None:
        """Saves the question as a session attribute.

        Implementation NOTE:
        Currently using series of get statements
        May be able to use a while loop instead that checks if data type is dict.
        May also like to change to try-except statement.
        """
        attr = handler_input.attributes_manager.session_attributes

        ## Keys
        wrong_quest_by_date = attr['wrong_quest_by_date']
        today = attr['today']
        table_1, table_2 = QuestionAttr.get_question_tables(handler_input, integers= False)
        log_all(wrong_quest_by_date, today, table_1, table_2)

        ## Get Dicts
        incorrect_today_dict = wrong_quest_by_date.get(today, {})
        tbl_1_incorrect_dict = incorrect_today_dict.get(table_1, {})
        tbl_2_val = tbl_1_incorrect_dict.get(table_2, 0)
        log_all(incorrect_today_dict, tbl_1_incorrect_dict, tbl_2_val)

        ## Val
        tbl_2_val += 1

        ## Update dicts
        tbl_1_incorrect_dict[table_2] = tbl_2_val
        incorrect_today_dict[table_1] = tbl_1_incorrect_dict
        wrong_quest_by_date[today] = incorrect_today_dict
        attr['wrong_quest_by_date'] = wrong_quest_by_date
        
        log_all(incorrect_today_dict, tbl_1_incorrect_dict, tbl_2_val)
        return