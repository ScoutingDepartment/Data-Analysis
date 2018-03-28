import pandas as pd
import xlwings as xw

from processor import entry_manager

locations = {"Entries Table Top Left": "J5",
             "Working Entry Table Top Left": "Y1",
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
             "Working Edited": "R25"}

log_loc = "B2"

default_sheet_num = 0

default_path = "data/database/data.warp7"

def get_val(wb, loc, sheet_num=default_sheet_num):
    return wb.sheets[sheet_num].range(loc).value


def put_val(wb, loc, val, sheet_num=default_sheet_num):
    wb.sheets[sheet_num].range(loc).value = val


pass
if True:
    pass

def log(wb, text, sheet_num=default_sheet_num, location=log_loc, append=False):
    if append:
        put_val(wb, location, get_val(wb, location) + text)
    else:
        wb.sheets[sheet_num].range(location).value = text


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
    filtered_table = wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(expand='table')

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

    # TODO call code to show first entry in list
    log(wb, "Done", append=True)


def clear_filters():
    wb = xw.Book.caller()
    log(wb, "Clearing filters ... ")
    # Get inputs
    database_file = get_val(wb, locations["Database File"])

    # TODO call code to get unfiltered database
    # TODO show unfiltered database
    log(wb, "Done", append=True)


def apply_filters():
    wb = xw.Book.caller()
    log(wb, "Applying filters ... ")

    # Get inputs
    database_file = get_val(wb, locations["Database File"])
    match_number = get_val(wb, locations["Filter Match Number"])
    team_number = get_val(wb, locations["Filter Team Number"])
    scout_name = get_val(wb, locations["Filter Scout Name"])
    board = get_val(wb, locations["Filter Board"])

    # TODO call code to get filtered database
    # TODO show filtered database
    log(wb, "Done", append=True)


def load_and_show_data():
    wb = xw.Book.caller()
    log(wb, "Loading data ... ")

    # Get inputs
    folder_path = get_val(wb, locations["Import Folder"])
    database_file = get_val(wb, locations["Database File"])

    # Load data
    import os
    new_path = os.path.join(os.path.dirname(__file__), "data/database/data.warp7")

    data = entry_manager.EntryManager(new_path)
    # TODO put data on sheet


    log(wb, "Showing data ... ")
    wb.sheets[default_sheet_num].range(locations["Entries Table Top Left"]).options(pd.DataFrame, expand='table',
                                                                                    index=False,
                                                                                    header=False).value = data.filter()
    log(wb, "Done", append=True)
