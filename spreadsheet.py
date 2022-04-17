import gspread
from all_json import SETTINGS, CREDENTIALS_FILENAME

gc = gspread.service_account(CREDENTIALS_FILENAME)

sh = gc.open_by_url(SETTINGS["google_spreadsheet_url"])

necessary_worksheets = [
    ("Payments", 100, 10),
    ("Users", 100, 10),
    ("Resets", 100, 10)
]


def create_necessary_worksheets(sheet: gspread.Spreadsheet):
    for worksheet in necessary_worksheets:
        sheet.add_worksheet(*worksheet)


def delete_all_worksheets(sheet: gspread.Spreadsheet):
    for worksheet in sheet.worksheets():
        sheet.del_worksheet(worksheet)
