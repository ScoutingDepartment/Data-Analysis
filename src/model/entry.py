class Entry:

    @staticmethod
    def split(hex_encode):
        """
        Splits hex strings into tuples of data
        Performs bit extraction
        :param hex_encode: Hex encoded string from the app
        :return: A generator of tuples
        """

        for i in range(len(hex_encode) // 4):
            data = int(hex_encode[i * 4: (i + 1) * 4], 16)

            data_type = (data & (1 << 6) - 1 << 8) >> 8
            value = data & ((1 << 8) - 1)
            undo_flag = bool(data & 1 << 15)
            state_flag = bool(data & 1 << 14)

            yield (data_type, value, undo_flag, state_flag)

    @staticmethod
    def join(iterator):
        """
        Joins data into hex strings
        :param iterator: iterator through t, v, u, s values
        :return: Hex string
        """

        def generate_datum_hex():
            for t, v, u, s in iterator:
                yield str(hex(u << 15 | s << 15 | t << 8 | v)).zfill(4)

        return "".join(generate_datum_hex())

    def __init__(self, info, board):
        self.team = info["Team"]
        self.match = info["Match"]
        self.name = info["Name"]
        self.start_time = info["StartTime"]
        self.comments = info["Comments"]
        self.data = info["Data"]

        self.board = board

        self.decoded_data = []

        for t, v, u, s in self.split(self.data):
            self.decoded_data.append((self.board.log(t), v, bool(u)))
