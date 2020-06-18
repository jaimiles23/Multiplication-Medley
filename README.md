![.](https://user-images.githubusercontent.com/50056791/84987459-06749080-b0f5-11ea-864b-19ef43dd6664.jpg)


# Multiplication Medley
Multiplication Medley is an educational Alexa skill that helps users practice their times tables. Users create a profile and practice their multiplication tables in Free Play or play Survival Mode or Speed Challenge. After collecting enough data, the skill designs a Custom Practice for the user to improve their times tables. [Link to Multiplication Medley in Amazon Marketplace.](https://www.amazon.com/jaimiles23-Multiplication-Medley/dp/B0899VVC7M/ref=sr_1_1?dchild=1&keywords=multiplication+medley&qid=1592459984&s=digital-skills&sr=1-1)


## Directory
1. 0_planning
   1. Documents related to the skill planning and design.
2. Code
   1. All code required to deploy the skill.
3. Interaction Model
   1. JSON data file used to train skill neural net.
4. Distribution
   1. Documents for the distribution of the skill.


## Major changes to implement
Below are major changes to be implemented.

### Re-structure wrong_quest_by_date dict.
Multiplication Medley currently saves the times tables that users get incorrect as a session attribute in the `wrong_quest_by_date` dictionary.

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
- `int_incorrect`: int, number of times user answered incorrectly.


There are _2 issues_ with this nested dictionary data structure. 

1. **Repetitive dictionay keys between dates**. 
For instance, a user may mess up the question 9 x 6 on two separate dates. The resulting dictionary would look similar to this.
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
This can be resolved by removing the date level from the dictionary. the only dictionay keys will be `table_1` and `table_2`. The `int_incorrect` value will instead be a list, `dates_incorrect`, which holds ISO-format string data representing the date that the user answered the question incorrect. The above sample dictionary will be stored as follows:
```python3
wrong_quest_by_date = {
    9   :   {
        6 :   [2020-06-18, 2020-06-17]
    },
}
```

2. **Stored as a session attribute**.
The `wrong_quest_by_date` dictionary is stored as session attribute level and is _not_ assigned to a player profile. Thus, during Custom Practice the `wrong_quest_by_date` does not distinguish players. This can be fixed by storing the `wrong_quest_by_date` dictionary as an instance attribute of the player class.


### Create, change, and delete user profiles
Currently, users are only prompted to create a user profile during the initial launch of the skill. There are no options to change between profiles, delete existing profiles, or corresponding help menus for creating a new profile. These are features that need to be built into the user_profile library.

