# Skill Plan

This document details the first-stage planning for my Multiplication Medley skill. There are 4 sections:
1. Purpose
2. Domain
3. Activities
4. Features


## Purpose
> provide a fun, engaging platform for users to practice their multiplication tables.

## Domain

Alexa’s primary purpose is that of a virtual assistant. She can order you a pizza, plan a trip, or turn off your lights while you’re in bed. As such, she waits for the user to give her a command and then carries it out. One command at a time. This is true for her music skill, video skills, Smart Home skills, etc. Naturally, this sets a precedent for the design of custom-model skills as well.   

Most Alexa custom-skills are **functionally defined**. Functionally defined skills are created to serve a specific purpose, e.g., to turn off the lights or to tell a knock-knock joke. The format for a traditional,  functionally-defined knock knock joke skill is as follows:
> User: "Alexa, tell me a knock knock joke."
> 
> Alexa: "Knock Knock."
> 
> User: "Who's there?"
> 
> Alexa: "Abby."
> 
> User: "Abby who?"
> 
> Alexa: "Abby birthday do you!"
> 
> Alexa: Close skill.


However, most custom-model skills should not be viewed with the same lens as traditional virtual assistant skills. Instead, custom-model skills should be designed with respect to Uses and Gratification theory, which attempts to understand why _users use media_. Most users seek custom-model skills for entertainment. It's likely that a user wants to hear more than one knock knock joke, just as it's likely that a user wants to practice more than a single multiplication problem.

I made two assumptions about Multiplication Medley users: (1) users want to practice multiplication tables and (2) users want to be entertained. Multiplication Medley is a **domain-defined** skill. The skill's domain is multiplication practice and thus has different multiplication-related activities. The different activities are key to keeping users entertained, while still achieving their purpose of practicing multiplication tables.


## Activities
All skill activities focus on the same premise; answering multiplication questions. Activities are grouped into two general modes:
1. Practice
2. Competitive


### Practice
There are two practice activities for Multiplication Medley:
1. Free Play
2. Focused Practice


#### Free Play
Free Play mode is used for general practice, where users can free practice multiplication questions.

**Set-up**:
1. lower table
2. upper table
3. lower limit, smallest number asked from table (optional)
4. upper limit, largest number asked from table (optional)
5. number of questions (optional)


**Mode features**
- Users can change parameters at any time. e.g., "Change the lower table to X"
- Positive & try again responses for user answer
- Tells user number of correct answers @ end
  - Should provide feedback, e.g., May want to practice 7's times tables. Or 95%! You've mastered this. Try going higher next time!
- Ask questions in different format, e.g., "What is"
  - Should change based on difficulty, e.g., on hard questions: "Do you know?"

#### Custom Practice 
This mode asks users questions based on the metrics collected about them. Practice is structured from 4 differnet activities:
  1. **Recent errors**: correct recent questions.
  2. **High error tables**: if user mistakes a table past a certain threshold.
  3. **High relative errors**: if user messes up a table more often than others.
  4. **New tables**: Recommend practicing a questions above average times table.

NOTE: thresholds are subject to change.

**Notes**:
- Need to avoid asking duplicate questions. If only duplicates in the list, then acknowledge it and say "I noticed you're having difficulty with this problem. Let's practice it twice to help you remember it".
- If fewer than X problems have been answered, tell the user to come back after playing through more questions.


**Mode features**
- Positive & Negative reinforcement for each answer
- Tells the user their score as a percentage correct.
- If there is still a Times Tables above a threshold, continue practicing.
- Ask questions in different format, e.g., "What is", 


### Competitive
Likewise, there are two competitive activities:
1. Speed
2. Survival


#### Speed Challenge
Speed mode tracks how quickly the user can complete a series of multiplication questions. There are 4 different modes to select from:

| Mode  |   Lower Times Table   |   Upper Times Table   |   
|   :-- |   --:                 |   --:                 |
|   Normal    |   0   |   10    |
|   Hard      |   0   |   12    |
|   Advanced  |   10  |   20    |
|   Insane    |   20  |   30    |

Users must correctly answer a number of questions sampled from the range. The time is tracked from the beginning of the mode until the user answers the last problem.

**Mode features**
- Only Negative reinforcement. Positive reinforcement may slow down the user's time and lead to frustration.
- Tells the user their time.
- Personal high score and average score for each mode


#### Survival Mode
Survival Mode tracks how many multiplication questions the user can answer without making a mistake. 

Questions are sampled from sliding Gaussian distribution.

**Mode features**
- Tracks personal record (number answered), and average & std of the last 15 attempts.
- Provides congratulations based on where the question was sampled from. If it's sampled towards the ceiling, provide congrats. If low, no congrats/confirmation.
- Indicate warnings when passing certain thresholds, e.g., questions will now be sampled above user's average table.


## Features
- NOTE: many features can be implemented AFTER all activities are finished. Should launch and develop small user base.
- Keep tuple of consecutive logins. Can have Launch request acknowledge hotstreaks of logins, problems solved this week, etc.
- Keep tuple of last 7 days. Tracks if logged in, number of problems solved, accuracy of answers, etc.
- Intent to hear statistics
- Intent to create and change user profiles
- Track dictionary of Times Tables. Contains key for each number, & increment when incorrect. Increment dictionay twice, once for each number in the question. Can then recommend user to practice Times Tables based on the error frequency. NOTE: Need to increment every for correct & incorrect. It should be % based, NOT pure quantity based.
  - Focused practice on these tables should modify this number somehow? like if recommended, and then practice, make those weight more?
  - OR, can keep list of X most recent answers, boolean T/F array if correct or not... 
    - if so, can also keep statistic of mean there, and update the mean everytime the table is updated... can update % wise, since always out of 25, to save on computations? Don't implement this way yet, only if expensive.
    - NOTE: each table should have a mean AND STD key associated with it too. This will reduce time complexity and remove nested for loops. These two metrics can be updated with the dict on each level.
    - NOTE2: Use mean so that can compare times tables with different amount of data.

- Different levels of congratulations that change depending on:
  - Relative difficulty of question vs user's average question over the past 5 days?
  - Frequency of error problem
  - Consecutive correct answer streaks
  - Correct answer after consecutive mistake streak
    - NOTE: Can store consecutive counts as a session attribute instead of in player class.
  - Note: can create different levels with wrappers while using same string. e.g.,, 1 & 2 can be the same, but an excite_low wrapper??
  - Note: small random chance to go up 1 congratulation level?
  - Chance for no congratulation too.
