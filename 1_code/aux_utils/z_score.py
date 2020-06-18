"""/**
 * @author [Jai Miles]
 * @email [jaimiles23@gmail.com]
 * @create date 2020-05-26 16:05:10
 * @modify date 2020-05-26 16:29:02
 * @desc [
    Auxiliary function to standardize the calculation of z-scores.
    
    NOTE:
    - The z_score (or standard score) is used to normalize the data for comparison.
    However, I do NOT assume the data to be normally distributed, and thus do not use assumptions associated with z_scores.
    e.g., % of other multiplication problems lower/higher than the z_score.
 ]
 */
"""

##########
# Imports
##########

from statistics import mean, stdev

from logs import log_all, log_func_name, logger


##########
# Calculate z_score func
##########

@log_func_name
def calc_z_score(
    data_point: float, 
    data_mean: float = None, 
    data_stdev: float = None,
    data: list = None,
    required_data_length: int = 2,
    ) -> float:
    """Returns z_score for data list.
    
    data_point: (required) float. Returns z_score.
    data_mean: (optional) float.
    data_stdev: (optional) float. 
    data: (optional) list. 
    required_data_length: int - minimum data to calculate z_score.


    NOTE: User must prvoide either mean & stdev, or data. Otherwise,
    insufficient data to calculate z-score.
    """
    if (data is not None) and (len(data) < required_data_length):
        logger.info(f"calc_z_score - list length {data}")
        return 0
    
    elif data_mean is None:
        data_mean = mean(data)
    
    elif data_stdev is None:
        data_stdev = stdev(data, xbar = data_mean)

    try:
        z_score = (data_point - data_mean) / data_stdev
    except ZeroDivisionError:
        logger.info("calc_z_score - 0 stdev")
        z_score = 0

    log_all( data_mean, data_stdev, z_score)
    return z_score

