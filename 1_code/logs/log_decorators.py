"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-04 15:50:17
 * @modify date 2020-05-05 09:21:30
 * @desc [
log_decorators

> def log_func_name(func, *args, **kwargs): Decorator to log the function name.

]
*/"""


##########
# Imports
##########

from functools import wraps


from logs import logger


##########
# Decorators
##########

def log_func_name(func, *args, **kwargs):
    """Decorator to log.debug the function name.
    """
    @wraps(func)
    def func_name_wrap(*args, **kwargs):
        logger.debug(f"FUNC:    {func.__name__}")
        return func(*args, **kwargs)
    return func_name_wrap
