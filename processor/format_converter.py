"""
Convert the encoded values into human-readable format
"""


def format_encode_value(value, const_set):
    """
    Formats the encoded value based on the type
    :param value: The value of the encode
    :param const_set: The dictionary specifying data type and any extra info
    :return: The formatted string
    """

    if const_set is None or "type" not in const_set:
        return str(value)
    else:
        t = const_set["type"]

        if t == "checkbox":
            return str(bool(value))

        elif t == "timestamp" or t == "duration":
            return str(value // 60) + "m " + str(value % 60) + "s "

        elif t == "rating":
            if "max" in const_set:
                return str(value) + " out of " + str(const_set["max"])
            else:
                return str(value)

        elif t == "choice":
            if "choices" in const_set:
                if 0 <= value < len(const_set["choices"]):
                    return "<" + str(const_set["choices"][value]) + ">"
                else:
                    return str(value)
            else:
                return str(value)

        else:
            return str(value)
