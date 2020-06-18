"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-07 23:09:05
 * @modify date 2020-05-20 20:48:04
 * @desc [
   FreePlayAttr class with methods for attributes:
   - Free Play mode
   - Slot setup
   - Num questions
   - Table bounds
   - Free play parameters
   - End free play
   - Player attr.
 ]
 */
"""

##########
# Imports
##########

from logs import log_func_name, logger
from slots.slot_utils import SlotUtils
from players.players_dict import PlayerDict

from free_play.fp_clean_input import FPCleanInput
import free_play.data


##########
# FreePlayAttr Utility Class
##########

class FreePlayAttr(object):

   ##########
   # Free Play Mode
   ##########
   @staticmethod
   @log_func_name
   def set_attr_free_play(handler_input):
      """Sets attributes for free play mode."""
      attr = handler_input.attributes_manager.session_attributes
      attr['mode'] = 'free_play'
      attr['help_pointer'] = 'fp_input'
      attr['inform_query_tables_format'] = False
      attr['questions_answered'] = 0
      return


   @staticmethod
   @log_func_name
   def reset_attr_query_format(handler_input):
      """Sets sesh attr inform_query_tables_format to False"""
      attr = handler_input.attributes_manager.session_attributes
      attr['inform_query_tables_format'] = False


   ##########
   # Setup Slots
   ##########
   @staticmethod
   @log_func_name
   def get_times_table_input_slots(handler_input) -> tuple:
      """Gets times table attributes:
         - lower_table
         - upper_table
         - table_query
      """
      lower_table, upper_table, query_tables = (
         SlotUtils.get_slot_val_by_name(handler_input, slot_name) for slot_name in 
            free_play.data.TIMES_TABLE_SLOTS)
      
      query_tables = FPCleanInput.clean_query_tables(handler_input, query_tables)
      lower_table, upper_table = FPCleanInput.clean_table_range(lower_table, upper_table)
      return (lower_table, upper_table, query_tables)


   @staticmethod
   @log_func_name
   def set_attr_times_tables(
      handler_input,
      lower_table: int, 
      upper_table: int, 
      table_query: list,
   ):
      """Sets setup slots as times_tables sesh attr for Free Play."""
      attr = handler_input.attributes_manager.session_attributes
      times_tables = FreePlayAttr.construct_attr_times_tables_from_input(
         lower_table, upper_table, table_query)

      attr['times_tables'] = times_tables
      return


   @staticmethod
   @log_func_name
   def add_to_attr_times_tables(
      handler_input,
      lower_table: int,
      upper_table: int,
      table_query: list,
   ) -> None:
      """Adds to the current times tables session attributes."""
      attr = handler_input.attributes_manager.session_attributes
      new_times_tables = FreePlayAttr.construct_attr_times_tables_from_input(
         lower_table, upper_table, table_query)

      times_tables = attr.get('times_tables', [])
      times_tables += new_times_tables
      times_tables = list(set(times_tables))
      attr['times_tables'] = times_tables
      return
   
   
   @staticmethod
   @log_func_name
   def construct_attr_times_tables_from_input(
      lower_table: int,
      upper_table: int,
      table_query: list,
   ):
      times_tables = []

      logger.debug(lower_table)
      logger.debug(upper_table)
      logger.debug(table_query)

      if lower_table is not None and upper_table is not None:
         for i in range(int(lower_table), int(upper_table) + 1):
            times_tables.append(i)

      elif lower_table is not None:
         times_tables.append( int(lower_table))

      elif upper_table is not None:
         times_tables.append( int(upper_table))

      elif table_query is not None:
         for table in table_query:
            times_tables.append( int(table))

      return times_tables


   ##########
   # Num questions
   ##########
   @staticmethod
   @log_func_name
   def set_attr_num_questions(handler_input, num_questions: int):
      """Sets session attribute for number of questions"""
      attr = handler_input.attributes_manager.session_attributes
      attr['num_questions'] = num_questions
      return


   ##########
   # Table Bounds
   ##########

   @staticmethod
   @log_func_name
   def get_table_bound_slots(handler_input) -> tuple:
      """Returns tuple of slots for lower & upper bounds."""
      lower_bound = SlotUtils.get_slot_val_by_name(handler_input, "lower_bound")
      upper_bound = SlotUtils.get_slot_val_by_name(handler_input, "upper_bound")
      
      if (lower_bound is not None) and (upper_bound is not None):
         lower_bound, upper_bound = sorted([int(lower_bound), int(upper_bound)])
      return (lower_bound, upper_bound)


   @staticmethod
   @log_func_name
   def set_table_bounds(handler_input, lower_bound: int, upper_bound: int) -> str:
      """Sets lower and upper table ranges for multiplication questions."""
      attr = handler_input.attributes_manager.session_attributes

      if lower_bound is not None:
         attr['lower_bound'] = lower_bound
      if upper_bound is not None:
         attr['upper_bound'] = upper_bound
      return
   

   ##########
   # FreePlay parameters
   ##########
   @staticmethod
   @log_func_name
   def get_fp_parameters(handler_input) -> dict:
      """Returns dict of the user specified free play parameters."""
      attr = handler_input.attributes_manager.session_attributes

      fp_param_dict = dict()
      for key in free_play.data.FP_PARAMS:
         fp_param_dict[key] = attr.get(key, None)
      
      return fp_param_dict


   ##########
   # End Free play
   ##########
   @staticmethod
   @log_func_name
   def set_attr_end_fp(handler_input) -> None:
      """Sets attributes when ending fp session."""
      attr = handler_input.attributes_manager.session_attributes
      reset_attrs = (
         'mode',

         'times_tables',
         'num_questions',
         'lower_bound',
         'upper_bound',

         'question',
         'questions_answered',
         'consecutive_correct',
         'consecutive_incorrect',
      )
      for reset_at in reset_attrs:
         attr[reset_at] = 0
      
      FreePlayAttr.increment_fp_plays(handler_input)
      return


   ##########
   # Player Attr
   ##########
   @staticmethod
   @log_func_name
   def increment_fp_plays(handler_input, player_obj: object = None) -> None:
      """Increments fp_plays for player."""
      if not player_obj:
         player_obj = PlayerDict.load_player_obj(handler_input)

      player_obj.fp_plays += 1
      PlayerDict.save_player_obj(handler_input, player_obj)
      return

