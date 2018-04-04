import pandas as pd
import xlwings as xw

from processor import entry_manager

locations = {"Entries Table Top Left": "J5",
             "Working Entry Table Top Left": "Y5",
             "Scout Comments": "Y5",
             "Import Folder": "C7",
             "Database File": "C10",
             "Filter Match Number": "G7",
             "Filter Team Number": "G10",
             "Filter Scout Name": "G13",
             "Filter Board": "G16",
             "Working Entry Index": "R7",
             "Working Match Number": "R10",
             "Working Team Number": "R13",
             "Working Scout Name": "R16",
             "Working Board": "R19",
             "Working Time Started": "R22",
             "Working Edited": "R25",
             "Working Scout Comments": "Y5"}

log_loc = "B2"

default_sheet_num = 0

default_path = "data/database/data.warp7"

def get_val(wb, loc, sheet_num=default_sheet_num):
    return wb.sheets[sheet_num].range(loc).value

def put_val(wb, loc, val, sheet_num=default_sheet_num):
    wb.sheets[sheet_num].range(loc).value = val

def log(wb, text, sheet_num=default_sheet_num, location=log_loc, append=False):
    if append:
        put_val(wb, location, get_val(wb, location) + text)
    else:
        wb.sheets[sheet_num].range(location).value = text


def new_manager():
    import os
    new_path = os.path.join(os.path.dirname(__file__), "data/database/data.warp7")

    board_path = os.path.join(os.path.dirname(__file__), "data/board/")

    return entry_manager.EntryManager(new_path, board_path)


def remove_entry():

    wb = xw.Book.caller()
    log(wb, "Removing entries ... ")

    # Get inputs
    inputs = {
        "Entry Index": get_val(wb, locations["Working Entry Index"]),
        "Match Number": get_val(wb, locations["Working Match Number"]),
        "Team Number": get_val(wb, locations["Working Team Number"]),
        "Scout Name": get_val(wb, locations["Working Scout Name"]),
        "Board": get_val(wb, locations["Working Board"]),
        "Time Started": get_val(wb, locations["Working Time Started"]),
        "Edited": get_val(wb, locations["Working Edited"])
    }
    # entry_index = get_val(wb, locations["Working Entry Index"]),
    # match_number = get_val(wb, locations["Working Match Number"]),
    # team_number = get_val(wb, locations["Working Team Number"]),
    # scout_name = get_val(wb, locations["Working Scout Name"]),
    # board = get_val(wb, locations["Working Board"]),
    # time_started = get_val(wb, locations["Working Time Started"]),
    # edited = get_val(wb, locations["Working Edited"])

    # TODO call code to remove the entry
    # TODO show next entry in working data table

    log(wb, "Done", append=True)


def revert_to_original():

    wb = xw.Book.caller()
    log(wb, "Reverting to original ... ")

    # Get inputs
    database_file = get_val(wb, locations["Database File"])
    entry_index = get_val(wb, locations["Working Entry Index"]),
    match_number = get_val(wb, locations["Working Match Number"]),
    team_number = get_val(wb, locations["Working Team Number"]),
    scout_name = get_val(wb, locations["Working Scout Name"]),
    board = get_val(wb, locations["Working Board"]),
    time_started = get_val(wb, locations["Working Time Started"]),
    edited = get_val(wb, locations["Working Edited"])

    # TODO call code to revert row in edited entries to original entry
    # TODO reload data
    log(wb, "Done", append=True)


def save_changes():

    wb = xw.Book.caller()
    log(wb, "Saving changes ... ")

    # Get inputs
    database_file = get_val(wb, locations["Database File"])
    entry_index = get_val(wb, locations["Working Entry Index"]),
    match_number = get_val(wb, locations["Working Match Number"]),
    team_number = get_val(wb, locations["Working Team Number"]),
    scout_name = get_val(wb, locations["Working Scout Name"]),
    board = get_val(wb, locations["Working Board"]),
    time_started = get_val(wb, locations["Working Time Started"]),
    edited = get_val(wb, locations["Working Edited"])
    entry_info = wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(expand='table')

    # TODO call code to save changes to db
    log(wb, "Done", append=True)


def previous_in_list():

    wb = xw.Book.caller()
    log(wb, "Showing previous in list ... ")

    # Get inputs
    database_file = get_val(wb, locations["Database File"])
    filtered_table = wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(expand='table')

    # TODO call code to show previous in list
    log(wb, "Done", append=True)


def next_in_list():

    wb = xw.Book.caller()
    log(wb, "Showing next in list ... ")

    # Get inputs
    database_file = get_val(wb, locations["Database File"])
    filtered_table = wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(pd.DataFrame,
                                                                                                     index=False,
                                                                                                     header=False,
                                                                                                     expand='table', )

    data = new_manager()

    working_entry_data = data.next(filtered_table, locations["Working Entry Index"])

    # Update data
    put_val(wb, locations["Working Match Number"], working_entry_data["Match"])


    # TODO call code to show next in list
    log(wb, "Done", append=True)


