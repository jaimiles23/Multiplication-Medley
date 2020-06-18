"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-13 12:16:03
 * @modify date 2020-05-16 15:46:00
 * @desc [
    FPCleanInput class to clean user slot input:
    - Query
    - Range
 ]
 */
"""

##########
# Imports
##########

from logs import logger, log_func_name


##########
# FPCleanInput utility class
##########

class FPCleanInput(object):

    @staticmethod
    @log_func_name
    def clean_query_tables(handler_input, query_tables: str) -> list:
        """Returns cleaned list of query tables.

        Only keeps input that can converted to an integer."""
        if query_tables is None:
            return None

        times_tables = []
        conjunctions = set()
        conjunctions.add("and")
        conjunction_count = 0
        query_tables_split = query_tables.split()
        
        for word in query_tables_split:
            try:
                times_table = int(word)
                times_tables.append(times_table)
            except ValueError:
                logger.debug(word)
                if word in conjunctions:
                    conjunction_count += 1
        
        # logger.debug( query_tables_split)
        # logger.debug( times_tables)
        # logger.debug( conjunction_count)
        # logger.debug( conjunction_count < len(query_tables) // 3)
        # logger.debug( len(query_tables) > 2)
        # logger.debug( len(times_tables) < len(query_tables) // 2)
        # logger.debug( len( str( max( times_tables))) > 2)

        parsed_incorrectly = (
            (
                conjunction_count < len(query_tables_split) // 3 and      # Low (f)
                len(query_tables_split) > 2 and
                len(times_tables) < len(query_tables_split) // 2
                    # check that more times tables than half length of query_tables
            ) or
            (
                len( str( max( times_tables))) > 2
            )
        )
        if parsed_incorrectly:
            handler_input.attributes_manager.session_attributes['inform_query_tables_format'] = True

        return times_tables


    @staticmethod
    @log_func_name
    def incorrect_query_tables_parse(handler_input, query_tables: str, times_tables: list):
        """Controls attributes & logs when likely wrong parsing for query tables."""
        attr = handler_input.attributes_manager.session_attributes
        attr['inform_query_tables_format'] = True

        logger.warning(f"query tables:   {query_tables}")
        logger.warning(f"times tables:   {times_tables}")
        return


    @staticmethod
    @log_func_name
    def clean_table_range(lower_table: int, upper_table: int) -> tuple:
        """Auxiliary function to differentiate lower & upper table.

        During input, may register lower & upper table as single number,
        e.g., 2 & 9 --> 29. This separates the two numbers and returns.
        NOTE: Assumes lower table will always be single digit.
        """
        if lower_table is None and upper_table is None:
            return None, None
        
        elif (lower_table is None) and len(str(upper_table)) > 1:
            lower_table, upper_table = str(upper_table)[0], str(upper_table)[1:]

        elif (upper_table is None) and len(str(lower_table)) > 1:
            lower_table, upper_table = str(lower_table)[0], str(lower_table)[1:]
        
        lower_table, upper_table = sorted([int(lower_table), int(upper_table)])
        return str(lower_table), str(upper_table)

        
