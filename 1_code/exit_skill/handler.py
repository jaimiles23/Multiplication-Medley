"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 14:14:31
 * @modify date 2020-05-26 10:05:18
 * @desc [
     Handlers for exiting the skill:
     - Exit
     - SessionEnded
     - StopActivity (to stop a specific activity).
]
*/"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler

from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard


from logs import logger, log_func_name
from exit_skill.exit_utils import ExitUtils
from skill_card.card_funcs import CardFuncs
from answer_response.confirmation_utils import ConfirmUtils
from helper.help_utils import HelpUtils
from pause.pauser import Pauser
from stats.mode_stats import ModeStats
from players.players_dict import PlayerDict

from free_play.fp_attr import FreePlayAttr
from survival_mode.survival_attr import SM_Attr
from speed_challenge.sc_attr import SC_Attr

import aux_data.skill_data


##########
# Exit
##########

class ExitHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (HandlerInput) -> bool
        return (
            is_intent_name("AMAZON.CancelIntent")(handler_input) or 
            is_intent_name("AMAZON.StopIntent")(handler_input) or 
            is_intent_name("AMAZON.PauseIntent")(handler_input)
        )

    def handle(self, handler_input):
        # type (HandlerInput) -> Response
        logger.info("HAN    ExitIntentHandler")
        speech_list = []

        player_obj = PlayerDict.load_player_obj(handler_input)

        ## TODO: Implement sesh performance func.
        ms_session_performance = ExitUtils.get_ms_session_performance(handler_input)
        ms_exit = ExitUtils.get_ms_exit_game()

        speech_list.append( ms_session_performance)
        speech_list.append( ms_exit)

        speech = ' '.join( speech_list)
        card_title = CardFuncs.get_card_title( handler_input)
        card_text = CardFuncs.clean_card_text( speech)

        ## Attr management @ very end.
        ExitUtils.update_player_mode_statistics(handler_input, player_obj)
        PlayerDict.save_player_obj(handler_input, player_obj)
        
        ExitUtils.exit_skill_attr_management(handler_input)
        return (
            handler_input.response_builder
                .speak(speech)
                .set_card( SimpleCard(
                    card_title, card_text))
                .set_should_end_session(True)
                .response)


##########
# SessionEnded
##########

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type (handlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info(f"SessionEndedRequest:   {handler_input.request_envelope.request.reason}")

        player_obj = PlayerDict.load_player_obj(handler_input)
        ExitUtils.update_player_mode_statistics(handler_input, player_obj)
        PlayerDict.save_player_obj(handler_input, player_obj)

        ExitUtils.exit_skill_attr_management(handler_input)

        return handler_input.response_builder.response


##########
# Stop Activity
##########

class StopActivity(AbstractRequestHandler):
    def can_handle(self, handler_input):
        attr = handler_input.attributes_manager.session_attributes
        return (
            is_intent_name("StopActivityIntent")(handler_input) and 
            (attr.get('mode', None) in aux_data.skill_data.MODE_ACT_DICT.keys())
            )
      
    def handle(self, handler_input):
        speech_list = []
        
        ms_confirm = ConfirmUtils.get_random_confirmation(handler_input)
        prompt, reprompt = (
            HelpUtils.get_q_what_todo() for _ in range(2))
        
        speech_list += Pauser.make_ms_pause_level_list(
            ms_confirm, 2, prompt)

        ModeStats.translate_mode_stats_to_sesh(handler_input)

        ## Set end all attr
        FreePlayAttr.set_attr_end_fp(handler_input)
        SM_Attr.set_attr_end_survival_mode(handler_input)
        SC_Attr.set_attr_end_sc(handler_input)
        
        speech = ' '.join(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)
        return (
            handler_input.response_builder
            .speak(speech)
            .ask(reprompt)
            .set_card( SimpleCard( card_title, card_text))
            .response)