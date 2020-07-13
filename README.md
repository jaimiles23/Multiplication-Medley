![.](https://user-images.githubusercontent.com/50056791/84987459-06749080-b0f5-11ea-864b-19ef43dd6664.jpg)


# Multiplication Medley
Multiplication Medley is an educational Alexa skill that helps users practice their times tables. Users create a profile and can then play 4 different multiplication activities:
1. Free Play
2. Custom Practice
3. Survival Mode
4. Speed Challenge

[Link to Multiplication Medley in Amazon Marketplace.](https://www.amazon.com/jaimiles23-Multiplication-Medley/dp/B0899VVC7M/ref=sr_1_1?dchild=1&keywords=multiplication+medley&qid=1592459984&s=digital-skills&sr=1-1)


## Directory
- 0_planning
  - Documents related to the skill planning and design.
- 1_code
  - Code required to deploy skill on AWS Lambda.
- 2_interaction_model
  - JSON to train the natural language understanding model through the [Alexa Developer Console.](https://developer.amazon.com/alexa/console/ask)
- 3_distribution
  - Documents pertaining to the distribution of the skill in the [Amazon Marketplace.](https://www.amazon.com/jaimiles23-Multiplication-Medley/dp/B0899VVC7M/ref=sr_1_1?dchild=1&keywords=multiplication+medley&qid=1592459984&s=digital-skills&sr=1-1)


## Activities
Multiplication Medley tracks user statistics across all modes, including the questions that users get wrong. Additionally, the skills tracks user scores for the two competitive modes: (1) Survival Mode and (2) Speed Challenge. Mode statistics are referenced when constructing messages for ending the activity.


### Free play
Users practice the multiplication tables they way they want. Users can pick:
- multiple tables or a range of tables to practice from
- an upper and lower limit for their tables (optional)
- a number of questions to practice (optional)

Questions are randomly generated from within the specified range.


### Custom practice
After collecting enough data on the user, the skill designs a customized practice for them. It analyzes usre data to ask questions from:
  1. **Recent errors**: correct recent questions.
  2. **High error tables**: if user mistakes a table past a certain threshold.
  3. **High relative errors**: if user messes up a table more often than others(1).
  4. **New tables**: times tables above the user's average difficulty.

(1) To determine high relative errors, individual multiplication table errors are standardized into z-scores and users are asked tables whose z-score are _X_ standard deviations above the average error.


### Survival mode
Survival Mode tracks how many multiplication questions the user can answer without making a mistake. 

Questions are sampled from sliding Gaussian distribution.


### Speed challenge
Speed mode tracks how quickly the user can complete a series of multiplication questions. There are 4 different modes to select from:

| Mode  |   Lower Times Table   |   Upper Times Table   |   
|   :-- |   --:                 |   --:                 |
|   Normal    |   0   |   10    |
|   Hard      |   0   |   12    |
|   Advanced  |   10  |   20    |
|   Insane    |   20  |   30    |

Users must correctly answer a number of questions sampled from the range. Time is tracked from the beginning of the mode until the user answers the last problem.


## Natural language generation
![](https://user-images.githubusercontent.com/50056791/87263264-7ca8b080-c471-11ea-92de-00a7b3644027.png)

This skill utilizes natural language generation (NLG) to transform  linearly connected sentence chunks (e.g., clauses, parts of speech, etc.) into speech responses. 

Consider the following arbitrary noun phrase:
> "The red dog"

This phrase can be parsed into 3 separate chunks:
   1. "The": determiner
   2. "red": colour adjective
   3. "dog": animal noun

In this example, the determiner, adjective, and noun have no effect on the meaning of the response. As such, we can use NLG to generate an arbitrary noun phrase. This skill's NLG samples from the following three message tuples (MT). A single item is sampled from each message tuple to create the noun phrase (DET, JJ, NN).
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
Dynamic speech construction requires careful consideration of sentence structure and semantics to avoid unnatural responses. However, successful implementation increases response variety multiplicatively. The speech construction for the above noun phrase yields 12 response permutations.


## Major changes to implement
![](https://user-images.githubusercontent.com/50056791/87263220-52ef8980-c471-11ea-92f0-a5d1ac830eda.gif)

I have a daunting backlog of features and qol improvements saved to my desktop. Let's ignore those and focus on these major changes to implement.

### Re-structure wrong_quest_by_date dict.
Multiplication Medley saves the times tables that users answer incorrectly in the `wrong_quest_by_date` dictionary, a session attribute. The abstract data structure is shown below.

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

1. **Repetitive dictionay keys between dates**. 

When a user incorrectly answers the question 9 x 6 on two separate dates, the resulting dictionary appears:
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

