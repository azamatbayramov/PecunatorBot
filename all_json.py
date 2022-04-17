"""Module for json file opening"""

import json

SETTINGS = json.load(open("settings.json", encoding="utf8"))
