"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 11:04:40
 * @modify date 2020-08-15 14:37:53
 * @desc [
    Handlers for the user profiles.
    - Create user profiles.

    NOTE: These handlers are incomplete. I need to create separate handlers for:
    - when creating first profile & pointer var next_handler == "create_profile"
    - when user wants to create a new profile
    - when user wants to switch between existing profiles

    Currently, all bundled up into a single handler that creates a new user profile. 
    Need to refactor code & create personalized responses for each scenario. 
    This will also make it easier to record metrics.
 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import logger
from user_profile.user_profile_utils import UserProfileUtils
from players.players_dict import PlayerDict
from slots.slot_utils import SlotUtils
from helper.help_utils import HelpUtils
from pause.pauser import Pauser
from exceptions.exception_utils import ExceptionUtils
from answer_response.confirmation_utils import ConfirmUtils
from skill_card.card_funcs import CardFuncs
from pause.pauser import Pauser
from aux_utils.create_tuple_message_clauses import get_linear_nlg


##########
# CreateProfileHandlers
##########

class CreateUserProfileHandler(AbstractRequestHandler):
    def can_handle(self, handler_input) -> bool:
        attr = handler_input.attributes_manager.session_attributes
        return (
            is_intent_name("UserNameIntent")(handler_input) or 
            is_intent_name("CreateProfileIntent")(handler_input) or
            attr.get('next_handler', None) == 'create_profile'
        )
    
    def handle(self, handler_input):
        logger.info("HAN    CreateUserProfileHandler")

        user_name = SlotUtils.get_first_slot_value(handler_input)
        if not user_name:
            logger.info("HAN    RetryUserName")
            ms_welcome = UserProfileUtils.get_ms_welcome(handler_input)
            ms_retry_name = UserProfileUtils.get_ms_did_not_hear_name()

            prompt, reprompt = (
                UserProfileUtils.get_q_retry_name() for _ in range(2))
            prompt = CardFuncs.format_prompt(prompt)

            speech_list = (
                ms_welcome, 
                0.5,
                ms_retry_name,
                1.75,
                prompt
            )
        else:
            logger.info("HAN    CreatedProfile")
            UserProfileUtils.set_sesh_attr(handler_input, user_name)
            PlayerDict.create_new_player(handler_input, user_name)
            
            ms_confirm = ConfirmUtils.get_player_confirmation(handler_input)
            ms_created_first_profile = UserProfileUtils.get_ms_created_first_profile(handler_input)
        
            ms_overview = HelpUtils.get_ms_act_descript()
            prompt, reprompt = (
                HelpUtils.get_q_what_todo() for _ in range(2))
            prompt = CardFuncs.format_prompt(prompt)

            speech_list = (
                ms_confirm, 
                1,
                ms_created_first_profile,
                3,
                ms_overview,
                2.25,
                prompt
            )
        
        speech = get_linear_nlg(speech_list)
        card_title, card_text = CardFuncs.get_card_info(handler_input, speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

