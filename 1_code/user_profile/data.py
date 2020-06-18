"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 11:04:40
 * @modify date 2020-05-22 22:09:29
 * @desc [
    Data module for user profile. Data for:
    - new profile
    - general tuples

    TODO: Update doc
 ]
 */
"""

##########
# Imports
##########


##########
# New Profile
##########

MS_FIRST_PROFILE = "I created a user profile to track your progress."


##########
# General Tuples
##########

MT_APOLOGY = (
    "",
    "Sorry.",
    "I'm sorry."
)

MT_NOT_CATCH = (
    "I didn't",
    "I did not",
)

MT_REGISTER = (
    "hear",
    "get",
)

MS_YOUR_NAME = "your name."


MS_NEED_NAME = "I need your name"

MT_CREATE = (
    "to create",
    "to set up",
)

MT_USER_PROFILE = (
    "a user profile",
    "a profile",
)

MS_TRACK_DATA = "and track your progress."

MMT_RETRY_USER_NAME = (
   MT_APOLOGY,
   MT_NOT_CATCH,
   MT_REGISTER,
   MS_YOUR_NAME,
   1.5,
   MS_NEED_NAME,
   MT_CREATE,
   MT_USER_PROFILE,
   MS_TRACK_DATA,
)


MT_WHAT_NAME = (
   "What is your name?",
   "What's your name?",
   "Please tell me your name.",
)
