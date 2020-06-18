@modify date 2020-05-25 17:32:37

## players
`players_dict`: dict - Dictionary of all players, stored as dictionaries.
`current_player`: str - name of the current player to access players_dict.


## General
`logins`: int - tracks the number of user logins.
`mode`: str - tracks the mode that the game is in: 
    - `free_play`
    - `custom`
    - `speed`
    - `survival`


`help_pointer`: str - tracks the type of information to include in the help menu.
    - `overview`
    - `user_profile`
    - `act_descript`
    - `free_play`
    - `fp_input`
    - `custom_practice`
    - `survival_mode`
    - `speed_challenge`


## Prompt
`prompt_func`: object - last function that was called for the prompt.
`prompt_ms`:  str - last prompt given to the user. called for auxiliary menu


## Flow Control
`next_handler`: str - indicates next handler in linear flow logic.
    - `create_profile`  -   CreateUserProfileHandler


## Free Play
- `times_tables`: list - constructed from lower_table & upper_table range, or tables_query. Determines which tables Free Play multiplication questions are taken from.
- `num_questions`: int - number of questions to ask the user.
- `asked_questions`: int - number of questions asked to the user.
- `upper_bound`: int - upper bound to ask multiplication questions.
- `inform_query_tables_format`: bool - handled by FreePlayAttr.clean_query_tables. True if likely parsed query tables incorrectly. Reminds user of format to use.


## Custom Practice
- `practice_type`: str. Represents the current practice type for custom practice. Types as follows ('incorrect', 'high_err_tbl', 'high_z_score', 'new_tables')
- `tbl_list_mean_errs`: list (table, mean_err). Tracks the table and the mean errors. Sorted by mean error, so higher mean error tables come first.
- `last_question`: bool. If the last question to ask in that practice. 
  - NOTE: This can be expanded to FP
- `cp_consecutive_correct`: int. Indicates how many consecutive correct questions have happened in each practice mode. This ends practice types that are not correcting incorrect answers.


## Survival mode
- `sm_upper`: int = 5. Used as the upper bound to be asked.
- `sm_center`: int = sm_upper / 1.25. Used as the center of random.gauss()

- `flag_double_digits`: bool. If should say double digits intro.
- `flag_upper_hit_avg`: bool. If should say sm_upper hit avg intro.
- `flag_cntr_hit_avg`: bool. If should say sm_center hit avg intro.


## Speed Challenge
- `sc_tables`: list: [int, int] representing the range of tables.
- `sc_questions`: list. Contains tuples representing the multiplication table.
- `sc_difficulty`: str. From ["Normal", "Hard", "Advanced", "Insane"]. Used to indicate what tables to use.
- `sc_start_time`: dict. Saves the start time of speed challenge.
- `sc_end_time`: dict. Saves the end time of speed challenge.


## Questions
- `question`: tuple(int, int) - holds the multiplication times tables asked to the user.
- `num_questions`: int - how many questions the user requested to be asked.
- `questions_answered`: int - the number of questions asked the user.
- `interrogative_question`: bool. Indicates if a question mark should be placed at the end of the question. This attr is reset each time used.


## Wrong questions
- `today`: str. YYYY_MM_DD (ISO format, internationa standard for organization), format to represent the current date. Used to save wrong_questions in the wrong_quest_by_date dictionary. 
- `wrong_quest_by_date`: 3 layer dictionary: all questions, specific dates, 1st table in problem, and 2nd table. The last integer value is the number of times that problem was incorrect.


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


## Session Statistics
- `consecutive_correct`: int - tracks number of questions that user got consecutively correct.
- `consecutive_incorrect`: int - tracks number of questions that user got consecutively incorrect.

- `mode_stats`: dict[ mode: [int, int] - tracks the statistics for each mode: int1 = correct answers, int2 = incorrect answers

- `session_correct`: int - tracks the number of answers that the user got correct during the session
- `session_incorrect`: int - tracks the number of answers that the user got incorrect during the session

