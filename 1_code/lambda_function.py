"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 16:01:37
 * @modify date 2020-08-15 13:10:50
 * @desc [
    Lambda function & Handler for Multiplication Medley skill.
    - Sets up S3 adapter
    - Imports handlers and interceptors
    - Adds request handlers to lambda function.

    NOTE: Handler's can_handle logic is checked sequentially. Thus, the order
    that request_handlers are added to the skill builder is important. 
    e.g., FallbackHandler must be added last. 
    There are similar order restrictions within skill activities.
]*/
"""


##########
# Imports
##########

import os

import boto3
from ask_sdk_core.skill_builder import CustomSkillBuilder, SkillBuilder
from ask_sdk_s3.adapter import S3Adapter


##########
# S3 adapter setup
##########

skill_s3_client = boto3.client('s3')
skill_bucket_name = os.environ['bucket_name']
skill_prefix = "users/"

skill_s3_adapter = S3Adapter(
    bucket_name = skill_bucket_name,
    path_prefix = skill_prefix,
    s3_client = skill_s3_client,
)


##########
# Imports
##########

from interceptors.cache_prompt import CacheRepromptInterceptor
from interceptors.cache_response_int import CacheResponseForRepeatInterceptor
from interceptors.launch_intercept import LaunchRequestInterceptor

from exit_skill.handler import ExitHandler, SessionEndedRequestHandler, StopActivity
from fallback.handler import FallbackHandler
from helper.handler import HelpHandler
from launch.handlers import LaunchRequestHandler
from repeat.handler import RepeatHandler

from user_profile.handlers import CreateUserProfileHandler
from act_descriptions.handlers import ActDescriptHandler
from stats.handlers import ModeStatsHandler

from free_play.handlers import (
    FP_StartHandler,
    FP_SetTimesTablesHandler,
    FP_AddTimesTablesHandler,
    FP_SetNumberQuestionsHandler,
    FP_SetTableBoundsHandler,
    FP_ParametersHandler,
    FP_CorrectAnswerHandler,
    FP_WrongAnswerHandler,
    FP_AnsweredRequestedQuestionsHandler,
)
from custom_practice.handlers import (
    CP_StartHandler,
    CP_CorrectAnswerHandler,
    CP_WrongAnswerHandler,
    CP_NextPracticeHandler,
)
from survival_mode.handlers import (
    SM_StartHandler,
    SM_CorrectAnswerHandler,
    SM_WrongAnswerHandler,
)
from speed_challenge.handlers import (
    SC_StartHandler, 
    SC_DifficultySetupHandler,
    SC_CorrectAnswerHandler ,
    SC_WrongAnswerHandler,
    SC_FinishedChallengeHandler,
)

from no_handler.handlers import NoHandler

from check_answer.handlers import GetAnswerHandler

from mult_questions.handlers import NumQuestionsAnsweredHandler



##########
# Request Handlers
##########

SKILL_REQUEST_HANDLERS = (
    ## Standard Handlers
    LaunchRequestHandler,
    HelpHandler,
    RepeatHandler,
    ExitHandler,
    SessionEndedRequestHandler,
    
    ## User Profle
    CreateUserProfileHandler,

    ## Aux
    ActDescriptHandler,
    ModeStatsHandler,
    StopActivity,
    NoHandler,
    
    ## FP
    FP_StartHandler,
    FP_SetTimesTablesHandler,
    FP_AddTimesTablesHandler,
    FP_SetNumberQuestionsHandler,
    FP_SetTableBoundsHandler,
    FP_ParametersHandler,
    FP_AnsweredRequestedQuestionsHandler,
    FP_AnswerQuestionHandler,

    ## CP
    CP_StartHandler,
    CP_NextPracticeHandler,
    CP_CorrectAnswerHandler,
    CP_WrongAnswerHandler,

    ## SM
    SM_StartHandler,
    SM_CorrectAnswerHandler,
    SM_WrongAnswerHandler,

    ## SC 
    SC_StartHandler, 
    SC_DifficultySetupHandler,
    SC_FinishedChallengeHandler,
    SC_CorrectAnswerHandler,
    SC_WrongAnswerHandler,

    ## Gen Questions & Answered
    GetAnswerHandler,
    NumQuestionsAnsweredHandler,

    ## Always True
    FallbackHandler,
    
)


sb = CustomSkillBuilder( persistence_adapter = skill_s3_adapter)

for req_handler in SKILL_REQUEST_HANDLERS:
    sb.add_request_handler( req_handler())


##########  
# Interceptors
##########

sb.add_global_request_interceptor( LaunchRequestInterceptor())

sb.add_global_response_interceptor( CacheResponseForRepeatInterceptor())
sb.add_global_response_interceptor( CacheRepromptInterceptor())


##########
# Finalize
##########

lambda_handler = sb.lambda_handler()

