"""
Validation for the entered data to check flawed data
"""

import re

ENCODE_VALIDATION = "\d{1,3}_\d{1,4}_[^_]+_[0-9a-f]{8}_[0-9a-f]{8}_([0-9a-f]{4})*_.*"


def check_encode(code):
    """
    Checks if the app-encoded string is valid
    :param code: The encoded string
    :return: Whether the encode is valid
    """
    return re.compile(ENCODE_VALIDATION).match(code) is not None
