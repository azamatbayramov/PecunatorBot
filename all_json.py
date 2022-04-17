"""Module for json file opening"""

import json

SETTINGS = json.load(open("json/settings.json", encoding="utf8"))
CREDENTIALS_FILENAME = "json/credentials.json"
WORKSHEET_SETTINGS = json.load(open("json/worksheet_settings.json", encoding="utf8"))
