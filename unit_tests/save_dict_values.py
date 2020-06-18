"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-24 15:55:49
 * @modify date 2020-05-24 15:56:40
 * @desc [
    Unit tests for checking dictionary save values.
 ]
 */
"""
"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-13 22:22:55
 * @modify date 2020-05-13 22:23:25
 * @desc [description]
 */
"""

##########
# Imports
##########

import pprint


##########
# Record wrong answer
##########

class WrongAnswer(object):

    @staticmethod
    def record_wrong_question(wrong_quest_by_date: dict, today: str, table_1: int, table_2: int) -> dict:
        """Saves the question as a session attribute.

        Currently using series of get statements?
        ## NOTE: May be able to use a while loop instead?? And keep going until 
        # either no value found or value is int?
        ## NOTE 2: Try-except may be best.
        """

        ## Get Dicts
        incorrect_today_dict = wrong_quest_by_date.get(today, {})
        tbl_1_incorrect_dict = incorrect_today_dict.get(table_1, {})
        tbl_2_val = tbl_1_incorrect_dict.get(table_2, 0)

        ## Val
        tbl_2_val += 1

        ## Update dicts
        tbl_1_incorrect_dict[table_2] = tbl_2_val
        incorrect_today_dict[table_1] = tbl_1_incorrect_dict
        wrong_quest_by_date[today] = incorrect_today_dict
        # print(wrong_quest_by_date)
        return wrong_quest_by_date


wrong_quest_by_date = {}

today = "2020_05_24"
table_1, table_2 = 1, 2

dates = ("2020_05_24", "2020_05_25", "2020_05_26", "2020_05_26")

for date in dates:
    for i in range(10):
        for j in range(0, 10, 2):
            wrong_quest_by_date = WrongAnswer.record_wrong_question(wrong_quest_by_date, date, i, j)

pprint.pprint(wrong_quest_by_date)