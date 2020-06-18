"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-03-27 20:57:58
 * @modify date 2020-04-28 16:15:07
 * @desc [
Contains logger for entire package Logger is instantiated here for easy editing, e.g., changing logger level to warning.

Logger level is access through Lambda environment variable: log_level

Logger levels described below:
    50  Critical
    40  Error
    30  Warning
    20  Info    
    10  Debug
    0   Notset
]
*/
"""


##########
# Imports
##########

from functools import wraps, partial
from logging import getLogger
import os


##########
# Logger
##########

logger = getLogger(__name__)

try:
    log_level = int( os.environ['log_level'])
except:
    log_level = 10
logger.setLevel(log_level)

