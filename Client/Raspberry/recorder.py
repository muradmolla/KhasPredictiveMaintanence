import asyncio
from queue import Queue
import portReader
import sqlWrite
import sqlite3
import csvWrite
import doubleDataHandler
from datetime import datetime

date = datetime.now()

# sqlWrite.SqlWrite(nameofdb, closingHours, closingMinutes)
# program will terminate at closingHours:closingMinutes
#sql_write = sqlWrite.SqlWrite(date.strftime("%Y_%m_%d"), 20, 27)


csv_write = csvWrite.CSVWrite(date.strftime("%Y_%m_%d"), 1, 59)


testProvider = portReader.PortReader("COM3", 9600)
#sql_write.bind("test", testProvider)

csv_write.bind("test", testProvider)

# PORT, BAUD, isRawData
testDoubleProvider = portReader.PortReader("COM7", 9600, True)

doubleDataHandler = doubleDataHandler.DoubleDataHandler(testDoubleProvider)
csv_write.bind("doubleData1", doubleDataHandler.mockProviderA)
csv_write.bind("doubleData2", doubleDataHandler.mockProviderB)
#doubleDataHandler.start()


try:
    #sql_write.start()
    csv_write.start()
except Exception as e:
    #csv_write.killed = True
    csv_write.kill()
    #sql_write.kill()
    #doubleDataHandler.killed = True
    #doubleDataHandler.kill()
    exit()