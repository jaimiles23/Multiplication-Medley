# Skill Plan

This document details the first-stage planning for my Multiplication Medley skill. There are 3 sections:
1. *Domain*: domain and purpose of the skill.
2. *Activities*: general planning of skill activities.
3. *Features*: non-activity features of the skill to enhance the user experience.

**Mandatory acknowledgement of scope creep**: I have found that my projects tend to evolve rapidly in scope. To help contain my skill's scope, I have made it good practice to do as much up-front planning for the skill as possible. It is imperative to have a rigid definition of the purpose and goals of the skill to know when to accomodate new, emergent feature ideas during the coding.

As such, my skill planning consists of defining the domain, the general purpose activities, and the features. These are established in hierarchy. The skill's domain is rigid and is nearly immovable. In contrast, the skill's features are more easily influenced by implementation and discovery.


## Domain
To define the domain of the skill, I reflect on my purpose for creating Alexa skills:
> To create fun, engaging skills that teach practical, transferrable skills.

_NOTE_: the audience of the skill may vary, e.g., normal audience vs children vs ESL. Thus, something that is fun & engaging is subjective, but do have some shared themes, e.g., variety and fluid play structure.


The broad domain of the skill is Multiplication, which has two immediate implementations: 
1. Teaching
2. Practice

It would require a group of educators and linguists to effectively teach multiplication through a Voice User Interface. This skill will provide a platform to practice Multiplication skills.


## Activities
All skill activities will focus on the same premise; answering multiplication questions. Activities will be grouped into two general modes:
1. Practice
2. Competitive


### Practice
I have outlined two practice activities for Multiplication Medley:
1. Free Play
2. Focused Practice


#### Free Play
Free Play mode is used for general practice, where users can free practice multiplication questions.

**Set-up**:
1. lower table
2. upper table
3. upper limit (optional) -- reconsider name.
4. number of questions (optional)

I THINK that the setup should only be table setup, and provide 2 options: range & individual tables --: individual will be query to parse.

If the user does not specify a number of questions, interruptions will occur in the following scenarios:

| Interrupt Condition | Interrupt Message |
| :--                 | :--               |
| Every X multiple of questions, e.g., 50 | "Wow, you've answered X questions. Do you want to keep playing, or do you want to play another activity?" | 
| If the user passes a certain metric error threshold, e.g., incorrect 9's times table above a threshold. | "I noticed you have some trouble with the 9's Times Tables. Do you want to practice them in focused practice?"  |


**Mode features**
- First problem should always be easier, e.g., second number should be sampled from lower range. If practice 9's table, then second number is from 1-5.
- Should be able to change these parameters mid-mode. e.g., "Change the lower table to X". 
- Positive & Negative reinforcement for each answer
- Tells user number of correct answers @ end
  - Should provide feedback, e.g., May want to practice 7's times tables. Or 95%! You've mastered this. Try going higher next time!
- Ask questions in different format, e.g., "What is"
  - Should change based on difficulty, e.g., on hard questions: "Do you know?"

#### Custom Practice 
NOTE: Currently using 'custom' to avoid confusion with words like 'tailored' or 'specialized'. This skill targets Elementary school kids.

This mode (name pending) will ask users questions based on the metrics collected about them. For instance, if they answered questions erroneously, will ask them if they want to practice the questions they got wrong. If they have a tendency to answer a certain times table incorrect, will ask those questions.

_NOTE_: The user may provide an intent to start by practicing mistakes, frequent errors, or a recommended times table.

Practice will suggest through 3 different activities:
  1. Outstanding errors.
  2. High frequency errors, e.g., 1.5 standard deviations above the mean.
  3. If no standard deviations, and errors below x% of questions asked, then recommend practicing a new Times Table, e.g., 13's.

NOTE: yes, need to implement so all means are low. Not sure what common % is? <5% error?


**Notes**:
- Need to avoid asking duplicate questions. If only duplicates in the list, then acknowledge it and say "I noticed you're having difficulty with this problem. Let's practice it twice to help you remember it".
- If fewer than X problems have been answered, tell the user to come back after playing through more questions.
- Maybe start suggesting things after the user answers 10 questions?


**Mode features**
- Positive & Negative reinforcement for each answer
- Tells the user their score as a percentage correct.
- If there is still a Times Tables above a threshold, indicate that they may want to practice it more.
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

Users are asked all question combinations in these Times Tables and must answer all problems corrects. The time is tracked from the beginning of the mode until the user answers the last problem.
NOTE: May like to change to ask 3 random problems from each times table in the range. For each table, pop3 numbers from a list and add those + the table to the list of questions.
This way, 30 or 36 questions instead of 100??
  - Can play with distribution still. e.g., double every number above the current table. If on 8's table, 2 8s, 9s, and 10s to pick from. Still 1 (1-7) to pick from??


**Mode features**
- Negative reinforcement. Positive reinforcement may slow down the user's time and lead to frustration.
- Tells the user their time & number of errors
- Personal record for each mode
- average and std for each mode -- NOTE: tracks average over last 15 (?) attempts & congrats changed on std from average.


#### Survival Mode
Survival Mode tracks how many multiplication questions the user can get right before making a mistake. 

Questions are scaled upward with Gaussian distribution.

**Mode features**
- Tracks personal record (number answered), and average & std of the last 15 attempts.
- Provides congratulations based on where the question was sampled from. If it's sampled towards the ceiling, provide congrats. If low, no congrats/confirmation.
- Changed from 3 lives to 1 to increase intensity/stakes. NEED TO LOG NUM PROBLEMS, upper/lower, distribution, etc. ON DEATH, AND CONSIDER IF SHOULD REMAKE 3 LIVES. Regardless, implement with lives mechanic.
- On 1st reprompt, note that they have to answer before Alexa shut's down, or else all progress is lost. HAVE VAR OPEN TO DICTATE LAUNCH INTENT. If var == True, upon re-opening in the same day, tell them that they took too long to answer Survival Mode so they lost all progress.


## Features
- NOTE: many features can be implemented AFTER all activities are finished. Should launch and develop small user base.
- Keep tuple of consecutive logins. Can have Launch request acknowledge hotstreaks of logins, problems solved this week, etc.
- Keep tuple of last 7 days. Tracks if logged in, number of problems solved, accuracy of answers, etc.

- Can add intent to check out statistics, etc.
- Track dictionary of Times Tables. Contains key for each number, & increment when incorrect. Increment dictionay twice, once for each number in the question. Can then recommend user to practice Times Tables based on the error frequency. NOTE: Need to increment every for correct & incorrect. It should be % based, NOT pure quantity based.
  - Focused practice on these tables should modify this number somehow? like if recommended, and then practice, make those weight more?
  - OR, can keep list of X most recent answers, boolean T/F array if correct or not... MHMMMM.
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


## File Organization
- EVERYTHING SHOULD BE OWN FOLDER - NO STANDARD COMPONENT BULLSHIT.


## Future
- Implement the user profile under a name, just so can add more later if I want??
- Note: LOG info for modes AND SCORES EACH TIME. That way, can parse the information and get an idea of the average time for each mode. Can later update the skill based on this.
  - NOTE: may also like to log other information with this, e.g., the user-id, the number of times they played, their problem accuracy, etc.
- May like to implement fun facts when certain number of problems is reached, e.g., 314, say something about Pie.
- Ability to switch user profile to accomodate more people. - note, may mess up login statistics, but that's fine.
- Note: Can later extend this to collect information on user answers. Get IP, correct Times Tables answers, incorrect Times Tables answers, number of logins, etc. 
- Can implement multiplayer survival mode later.