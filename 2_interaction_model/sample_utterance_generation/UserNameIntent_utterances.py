"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-06 10:59:24
 * @modify date 2020-05-06 10:59:24
 * @desc [
    Script to generate sample utterances for UserNameIntent.
 ]
 */
"""

##########
# Slots
##########

slots = (
    r"{first_name}",
    r"{us_first_name}",
    r"{gb_first_name}",
)


utterance_format = (
    "{}",
    "My name is {}",
    "Call me {}",
    "I'm {}",
)


##########
# Print utterances
##########

for utterance in utterance_format:
    for slot in slots:
        print(utterance.format(slot))



