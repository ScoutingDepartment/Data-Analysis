"""
Conversion between numeric and string representations of time
"""
from datetime import datetime

DISPLAY_TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
FILE_TIME_FORMAT = "%Y%m%d%H%M%S"


def display_time(timestamp):
    """
    Returns the formatted timestamp according to DISPLAY_TIME_FORMAT constant
    """

    return datetime.fromtimestamp(timestamp).strftime(DISPLAY_TIME_FORMAT)


def file_time(timestamp):
    """
    Returns the formatted timestamp according to FILE_TIME_FORMAT constant
    """

    return datetime.fromtimestamp(timestamp).strftime(FILE_TIME_FORMAT)
