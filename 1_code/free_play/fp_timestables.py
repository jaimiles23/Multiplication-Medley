"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-11 12:00:22
 * @modify date 2020-05-17 16:45:17
 * @desc [
     FPTimesTables utility class. Methods for:
     - existing tables
     - Query & Range times tables
     - Utility speech method
     - Times table input
     - Add times tables
 ]
 */
"""

##########
# Imports
##########

import random


from logs import log_func_name, logger
from slots.slot_utils import SlotUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from aux_utils.list_to_speech import get_str_from_list
from aux_utils.try_saying import get_ms_try_saying
from pause.pauser import Pauser

import free_play.data
from aux_data.SSML_tags import (
    MW_EXCITED_LOW, 
    MW_SLOW1, MW_SLOW2, MW_SLOW3
)


##########
# FPTimesTablesUtils
##########

class FPTimesTables(object):

    ##########
    # Use Existing Tables
    ##########
    @staticmethod
    @log_func_name
    def get_ms_use_existing_tables(handler_input) -> str:
        """Returns message that will use existing tables.

        Incase the user sets the parameters before entering Free Play mode."""
        attr = handler_input.attributes_manager.session_attributes

        times_tables = attr['times_tables']
        times_tables_to_use = get_str_from_list(times_tables)

        speech_list = (
            free_play.data.MTT_EXISTING_TABLES,
            times_tables_to_use
        )
        return get_ms_from_tuple(speech_list)
        

    ##########
    # Times Tables -- Query & Range.
    ##########
    @staticmethod
    @log_func_name
    def get_ms_using_tables_from_input(lower_table, upper_table, times_tables):
        """Returns message on what tables will be used. 

        If lower & upper, calls use_table_range. 
        Elif times_tables, uses queried tables.
        Else, only 1 table registered & uses it as table.
        """
        if (lower_table is not None) and upper_table:
            return FPTimesTables.get_ms_use_table_range(lower_table, upper_table)
        
        elif times_tables:
            return FPTimesTables.get_ms_use_query_times_tables(times_tables)
        
        logger.error(f"get_ms_using_tables_from_input: end reached")
        return ''


    @staticmethod
    @log_func_name
    def get_ms_use_table_range(lower_table: int, upper_table: int) -> str:
        """Returns message that will use table range."""
        ms_use_problems = FPTimesTables.get_ms_use_problems_start()
        ms_table_range = (
            random.choice(free_play.data.MT_TABLE_RANGE).format(
                lower_table, upper_table))
        
        speech_list = (
            ms_use_problems,
            free_play.data.MS_BETWEEN,
            ms_table_range)
        return ' '.join(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_use_query_times_tables(times_tables: list) -> str:
        """Returns message that will use queried times tables."""
        ms_use_problems = FPTimesTables.get_ms_use_problems_start()
        times_tables = get_str_from_list(times_tables)

        speech_list = (
            ms_use_problems,
            free_play.data.MS_FROM,
            free_play.data.MT_USE_TABLES,
            Pauser.get_p_level(1),
            times_tables,
        )
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_potential_mistake_parsing_query() -> str:
        """Returns message that may have made mistake parsing query_tables.

        Called when likely parsed query_tables incorrectly."""
        speech_list = (
            free_play.data.MMT_MISTAKE_PARSING,
        )
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_can_retry_query_format() -> str:
        """Returns message that can re-input query tables."""
        speech_list = (
            free_play.data.MMT_WRONG,
            1.5,
            "For example,",
            get_ms_try_saying(),
            0.75,
            FPTimesTables.get_example_tables_query(),
        )
        return get_ms_from_tuple(speech_list)


    ##########
    # Utility speech method
    ##########
    @staticmethod
    @log_func_name
    def get_ms_use_problems_start() -> str:
        """Returns initial message about what problems to use.

        e.g.,
            "I'll ask questions from."
        """
        return get_ms_from_tuple( free_play.data.MMT_USE_PROBLEMS_START)


    ##########
    # Times Tables input
    ##########
    @staticmethod
    @log_func_name
    def get_q_times_tables_input() -> str:
        """Returns prompt asking what times tables to practice.
        
        NOTE: Should add handler_input so can change example b/w prompt & reprompt,
        and depending on num logins, etc.
        """
        q_what_tables = get_ms_from_tuple( free_play.data.MMT_WHAT_TABLES_PRACTICE)
        if random.random() < 0.0:       ## TODO: Change chance of prompt.
            ms_example = FPTimesTables.get_example_tables_query()
        else:
            ms_example = FPTimesTables.get_example_table_range()
        
        speech_list =  (
            q_what_tables, 
            Pauser.get_p_level(2),
            get_ms_try_saying(),
            Pauser.get_p_level(0.75),
            ms_example)
        speech = ' '.join(speech_list)
        return MW_SLOW1.format(speech)


    @staticmethod
    @log_func_name
    def get_example_tables_query() -> str:
        """Returns example of providing for times tables query."""
        speech_list = list(free_play.data.MMT_QUERY_TABLES_SETUP)
        
        random_tables = set()
        while len(random_tables) < 3:
            rand_num = random.randint(2, 10)
            random_tables.add(str(rand_num))

        random_tables = list(random_tables)
        random_tables.sort()

        sample_tables = ', and '.join(random_tables) + '.'
        sample_tables = MW_SLOW3.format(sample_tables)

        speech_list += Pauser.make_ms_pause_level_list(1, sample_tables)
        return MW_SLOW1.format( get_ms_from_tuple( speech_list))


    @staticmethod
    @log_func_name
    def get_example_table_range() -> str:
        """Returns example of providing times table range."""
        # ms_start_table_req = random.choice( free_play.data.MT_START_TABLE_REQUEST)
        low_table, upper_table = random.randint(0, 5), random.randint(6, 10)
        ms_range = random.choice( free_play.data.MT_RANGE_TABLES).format(
            low_table, upper_table)
        
        speech_list = (
            # ms_start_table_req,
            # free_play.data.MT_FROM,
            free_play.data.MS_USE,
            free_play.data.MT_TIMES_TABLES,
            ms_range,
        )
        return get_ms_from_tuple(speech_list)


    ##########
    # Add Times Tables
    ##########
    @staticmethod
    @log_func_name
    def get_ms_added_tables(tables_query: list) -> str:
        """Confirms message that added tables to message list."""
        ms_tables = 'tables' if len(tables_query) > 1 else 'table'
        ms_added_tables = get_str_from_list(tables_query, punct= False)

        speech_list = (
            free_play.data.MT_INCLUDING_TABLES,
            ms_added_tables,
            ms_tables,
            free_play.data.MT_TO_PRACTICE
        )
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_can_add_tables() -> str:
        """Returns message that can add tables."""
        ms_can_add_tables = get_ms_from_tuple(free_play.data.MMT_CAN_ADD_TIMES_TABLES)
        ms_add_table_example = FPTimesTables.get_ms_add_table_example()

        speech_list = (
            ms_can_add_tables,
            2,
            ms_add_table_example)
        return get_ms_from_tuple(speech_list)


    @staticmethod
    @log_func_name
    def get_ms_add_table_example() -> str:
        """Returns example of how to add tables"""
        random_nums = set()
        while len(random_nums) != 3:
            num = random.randint(0, 10)
            if num not in random_nums:
                random_nums.add(str(num))
        
        speech_list = (
            get_ms_try_saying(),
            get_ms_from_tuple(free_play.data.MMT_EXAMPLE_ADD_TIMES_TABLES),
            ' and '.join(random_nums),
        )
        return ' '.join(speech_list)

