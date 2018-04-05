"""
Decodes the hex string as a table of data
"""


def split(hex_encode):
    """
    Splits hex strings into tuples of data
    Performs bit extraction
    :param hex_encode: Hex encoded string from the app
    :return: A generator of tuples
    """

    for i in range(len(hex_encode)//4):

        data = int(hex_encode[i * 4: (i + 1) * 4], 16)

        data_type = (data & (1 << 6) - 1 << 8) >> 8
        value = data & ((1 << 8) - 1)
        undo_flag = bool(data & 1 << 15)
        state_flag = bool(data & 1 << 14)

        yield (data_type, value, undo_flag, state_flag)


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


def decode(hex_encode, board):
    """
    Decodes hex data into a table
    :param hex_encode: Hex encoded string from the app
    :param board: The board data for formatting
    :return: Generator in the format of (formatted_type, formatted_value, undo)
    """

    for t, v, u, s in split(hex_encode):

        formatted_type = board.log(t)

        if not s:
            formatted_type += ":Off"

        formatted_value = format_encode_value(v, board.dc(t))

        undo = "Yes" if u else "No"

        yield (formatted_type, formatted_value, undo)
