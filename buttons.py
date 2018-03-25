import xlwings as xw

locations = {"Filter Match Number": "G7",
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


def get_val(wb, loc, sheet_num=0):
    return wb.sheets[sheet_num].range(loc).value


def put_val(wb, loc, val, sheet_num=0):
    wb.sheets[sheet_num].range(loc).value = val


def log(wb, text, location=log_loc, append=False):
    if append:
        put_val(wb, location, get_val(wb, location) + text)
    else:
        wb.sheets[0].range(location).value = text


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
    # TODO call code to remove the entry
    # TODO show next entry in working data table

    log(wb, "Done", append=True)


def revert_to_original():
    wb = xw.Book.caller()
    log(wb, "Reverting to original ... ")
    # TODO call code to revert row in edited entries to original entry
    # TODO reload data
    log(wb, "Done", append=True)


def save_changes():
    wb = xw.Book.caller()
    log(wb, "Saving changes ... ")
    # TODO call code to save changes to db
    log(wb, "Done", append=True)


def previous_in_list():
    wb = xw.Book.caller()
    log(wb, "Showing previous in list ... ")
    # TODO call code to show previous in list
    log(wb, "Done", append=True)


def next_in_list():
    wb = xw.Book.caller()
    log(wb, "Showing next in list ... ")
    # TODO call code to show next in list
    log(wb, "Done", append=True)


def add_new_entry():
    wb = xw.Book.caller()
    log(wb, "Adding new entry ... ")
    # TODO call code to add a new entry
    # TODO show blank entry
    log(wb, "Done", append=True)


def go_to_beginning():
    wb = xw.Book.caller()
    log(wb, "Going to beginning ... ")
    # TODO call code to show first entry in list
    log(wb, "Done", append=True)


def clear_filters():
    wb = xw.Book.caller()
    log(wb, "Clearing filters ... ")
    # TODO call code to get unfiltered database
    # TODO show unfiltered database
    log(wb, "Done", append=True)


def apply_filters():
    wb = xw.Book.caller()
    log(wb, "Applying filters ... ")
    # TODO call code to get filtered database
    # TODO show filtered database
    log(wb, "Done", append=True)


def load_and_show_data():
    wb = xw.Book.caller()
    log(wb, "Loading data ... ")
    # TODO call code to load unique data from csv
    log(wb, "Showing data ... ")
    # TODO show new unfiltered database ? filter ?
    log(wb, "Done", append=True)