def add_new_entry():
    wb = xw.Book.caller()
    log(wb, "Adding new entry ... ")
    # Get inputs
    database_file = get_val(wb, locations["Database File"])

    # TODO call code to add a new entry
    # TODO show blank entry
    log(wb, "Done", append=True)


def go_to_beginning():
    wb = xw.Book.caller()
    log(wb, "Going to beginning ... ")

    # Get inputs
    database_file = get_val(wb, locations["Database File"])
    filtered_table = wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(expand='table')

    load_and_show_data()

    # TODO call code to show first entry in list
    log(wb, "Done", append=True)


def clear_filters():
    wb = xw.Book.caller()
    log(wb, "Loading data ... ")

    # Get inputs
    folder_path = get_val(wb, locations["Import Folder"])
    database_file = get_val(wb, locations["Database File"])
    match_number = get_val(wb, locations["Filter Match Number"])
    team_number = get_val(wb, locations["Filter Team Number"])
    scout_name = get_val(wb, locations["Filter Scout Name"])

    # Load data

    data = new_manager()

    # TODO put data on sheet


    log(wb, "Clearing filters ... ")
    put_val(wb, match_number, '')
    put_val(wb, team_number, '')
    put_val(wb, scout_name, '')

    log(wb, "Showing data ... ")
    wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(pd.DataFrame, expand='table',
                                                                                    index=False,
                                                                                    header=False).value = data.filter()
    log(wb, "Done", append=True)


def apply_filters():
    # def parse_filter_number(parseString, listOfNumbers):
    #     if parseString == '':
    #         return listOfNumbers
    #
    #     parseArray = parseString.split(',')
    #
    #     for i in range(len(parseArray)):
    #         parseArray[i] = parseArray[i].replace(' ', '')
    #
    #     numbers = []
    #
    #     for i in parseArray:
    #         if '-' in i:
    #             arr = i.split('-')
    #             for j in listOfNumbers:
    #                 if j >= arr[0] and j <= arr[1]:
    #                     numbers.append(j)
    #
    #         for j in ['>=', '<=', '>', '<']:
    #             if j in i:
    #                 string = int(i.replace(j, ''))
    #                 for k in listOfNumbers:
    #                     if eval(str(k) + str(j) + str(string)):
    #                         numbers.append(k)
    #         try:
    #             for j in listOfNumbers:
    #                 if j == int(i):
    #                     numbers.append(j)
    #         except:
    #             pass
    #     return (numbers)
    #
    # def parse_filter_string(parseString, listOfStrings):
    #     if parseString == '':
    #         return listOfStrings
    #
    #     parseArray = parseString.split(',')
    #
    #     strings = []
    #
    #     for i in parseArray:
    #         for j in listOfStrings:
    #             if '~' in i.strip().lower():
    #                 if i.strip().replace('~', '').lower() in j.strip().lower():
    #                     strings.append(j)
    #             if i.strip().lower() == j.strip().lower():
    #                 strings.append(j)

    def parse_filter_input(parse_string):
        return parse_string.split(",")

    wb = xw.Book.caller()
    log(wb, "Loading data ... ")

    # Get inputs
    folder_path = get_val(wb, locations["Import Folder"])
    database_file = get_val(wb, locations["Database File"])
    match_number = str(get_val(wb, locations["Filter Match Number"]))
    team_number = str(get_val(wb, locations["Filter Team Number"]))
    scout_name = str(get_val(wb, locations["Filter Scout Name"]))
    board = str(get_val(wb, locations["Filter Board"]))

    # Load data
    manager = new_manager()

    match_numbers_for_filter = list(map(int, match_number.split()))
    team_numbers_for_filter = list(map(int, team_number.split()))
    scout_names_for_filter = scout_name.split()

    log(wb, str(list(match_numbers_for_filter)))

    # log(wb, "Filtering data ... ")
    data = manager.filter(match=match_numbers_for_filter,
                          team=team_numbers_for_filter,
                          name=scout_names_for_filter)

    wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).expand().value = []
    #log(wb, "Showing data ... ")
    wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(pd.DataFrame, expand='table',
                                                                                    index=False,
                                                                                    header=False).value = data
    #log(wb, "Done", append=True)


def load_and_show_data():
    from processor import csv_to_database

    wb = xw.Book.caller()
    log(wb, "Loading data ... ")

    # Get inputs
    folder_path = get_val(wb, locations["Import Folder"])
    database_file = get_val(wb, locations["Database File"])

    # Load data
    import os

    db_path = os.path.join(os.path.dirname(__file__), "data/database/data.warp7")
    board_path = os.path.join(os.path.dirname(__file__), "data/board/")
    scan_path = os.path.join(os.path.dirname(__file__), "data/scan")

    csv_to_database.write_unique(db_path, scan_path, board_path)

    data = entry_manager.EntryManager(db_path, board_path)
    # TODO put data on sheet


    log(wb, "Showing data ... ")
    wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(pd.DataFrame, expand='table',
                                                                                    index=False,
                                                                                    header=False).value = data.filter()
    log(wb, "Done", append=True)
