"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 15:57:32
 * @modify date 2020-05-04 16:00:20
 * @desc [
Init file for the logger directory. Contains:
- logger
- log_func_name decorator
- log_all


NOTE: This is not done for all libraries loading __init__ file will force import of all. 
This can lead to circular imports for inter-reliant classes.
 ]
 */
"""

from logs.logger_init import logger

from logs.log_decorators import log_func_name

from logs.log_all_args import log_all
