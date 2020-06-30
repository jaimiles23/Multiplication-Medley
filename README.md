![.](https://user-images.githubusercontent.com/50056791/84987459-06749080-b0f5-11ea-864b-19ef43dd6664.jpg)


# Multiplication Medley
Multiplication Medley is an educational Alexa skill that helps users practice their times tables. Users create a profile and practice their multiplication tables in Free Play, or play Survival Mode or Speed Challenge. After sufficient data is collected, the skill designs a Custom Practice for the user to improve their times tables. 

[Link to Multiplication Medley in Amazon Marketplace.](https://www.amazon.com/jaimiles23-Multiplication-Medley/dp/B0899VVC7M/ref=sr_1_1?dchild=1&keywords=multiplication+medley&qid=1592459984&s=digital-skills&sr=1-1)


## Directory
1. 0_planning
   1. Documents related to the skill planning and design.
2. 1_code
   1. Code required to deploy the skill.
3. 2_interaction_model
   1. JSON data file used to train skill neural net.
4. 3_distribution
   1. Documents for the distribution of the skill.


## Speech construction
This skill uses **speech construction** to dynamically generate the prompts returned to the user. Speech construction generates a speech response by sampling sentence chunks (e.g., clauses, parts of speech, etc) from a series of linearly connected tuples.

Consider the following noun phrase:
> "The red dog"

This sentence can parsed into 3 separate chunks:
   1. "The": determiner
   2. "red": colour adjective
   3. "dog": animal noun

Rather than hard coding "the red dog" as a response, speech construction methods sample from the following three message tuples (MT).
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

A single item is sampled from each message tuple to create the noun phrase (DET, JJ, NN). Speech construction requires careful consideration of sentence structure and semantics to avoid unnatural responses. However, successful implementation increases response variety multiplicatively. The speech construction for the above noun phrase yields 12 response permutations.


## Major changes to implement
Below are major changes to be implemented.

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

The `wrong_quest_by_date` dictionary is stored as session attribute level and is _not_ assigned to a player profile. Thus, Custom Practice does not distinguish the `wrong_quest_by_date` between players. This can be fixed by storing the `wrong_quest_by_date` dictionary as an instance attribute of the player class.


### Create, change, and delete user profiles
Currently, users are only prompted to create a user profile during the initial launch of the skill. There are no options to change between profiles, delete existing profiles, or corresponding help menus for creating a new profile. These features need to be implemented in the user_profile library.

