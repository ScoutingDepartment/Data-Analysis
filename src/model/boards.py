"""
Parses the board/specs files
"""

import json
import os


class Board:
    """Metadata about the robot scouted and the transmission constants"""

    def __init__(self, specs):
        self.specs = specs

    def __str__(self):
        return str(self.specs)

    def __repr__(self):
        return str(self.specs)

    def id(self):
        """Returns the numeral identifier of the board"""
        return int(self.specs["id"], 16)

    def name(self):
        """Returns the name of the board"""
        return self.specs["board"]

    def alliance(self):
        """Returns the letter of the alliance"""
        return self.specs["alliance"]

    def data_index_from_log(self, log_str):
        """Returns the index from the string id"""
        for i, d in enumerate(self.specs["data"]):
            if d["log"] == log_str:
                return i
        return -1

    def dc(self, index):
        """Gets the data dictionary for a particular constant"""
        d = self.specs["data"]
        if 0 <= index < len(d):
            return d[index]
        else:
            return None

    def log(self, index):
        """Returns the log attribute from the constants index"""
        return self.dc(index)["log"]


class Finder:
    def __init__(self, path):
        idf = open(os.path.join(path, "index.json"), "r")
        index_data = json.load(idf)
        idf.close()

        self.files = index_data["files"]
        self.id_list = list(map(lambda x: int(x, 16), index_data["identifiers"]))

        self.boards = []
        self.names = []
        for file in self.files:
            board_file = open(os.path.join(path, file), "r")
            board_obj = Board(json.load(board_file))
            self.names.append(board_obj.name())
            self.boards.append(board_obj)
            board_file.close()

    def get_board_by_id(self, board_id):
        return self.boards[self.id_list.index(board_id)]

    def get_board_by_name(self, name):
        return self.boards[self.names.index(name)]

    def get_first(self):
        return self.boards[0]


if __name__ == "__main__":
    find = Finder("../data/board")
    board = find.get_board_by_id(int("e3bb3f98", 16))
    print(board)
