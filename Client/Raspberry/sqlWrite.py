import sqlite3
from queue import Queue
import time

class SqlWrite:
    def __init__(self, data_provider, date, dataType):
        self.con = sqlite3.connect(date + ".sqlite")
        self.cur = self.con.cursor()
        self.dataType = dataType
        self.killed = False

        self.start_writing()
        self.data_provider = data_provider
        self.data_queue = Queue(maxsize=0)

        self.data_provider.bind_queue(self.data_queue)
        self.data_provider.bind_call(self.test)
        self.writeHelper()
        

    def start_writing(self):
        self.cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='"+ self.dataType+"'" )

        #if the count is 1, then table exists
        if not self.cur.fetchone()[0]==1 : {
            self.cur.execute("CREATE TABLE " + self.dataType + "(timestamp real, value real)")
        }

    def write(self):
        while not self.data_queue.empty():
            data = self.data_queue.get().data
            self.cur.execute("INSERT INTO " + self.dataType + " VALUES(?,?)", (data["timestamp"], data["value"]))


    def writeHelper(self):
        while not self.killed:
            self.write()
            self.con.commit()
            time.sleep(0.01)

    def test(self):
        True

    def kill(self):
        self.killed = True
        self.con.close()