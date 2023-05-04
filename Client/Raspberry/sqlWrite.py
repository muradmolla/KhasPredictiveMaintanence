import sqlite3
from queue import Queue
import time
from datetime import datetime

class SqlWrite:
    def __init__(self, date, closingHour, closingMinute):
        self.con = sqlite3.connect("db/" + date + ".sqlite")
        self.cur = self.con.cursor()
        self.killed = False
        self.data_providers = []

        self.closingHour = closingHour
        self.closingMinute = closingMinute

    def bind(self, dataType, dataProvider):
        dataHolder = {
            "dataType": dataType,
            "data_provider": dataProvider,
            "data_queue": Queue(maxsize=0)
        }
        dataHolder["data_provider"].bind_queue(dataHolder["data_queue"])
        self.data_providers.append(dataHolder)
        
    def start(self):
        for provider in self.data_providers:
            self.cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='"+ provider["dataType"]+"'" )

            #if the count is 1, then table exists
            if not self.cur.fetchone()[0]==1 : {
                self.cur.execute("CREATE TABLE " + provider["dataType"] + "(timestamp real, value real)")
            }
        self.writeHelper()

    def write(self, provider):
        while not provider["data_queue"].empty():
            data = provider["data_queue"].get().data
            self.cur.execute("INSERT INTO " + provider["dataType"] + " VALUES(?,?)", (data["timestamp"], data["value"]))

    def writeHelper(self):
        while not self.killed:
            for provider in self.data_providers:
                self.write(provider)
            self.con.commit()
            now = datetime.now()
            if (now.hour == self.closingHour and now.minute >= self.closingMinute) or (now.hour > self.closingHour):
                self.kill()
            time.sleep(0.01)

    def kill(self):
        for provider in self.data_providers:
            provider["data_provider"].kill()
        self.killed = True
        self.con.close()