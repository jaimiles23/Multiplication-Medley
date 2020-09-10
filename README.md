![](https://i.imgur.com/HGvz2s5.jpg)

# Multiplication Medley

- [Multiplication Medley](#multiplication-medley)
  - [About](#about)
  - [Directory](#directory)
  - [Skill activities](#skill-activities)
    - [Free play](#free-play)
    - [Custom practice](#custom-practice)
    - [Survival mode](#survival-mode)
    - [Speed challenge](#speed-challenge)
  - [Voice User Interface](#voice-user-interface)
    - [Natural language understanding](#natural-language-understanding)
    - [Natural language generation](#natural-language-generation)
  - [Major changes to implement](#major-changes-to-implement)
    - [Re-structure wrong_quest_by_date dict.](#re-structure-wrong_quest_by_date-dict)
    - [Create, change, and delete user profiles](#create-change-and-delete-user-profiles)

## About
Multiplication Medley is an educational Alexa skill that helps users practice their times tables. Users create a profile and play 4 different multiplication activities:
1. Free Play
2. Custom Practice
3. Survival Mode
4. Speed Challenge

[Link to Multiplication Medley in Amazon Marketplace.](https://www.amazon.com/jaimiles23-Multiplication-Medley/dp/B0899VVC7M/ref=sr_1_1?dchild=1&keywords=multiplication+medley&qid=1592459984&s=digital-skills&sr=1-1)

<br>
<b> <a href = "#multiplication-medley"> ToC &#8593; </a></b>
<br>
<br>

## Directory

- 0_planning
  - Documents related to the skill planning and design.
- 1_code
  - Code required to deploy skill on AWS Lambda.
- 2_interaction_model
  - JSON to train the natural language understanding model through the [Alexa Developer Console.](https://developer.amazon.com/alexa/console/ask)
- 3_distribution
  - Documents pertaining to the distribution of the skill in the [Amazon Marketplace.](https://www.amazon.com/jaimiles23-Multiplication-Medley/dp/B0899VVC7M/ref=sr_1_1?dchild=1&keywords=multiplication+medley&qid=1592459984&s=digital-skills&sr=1-1)


** Navigating 1_code**
Application code is deployed via AWS Lambda. A user Alexa request triggers the lambda function which accesses the skill builder stored in the `lambda_function.py` file. The skill builder selects the appropriate handler to process the user's request.

<br>
<b> <a href = "#multiplication-medley"> ToC &#8593; </a></b>
<br>
<br>

## Skill activities

### Free play
Users practice set up the multiplication tables they want to practice. They select:
- the tables to answer questions from
- an upper and lower limit for their tables (optional)
- a number of questions to practice (optional)


### Custom practice
Multiplication Medley designs a customized practice for the user based on their answer statistics. The custom practice has 4 components:
  1. *Recent errors*: users correct recent errors
  2. *High error tables*: users practice tables with more mistakes than an accepted threshold
  3. *High relative errors*: users practice tables they mess up more often than others (a)
  4. *New tables*: times tables above the user's average difficulty

(a) To determine high relative errors, individual multiplication table errors are standardized into z-scores and users are asked tables with high mistake z-scores.


### Survival mode
Survival Mode tracks how many multiplication questions the user can answer without making a mistake. 


### Speed challenge
Speed mode tracks how quickly the user can complete a series of multiplication questions. There are 4 different modes to select from:

| Mode  |   Lower Times Table   |   Upper Times Table   |   
|   :-- |   --:                 |   --:                 |
|   Normal    |   0   |   10    |
|   Hard      |   0   |   12    |
|   Advanced  |   10  |   20    |
|   Insane    |   20  |   30    |

Users answer a number of questions sampled from the range. Time is tracked from the beginning of the mode until the user answers the last problem.

<br>
<b> <a href = "#multiplication-medley"> ToC &#8593; </a></b>
<br>
<br>


## Voice User Interface
Alexa applications utilize a Voice User Interface (VUI) and thus frontend development differs from standard development for Graphical User Interfaces. To interact with the user, Alexa employs two areas of natural language processing:
1. natural language understanding
2. natural language generation


### Natural language understanding
Skills train Alexa's neural net to assign user utterances to specific intents. The neural net is trained with 3 pieces of information for each intent:
1. Intent Name
1. Slots
1. Sample Utterances

Intent slots represent specific information for the specified intent. For instance, if the user wants to start Speed Challenge on easy difficulty, they must
provide the 'easy' slot in their intent. A sample utterance follows:
> "Start Speed Challenge on easy difficulty."

The following code block shows the training data for the Start Speed Challenge Intent.
```json
"name": "StartSpeedChallengeIntent",
    "slots": [
        {
            "name": "difficulty",
            "type": "sc_difficulty"
        }
    ],
    "samples": [
        "play speed challenge",
        "play speed challenge with {difficulty}",
        "Begin speed challenge with {difficulty}",
        "speed challenge with {difficulty}",
        "start speed challenge with {difficulty} difficulty",
        "begin speed challenge",
        "start speed challenge"
    ]
```

Neural net training information is held in the skill's **interaction_model** json file.


### Natural language generation
![](https://user-images.githubusercontent.com/50056791/87263264-7ca8b080-c471-11ea-92de-00a7b3644027.png)

This skill utilizes a naive natural language generation (NLG) to interact with the user. The method transforms linearly connected sentence chunks (e.g., clauses, parts of speech, etc.) into speech responses.

Consider the following arbitrary noun phrase:
> "The red dog"

This phrase can be parsed into 3 separate chunks:
   1. "The": determiner
   2. "red": colour adjective
   3. "dog": animal noun

In this example, the determiner, adjective, and noun have no effect on the meaning of the response. We can use naive NLG to create an arbitrary noun phrase. This skill's NLG method would sample from the following three message tuples (MT). A single item is sampled from each message tuple to create the noun phrase (DET, JJ, NN).
```python 3
MT_DET = (
    "The",
    "A",
)
MT_COLOUR_JJ = (
    "red",
    "blue",
    "yellow",
)
MT_ANIMAL_NN = (
    "dog",
    "cat",
)
```
This NLG method requires careful consideration of sentence structure and semantics to avoid unnatural responses. However, successful implementation increases response variety multiplicatively. The speech construction for the above noun phrase yields 12 response permutations.

Data for each NLG method is located in each subdirectory's `data` module.

<br>
<b> <a href = "#multiplication-medley"> ToC &#8593; </a></b>
<br>
<br>

## Major changes to implement
![](https://user-images.githubusercontent.com/50056791/87263220-52ef8980-c471-11ea-92f0-a5d1ac830eda.gif)

I have a daunting backlog of features and quality of life improvements saved to my desktop. I will ignore those and instead focus on implementing the following major changes.

### Re-structure wrong_quest_by_date dict.
Multiplication Medley saves the times tables that users answer incorrectly in the `wrong_quest_by_date` dictionary, a session attribute. Questions are saved under the date that the user answered it incorrectly. This makes it easy to remove questions that are no longer pertinent to the user, e.g., if the user missed it 2 weeks ago.

The abstract data structure is shown below.

```python3
wrong_quest_by_date = {
    date1   :   {
        table_1   :   {
            table_2 :   int_incorrect,
            table_3 :   int_incorrect,
        },
        2nd_table   :   {
            table_1 :   int_incorrect,
            table_2 :   int_incorrect,
        },
    }
    date2   :   {
        table_1 :   {
            table_2 :   int_incorrect,
        },
    }
}
```

The nested dictionary keys and values are as follow:
- `date`: str, ISO-formatted
- `table_1`: int, 1st number of times table
- `table_2`: int, 2nd number of times table
- `int_incorrect`: int, number of times user answered incorrectly


There are _2 challenges_ with this data structure. 

1. **Repetitive dictionary keys between dates**. 

If a user answers the question 9 x 6 on two separate dates, the `wrong_quest_by_date` assumes the following data structure:
```python3
wrong_quest_by_date = {
    2020-06-18   :   {
        9   :   {
            6 :   1,
        },
    }
    2020-06-17   :   {
        9 :   {
            6 :   1,
        },
    }
}
```
The key overlap can be resolved by storing the dates as values instead of dictionary keys. The `int_incorrect` value should instead be a list, `dates_incorrect`, that holds ISO-format string data representing the date that the user answered the question incorrect. The above sample dictionary should be stored as followed instead:
```python3
wrong_quest_by_date = {
    9   :   {
        6 :   [2020-06-18, 2020-06-17]
    },
}
```

1. **Stored as a session attribute**.

The `wrong_quest_by_date` dictionary is stored as session attribute (i.e., JSON file) and is _not_ assigned to a player profile. Thus, Custom Practice does not distinguish the `wrong_quest_by_date` between players. This can be fixed by storing the `wrong_quest_by_date` dictionary as an instance attribute of the player class.


### Create, change, and delete user profiles
Currently, users are only prompted to create a user profile during the initial launch of the skill. There are no options to change between profiles, delete existing profiles, or corresponding help menus for creating a new profile. These features need to be implemented in the user_profile library.
