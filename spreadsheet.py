import json
import os
import gspread

GC = gspread.service_account(filename="json/credentials.json")
SHEET = GC.open_by_url(os.environ["GOOGLE_SPREADSHEET_URL"])
WS_S = json.load(open("json/worksheet_settings.json", encoding="utf8"))


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


def fill_worksheets(sheet: gspread.Spreadsheet):
    for worksheet_name in WS_S["necessary_worksheets"]:
        sheet.worksheet(worksheet_name).update("A1:Z1", [WS_S["worksheets_headers"][worksheet_name]])


def reset_spreadsheet(sheet: gspread.Spreadsheet):
    create_necessary_worksheets(sheet)
    delete_unnecessary_worksheets(sheet)
    clear_all_worksheets(sheet)
    fill_worksheets(sheet)


def is_opened_spreadsheet_valid():
    worksheets_titles = [sheet.title for sheet in SHEET.worksheets()]
    return sorted(worksheets_titles) == sorted(WS_S["necessary_worksheets"])


if not is_opened_spreadsheet_valid():
    reset_spreadsheet(SHEET)