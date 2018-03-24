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

    def data_index(self, str_id):
        """Returns the index from the string id"""
        for i, d in enumerate(self.specs["data"]):
            if d["id"] == str_id:
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


def find(path, board_id):
    idf = open(os.path.join(path, "index.json"), "r")
    index_data = json.load(idf)
    idf.close()

    files = index_data["files"]
    ids = list(map(lambda x: int(x, 16), index_data["identifiers"]))

    board_file = open(os.path.join(path, files[ids.index(board_id)]), "r")
    board_data = json.load(board_file)
    board_file.close()
    return Board(board_data)


if __name__ == "__main__":
    board = find("../data/board", int("e3bb3f98", 16))
    print(board)
