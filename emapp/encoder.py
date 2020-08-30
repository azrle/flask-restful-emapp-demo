from json import JSONEncoder
import sqlite3
import datetime


class ApiResponseJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, sqlite3.Row):
            return {col: o[col] for col in o.keys()}
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()
