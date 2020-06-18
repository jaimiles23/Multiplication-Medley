"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-21 20:18:23
 * @modify date 2020-05-21 20:18:23
 * @desc [
    Unit tests for Speed Challenge question generation.

    Generates questions uses random.sample. HOWEVER, to control distribution of sample, favored to sample numbers ABOVE 
    the times table, up until no more numbers can be sampled there.
 ]
 */
 """
import random


class SC_Questions(object):

    @staticmethod
    def generate_questions() -> list:
        """Generates list of questions to ask user in speed challenge."""
        lower_table, upper_table = 0, 10
        num_questions = 3
        table_questions = list()

        for table in range(lower_table, upper_table + 1):
            # print("*" * 10, table)
            lower_range = range(lower_table, table + 1)
            upper_range = range(table + 1, upper_table + 1)

            rand_num = random.randint(0, int( (table - lower_table) / 2))
            rand_num = rand_num if rand_num <= num_questions else num_questions

            num_upp_q = num_questions - rand_num
            num_low_q = rand_num

            # print(f"num_upp_q   {num_upp_q}")
            # print(f"num_low_q   {num_low_q}")

            if num_upp_q > len(upper_range):
                # print(f"num_upp_q   {num_upp_q}")
                # print(f"len(upper_range)    {len(upper_range)}")
                difference = num_upp_q - len(upper_range)

                num_upp_q -= difference
                num_low_q += difference

            if num_low_q > len(lower_range):
                # print(f"num_low_q   {num_low_q}")
                # print(f"len(lower_range)    {len(lower_range)}")
                difference = num_low_q - len(lower_range)

                num_low_q -= difference
                num_upp_q += difference
            
            
            # print(lower_range, num_low_q)
            # print(upper_range, num_upp_q)
            lower_questions = random.sample( lower_range, num_low_q)
            upper_questions = random.sample( upper_range, num_upp_q)

            table_questions.append(lower_questions)
            table_questions.append(upper_questions)
        
        sc_questions = list()
        times_table = lower_table
        # print(table_questions)

        for i in range(len(table_questions)):
            for table in table_questions[i]:
                sc_questions.append( (times_table, table))
                # print(table, (times_table, table))
            
            times_table = int((i + 1) / 2) + lower_table

        print(sc_questions)
        print(len(sc_questions))



            
            







for i in range(1):
    SC_Questions.generate_questions()

