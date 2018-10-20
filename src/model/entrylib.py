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
                yield str(hex(u << 15 | s << 14 | t << 8 | v))[2:].zfill(4)

        return "".join(generate_datum_hex())

    def __init__(self, info, board_finder):
        self.team = info["Team"]
        self.match = info["Match"]
        self.name = info["Name"]
        self.start_time = info["StartTime"]
        self.comments = info["Comments"]
        self.encoded_data = info["Data"]
        self.decoded_data = []

        self.board = board_finder.get_board_by_name(info["Board"])

        try:
            self.decode()
        except TypeError:
            print("Error!!!")
            print("match: ", self.match)
            print("team: ", self.team)
            print("board: ", self.board.name())
            print()

    def decode(self):
        self.decoded_data = []
        for t, v, u, s in self.split(self.encoded_data):
            try:
                self.decoded_data.append([self.board.log(t), bool(s), v, bool(u)])
            except TypeError:
                print(t, v, u, s)
                raise TypeError()

        return self.decoded_data

    def encode(self):
        def generate_numerical_tuple():
            for tt, ss, vv, uu in self.decoded_data:
                yield (self.board.data_index_from_log(tt), int(vv), int(uu), int(ss))

        self.encoded_data = self.join(generate_numerical_tuple())

        return self.encoded_data

    def look(self, type_str):
        r = []
        for tt, ss, vv, uu in self.decoded_data:
            if tt == type_str and not uu:
                r.append(vv)
        return r

    def count(self, type_str):
        return len(self.look(type_str))

    def final_value(self, type_str, default=0):
        looked_list = self.look(type_str)
        if looked_list:
            return looked_list[-1]
        return default
