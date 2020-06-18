"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-12 13:28:25
 * @modify date 2020-05-18 17:28:37
 * @desc [
   Data module for the questions directory. Data for:
   - Problem synonyms
   - 1st problem intros
   - Normal problem intros
   - question intros
   - problem number
   - retry question
   - num questions answered.
 ]
*/
"""

##########
# Problem Synonyms
##########

MT_QUESTION_SYNS = (
   "problem",
   "question",
   "one",
)

MT_QUESTION_NUM_SYNS = (
   "problem",
   "question",
)


##########
# 1st Problem
##########

MT_CONFIRM = (
   "OK,",
   "Alright,",
)

MT_FIRST_QUESTION = (
   "Here's the first",
   "Get ready for the first",

   "To start, try this",
   "Let's start with this",
   "We're starting with this",

   "Begin with this",
   "Let's begin with this",
)

MMT_FIRST_QUESTION = (
   MT_FIRST_QUESTION,
   MT_QUESTION_SYNS,
)


##########
# Normal Problem
##########
MT_LONG_INTRO = (
   "Here's another.",
   "Let's keep going.",
   
   "Try another.",
   "Try this one.",
   
   "Next Problem.",
   
   "Another one.",
   "Another.",
)

##########
# Question Intro
##########
MT_QUESTION_INTRO = (
   "What about",
   "And",
   "What's",
   "What's",
)


##########
# Problem Number
##########
MT_START_PROB_NUM = (
   "Here's",
   "Let's go to",
   "And",
   "Solve",
)

MMT_PROBLEM_NUM = (
   MT_START_PROB_NUM,
   MT_QUESTION_NUM_SYNS,
)


##########
# Retry question
##########

MT_FIRST_RETRY = (
   "Same question again:",
   "Same question:",
   
   "You got this!",

   "Try again:",
   "Let's try this again:",
   "Let's try again:",
)

MT_MULT_RETRY = (
   "I know this is hard, but you got this!",
   "I believe in you!",
   "Don't give up!",
   "This time for sure!",
)

##########
# Num Questions answered
##########

MT_NUM_QUESTIONS_ANS = (
   "You've answered {} questions.",
)
