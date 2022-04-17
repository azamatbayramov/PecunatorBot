import gspread
from all_json import SETTINGS, CREDENTIALS_FILENAME, WORKSHEET_SETTINGS as WS_S

gc = gspread.service_account(filename=CREDENTIALS_FILENAME)

sh = gc.open_by_url(SETTINGS["google_spreadsheet_url"])


def create_necessary_worksheets(sheet: gspread.Spreadsheet):
    existing_worksheets = list(map(lambda s: s.title, sheet.worksheets()))
    for worksheet_name in WS_S["necessary_worksheets"]:
        if worksheet_name not in existing_worksheets:
            sheet.add_worksheet(worksheet_name, WS_S["rows_count"], WS_S["columns_count"])


def clear_all_worksheets(sheet: gspread.Spreadsheet):
    for worksheet in sheet.worksheets():
        worksheet.clear()


def delete_unnecessary_worksheets(sheet: gspread.Spreadsheet):
    for worksheet in sheet.worksheets():
        if worksheet.title not in WS_S['necessary_worksheets']:
            sheet.del_worksheet(worksheet)


def reset_spreadsheet(sheet: gspread.Spreadsheet):
    create_necessary_worksheets(sheet)
    delete_unnecessary_worksheets(sheet)
    clear_all_worksheets(sheet)


reset_spreadsheet(sh)
