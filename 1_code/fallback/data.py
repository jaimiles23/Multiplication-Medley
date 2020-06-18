"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-05 13:56:45
 * @modify date 2020-05-05 13:56:45
 * @desc [
     Data module for the fallback handler.
 ]
 */
"""

##########
# Standard Fallback
##########


MS_FALLBACK = "I can't help you with that right now."


##########
# Did not understand answer
##########
"Sorry, I didn't catch your answer. Can you please try again."

MT_SORRY = (
    "Sorry,",
    "Sorry,",
    "I'm sorry,",
    "",
    "",
)
MT_DID_NOT_REGISTER_SLOT = (
    "I didn't catch that.",
    "I didn't get your answer.",
    "I didn't quite hear you.",
)
MT_TRY_AGAIN = (
    "Please try again.",
    "Please retry.",

    "Can you please try again?",
    "Can you please retry?",
)
MMT_NOT_UNDERSTAND = (
    MT_SORRY,
    MT_DID_NOT_REGISTER_SLOT,
    MT_TRY_AGAIN,
)

