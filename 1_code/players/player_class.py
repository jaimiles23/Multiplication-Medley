"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 17:34:05
 * @modify date 2020-05-27 10:20:01
 * @desc [
   Player class to track statistics. Utility methods for:
   - Track answers
   - Survival Mode statistics
   - Speed Challenge statistics
   - Average Table statistics
   - Times Tables information
   - Utility methods 
]
*/
"""

##########
# Imports
##########

from statistics import mean

from logs import logger, log_func_name, log_all
import players.data
import speed_challenge.data


##########
# Player class
##########

class Player(object):
   """Player object to track player's statistics."""
   
   @log_func_name
   def __init__(
      self,
      name: str,
      total_correct: int = 0,
      total_incorrect: int = 0,
      answered_tables: list = [],
      times_tables_info: dict = {},

      fp_plays: int = 0,
      cp_plays: int = 0,

      sm_plays: int = 0,
      sm_high_score: int = 0,
      sm_average_records: list = [],

      sc_plays: int = 0,
      sc_high_score_dict: dict = {},
      sc_average_record_dict = {},

   ):
      self.name = name
      self._total_correct = total_correct
      self._total_incorrect = total_incorrect
      self._answered_tables = answered_tables
      self._times_tables_info = times_tables_info

      self.fp_plays = fp_plays
      self.cp_plays = cp_plays

      self.sm_plays = sm_plays
      self._sm_high_score = sm_high_score
      self._sm_average_records = sm_average_records

      self.sc_plays = sc_plays
      self._sc_high_score_dict = sc_high_score_dict
      self._sc_average_record_dict = sc_average_record_dict


   ##########
   # Track Answers
   ##########
   @log_func_name
   def increment_answer_counter(self, correct: bool) -> None:
      """Increments correct/incorrect answer based correct boolean."""
      if correct:
         self._total_correct += 1
      else:
         self._total_incorrect += 1
      return


   @log_func_name
   def get_answered_questions(self) -> int:
      """Returns integer for the total number of questions user answered."""
      return (self._total_correct + self._total_incorrect)
   

   ##########
   # Survival Mode
   ##########
   @log_func_name
   def set_sm_high_score(self, high_score: int) -> None:
      """Sets the high score for survival mode."""
      self._sm_high_score = high_score
   

   @log_func_name
   def get_sm_high_score(self) -> int:
      """Returns sm highscore."""
      return self._sm_high_score


   @log_func_name
   def update_sm_records(self, sm_score: int) -> None:
      """Updates survival mode records."""
      sm_records = self._sm_average_records
      sm_records.append( sm_score)

      if len(sm_records) > players.data.ALLLOWED_AVG_RECORDS:
         del sm_records[0]
      self._sm_average_records = sm_records
   
   
   @log_func_name
   def get_sm_avg_records(self) -> str:
      """Returns survival mode records."""
      return self._sm_average_records
   

   ##########
   # Speed Challenge
   ##########
   @log_func_name
   def set_sc_high_score(self, difficulty: str, user_score: int) -> None:
      """Sets the highscore for speed challenge's difficulty."""
      sc_hs_dict = self._sc_high_score_dict
      log_all(sc_hs_dict)
      
      if difficulty not in sc_hs_dict.keys():
         sc_hs_dict[difficulty] = user_score
         self._sc_high_score_dict = sc_hs_dict
         return None

      high_score = sc_hs_dict[difficulty]
      if (user_score < high_score):
         sc_hs_dict[difficulty] = user_score
         self._sc_high_score_dict = sc_hs_dict
      
      return


   @log_func_name
   def get_sc_high_score(self, difficulty: str) -> int:
      """Returns the user's high score for the speed challenge difficulty.
      
      Returns None if no high score is found for that difficulty."""
      sc_hs_dict = self._sc_high_score_dict
      log_all(sc_hs_dict)
      return sc_hs_dict.get(difficulty, None)


   @log_func_name
   def update_sc_average_record(self, difficulty: str, user_score: int) -> None:
      """Updates the average records for speed challenge's difficulty."""
      sc_average_record_dict = self._sc_average_record_dict
      log_all(sc_average_record_dict)

      if difficulty not in sc_average_record_dict.keys():
         sc_average_record_dict[difficulty] = [user_score]
         self._sc_average_record_dict = sc_average_record_dict
         return None
      
      average_records = sc_average_record_dict[difficulty]
      average_records.append(user_score)

      if len(average_records) > players.data.ALLLOWED_AVG_RECORDS:
         del average_records[0]
      
      sc_average_record_dict[difficulty] = average_records
      self._sc_average_record_dict = sc_average_record_dict
      log_all(sc_average_record_dict)
      return None


   @log_func_name
   def get_sc_average_records(self, difficulty: str) -> list:
      """Returns list of average records for appropriate speed challenge difficulty."""
      sc_average_record_dict = self._sc_average_record_dict
      log_all(sc_average_record_dict)
      return sc_average_record_dict.get(difficulty, None)


   ##########
   # Average Table
   ##########
   @log_func_name
   def update_average_table(self, tables):
      """Updates the average table answered by the user.

      NOTE: Can make average tables a dict, one val of tables array, one val of mean.
      max_len = 100. If max_len, then can determine mean by subtracting 
      (first_val / 100) and adding (new_val / 100).
      May save computation time, O(2) instead of O(100) for mean.

      TODO: Rename the function - this is answered tables, not average tables
      """
      answered_tables = self._answered_tables
      tables = Player.check_not_duplicate_tables(tables)

      for table in tables:
         int_table = int(table)
         answered_tables.append(int_table)

      answered_tables = Player.enforce_allowed_answered_tables( answered_tables)
      self._answered_tables = answered_tables
      return
   

   @log_func_name
   def get_answered_tables(self, integers: bool = True):
      """Returns user tables.
      
      Optional intergers argument determines if the list is returned as ints.
      POST NOTE: Not sure why I included this?
      """
      if integers:
         answered_tables = [ int(table) for table in self._answered_tables]
      else:
         answered_tables = self._answered_tables
      return answered_tables


   ##########
   # Times Tables information
   ##########
   @log_func_name
   def get_times_table_info(self) -> dict:
      """Returns times_table_info dictionary."""
      return self._times_tables_info


   @log_func_name
   def update_times_tables_info_dict(self, tables: tuple, correct: bool):
      """Updates the times_table dict mean & correct/incorrect answer.
      
      Passes times tables (str, str). """
      times_tables_info = self._times_tables_info
      tables = Player.check_not_duplicate_tables(tables)

      for table in tables:
         table = str(table)      # dict keys saved as str in json?
         table_dict = times_tables_info.get(table, dict())

         log_all(table, table_dict)

         if table_dict == dict():
            table_dict = Player.init_times_table_dict(correct)
         else:
            table_dict = Player.get_updated_table_dict(table_dict, correct)
           
            
         times_tables_info[ table] = table_dict
      
      self._times_tables_info = times_tables_info


   ##########
   # Utility methods -- may like to create a separate class for this??
   ##########

   @staticmethod
   @log_func_name
   def check_not_duplicate_tables(tables: tuple) -> tuple:
      """Checks that two times tables are not duplicates.
      
      If duplicates, returns single table. Else returns tuple input."""
      table_1, table_2 = tables
      if table_1 == table_2:
         return [table_1]
      return tables


   @staticmethod
   @log_func_name
   def init_times_table_dict(correct: bool) -> dict:
      """Returns dictionary for initialized times table.
      
      Use mean instead of sum because can compare numbers with
      different data points."""
      table_dict = {
         'mean'         :  correct,
         'table_data'   :  [correct, ]
      }
      return table_dict


   @staticmethod
   @log_func_name
   def get_updated_table_dict(table_dict: dict, correct: bool) -> dict:
      """Returns updated times table dictionary.
      
      Adds data point, enforces allowed data points, and updates the mean."""
      table_data = table_dict['table_data']
      table_data.append(correct)
      table_data = Player.enforce_table_data_size(table_data)

      table_mean = mean(table_data)
      table_dict['mean'] = table_mean
      table_dict['table_data'] = table_data
      return table_dict


   @staticmethod
   @log_func_name
   def enforce_table_data_size(table_data: list) -> list:
      """Enforces the allowed length of the table data.

      If data exceeds the length of the allowed data, 
      removes excess elements."""
      table_overflow = len(table_data) - players.data.ALLOWED_TABLE_DATA
      if table_overflow <= 0:
         return table_data

      log_all(table_overflow, table_data)
      del table_data[0 : table_overflow]
      logger.debug(table_data)

      return table_data


   @staticmethod
   @log_func_name
   def enforce_allowed_answered_tables(answered_tables: list) -> list:
      """Enforces the allowed length of answered_tables."""
      table_overflow = len(answered_tables) - players.data.ALLOWED_ANSWERED_TABLES
      if table_overflow <= 0:
         return answered_tables
      
      log_all(table_overflow, answered_tables)
      del answered_tables[0 : table_overflow]
      logger.debug(answered_tables)
      return answered_tables

