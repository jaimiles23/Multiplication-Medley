@modify date 2020-05-25 17:33:17
I chose to use a dictionary for each mode to account for the flat access structure of the skill. A user may pre-emptively exit one mode, e.g., FreePlay, and start another without exiting.
By holding a dictionay for each mode, I don't have to continually call a method to update the session statistics if this occurs. Instead, I can call it once either when the user 
provides a proper stop to an activity & i want to report their stats to them, or they exit the skill and I want to update session statistics for the exit message.

### Congrats
NOTE: Congrats must be before adjusting other attributes, e.g., consecutive correct. This is because uses breaking a consecutive incorrect congrats.


### Frequency of practicing incorrect answers
The number of times incorrect is manipulated to determine the number of times the user should practice the problem. 
```python

times_incorrect = int( sqrt(times_incorrect + 1))
if times_incorrect == 1:
    times_incorrect -= 1
```
When incorrect is 0, delete the table, and delete subsequent empty data structures.

NOTE: This needs to be updated. It's not num times to practice, but the manipulation of times incorrect.

For instance:
|   Times Incorrect |   Num times practice  |
|   :--             |   :--                 |
|   1               |   1                   |
|   2               |   1                   |
|   3               |   1                   |
|   4               |   2                   |
|   5               |   2                   |
|   6               |   2                   |
|   7               |   2                   |
|   8               |   3                   |
|   9               |   3                   |

Why? The square root provides an easy way to 'flatten' the curve, and avoid heavy repetition of a problem. A simple 1:1 of times incorrect and times to practice would be tedious. Additionally, Free Play and Speed Challenge provide additional practice on the problem, by requiring that the user answer the question correctly before moving forward. Thus, the user is already receiving extra practice on these questions.

