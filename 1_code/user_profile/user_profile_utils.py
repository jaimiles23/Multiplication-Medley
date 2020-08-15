"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 11:04:40
 * @modify date 2020-05-22 22:04:49
 * @desc [
    UserProfileUtils class for methods on creating a user profile
    - General
    - Input Again
    - Welcome

    NOTE: Refernces creating first profile. Should distinguish between first and other profiles.
 ]
 */
"""

##########
# Imports
##########

import random

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, is_request_type


from logs import log_func_name, logger
from pause.pauser import Pauser
from aux_utils.create_tuple_message_clauses import get_linear_nlg
from launch.launch_utils import LaunchUtils

import user_profile.data


##########
# NewProfileUtils
##########
class UserProfileUtils(object):
   
   @staticmethod
   @log_func_name
   def set_sesh_attr(handler_input, player_name: str):
      """Sets the session attributes after creating the User Profile."""
      attr = handler_input.attributes_manager.session_attributes
      attr['current_player'] = player_name
      attr['next_handler'] = None
      attr['help_pointer'] = 'overview'
      return


   @staticmethod
   @log_func_name
   def get_ms_created_first_profile(handler_input) -> str:
      """Returns message that created a profile.

      NOTE: User name included in handler confirmation."""
      return user_profile.data.MS_FIRST_PROFILE


   ##########
   # Input again
   ##########

   @staticmethod
   @log_func_name
   def get_ms_did_not_hear_name() -> str:
      """Returns message did not register name input and needs to retry."""
      return get_linear_nlg(
         user_profile.data.MMT_RETRY_USER_NAME)
   

   @staticmethod
   @log_func_name
   def get_q_retry_name() -> str:
      """Returns message asking for the user name."""
      return random.choice(
         user_profile.data.MT_WHAT_NAME)
   
   ##########
   # Welcome Utils
   ##########
   @staticmethod
   @log_func_name
   def get_ms_welcome(handler_input) -> str:
      """Returns welcome message if LaunchRequest."""
      if is_request_type("LaunchRequest")(handler_input):
         return LaunchUtils.get_q_player_name()
      
      else:
         return ''


