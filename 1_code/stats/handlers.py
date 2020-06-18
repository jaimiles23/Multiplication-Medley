"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-20 13:17:50
 * @modify date 2020-05-23 00:35:49
 * @desc [
    Handlers for mode statistics.
    - ModeStatsHandler

    TODO: Consider refactoring this into differnet handlers??


 ]
 */
"""

##########
# Imports
##########

from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name
from ask_sdk_model import ui, Response
from ask_sdk_model.ui import SimpleCard

from logs import logger, log_func_name
from pause.pauser import Pauser
from answer_response.confirmation_utils import ConfirmUtils
from slots.slot_utils import SlotUtils
from skill_card.card_funcs import CardFuncs
from aux_utils.last_prompt import LastPrompt
from helper.help_utils import HelpUtils
from aux_utils.create_tuple_message_clauses import get_ms_from_tuple
from players.players_dict import PlayerDict
from stats.mode_speech_utils import ModeSpeech

import speed_challenge.data


##########
# Imports
##########

class ModeStatsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("ModeStatsIntent")(handler_input)
    
    def handle(self, handler_input):
        logger.info("HAN    ModeStatsHandler")
        attr = handler_input.attributes_manager.session_attributes
        speech_list = []
        player_obj = PlayerDict.load_player_obj(handler_input)

        mode = attr.get('mode', None)
        activity = SlotUtils.get_resolved_value(handler_input, 'activity')
        activity = activity if activity else mode
        difficulty = True
        
        if activity == 'survival':
            speech_list += ModeSpeech.get_ms_sm_stats(player_obj, activity)
            
        elif activity == 'speed':
            difficulty = SlotUtils.get_resolved_value(handler_input, 'difficulty')
            sc_difficulty = difficulty if difficulty else attr.get('sc_difficulty', None)
            
            if (difficulty in speed_challenge.data.SC_DIFFICULTIES):
                speech_list += ModeSpeech.get_ms_sc_stats(player_obj, sc_difficulty, activity)
            else:
                reprompt = ModeSpeech.get_ms_sc_what_difficulty()
                speech_list += reprompt
                reprompt = get_ms_from_tuple(reprompt)

        else:
            ms_can_tell_record = ModeSpeech.get_ms_can_tell_record()
            ms_example_saying = ModeSpeech.get_example_hear_records()
            speech_list = [ms_can_tell_record, 2, ms_example_saying]
            
            reprompt = HelpUtils.get_q_what_todo()

        if activity in ('survival', 'speed') and (difficulty):
            prompt, reprompt = (
                LastPrompt.get_last_prompt(handler_input) for _ in range(2))
            speech_list += Pauser.make_ms_pause_level_list( 3, prompt)
        

        speech = get_ms_from_tuple(speech_list)
        card_title = CardFuncs.get_card_title(handler_input)
        card_text = CardFuncs.clean_card_text(speech)
        return (
            handler_input.response_builder
                .speak(speech)
                .ask(reprompt)
                .set_card( SimpleCard( card_title, card_text))
                .response)

