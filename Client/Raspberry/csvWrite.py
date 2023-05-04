import sqlite3
from queue import Queue
import time
from datetime import datetime
import threading
import csv

class CSVWrite:
    def __init__(self, date, closingHour, closingMinute):
        self.path = "db/" + date + "/"
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
        dataHolder["data_writer"] = csvFileWriter(self.path + dataType + ".csv", self.closingHour, self.closingMinute, dataHolder["data_queue"])
        
        dataHolder["data_provider"].bind_queue(dataHolder["data_queue"])
        self.data_providers.append(dataHolder)
        
    def start(self):
        for provider in self.data_providers:
            provider["data_writer"].start()
        while not self.killed:
            now = datetime.now()
            if (now.hour == self.closingHour and now.minute >= self.closingMinute) or (now.hour > self.closingHour):
                self.kill()
            time.sleep(1)
        self.kill()

    def kill(self):
        for provider in self.data_providers:
            provider["data_provider"].killed = True
            provider["data_provider"].kill()
            provider["data_writer"].killed = True

        self.killed = True

class csvFileWriter:
    def __init__(self, path, closingHour, closingMinute, queue):
        self.closingHour = closingHour
        self.closingMinute = closingMinute
        self.path = path
        self.killed = False
        self.queue = queue
        self.thread = threading.Thread(target=self.write)

    def start(self):
        self.thread.start()

    def write(self):
        with open(self.path, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            while not self.killed:
                while not self.queue.empty():
                    data = self.queue.get().data
                    print(data["value"])
                    spamwriter.writerow([data["timestamp"], data["value"]])