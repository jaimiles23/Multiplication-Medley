"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-18 10:59:55
 * @modify date 2020-05-18 10:59:55
 * @desc [
    log_all function used to log all parameters @ specified log_level.
 ]
 */
"""

##########
# Imports
##########

from logs import logger, log_func_name


##########
# Log_all func
##########
@log_func_name
def log_all(*args, log_level: int = 10) -> None:
    """Logs all arguements at log_level keyword."""
    log_level_dict = {
        10  :   logger.debug,
        20  :   logger.info,
        30  :   logger.warning,
        40  :   logger.error,
    }

    log_type = log_level_dict[log_level]
    for arg in args:
        log_type(arg)
    return

