import xlwings as xw

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


def get_val(wb, loc, sheet_num=default_sheet_num):
    return wb.sheets[sheet_num].range(loc).value


def put_val(wb, loc, val, sheet_num=default_sheet_num):
    wb.sheets[sheet_num].range(loc).value = val


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
    entry_manager = EntryManager
    # TODO put data on sheet


    log(wb, "Showing data ... ")
    wb.sheets[sheet_num].range("J5")

    log(wb, "Done", append=True)


def parseFilterNumber(parseString, listOfNumbers):
    parseArray = parseString.split(',')

    for i in range(len(parseArray)):
        parseArray[i] = parseArray[i].replace(' ', '')

    numbers = []

    for i in parseArray:
        if '-' in i:
            arr = i.split('-')
            for j in listOfNumbers:
                if j >= arr[0] and j <= arr[1]:
                    numbers.append(j)

        for j in ['>=', '<=', '>', '<']:
            if j in i:
                string = int(i.replace(j, ''))
                for k in listOfNumbers:
                    if eval(str(k) + str(j) + str(string)):
                        numbers.append(k)
        try:
            for j in listOfNumbers:
                if j == int(i):
                    numbers.append(j)
        except:
            pass
    return (numbers)
