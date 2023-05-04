import asyncio
from queue import Queue
import portReader
import sqlWrite
import sqlite3
import doubleDataHandler
from datetime import datetime

date = datetime.now()

# sqlWrite.SqlWrite(nameofdb, closingHours, closingMinutes)
# program will terminate at closingHours:closingMinutes
sql_write = sqlWrite.SqlWrite(date.strftime("%Y_%m_%d"), 20, 27)


testProvider = portReader.PortReader("COM4", 9600)
sql_write.bind("test", testProvider)

# PORT, BAUD, isRawData
testDoubleProvider = portReader.PortReader("COM8", 9600, True)

doubleDataHandler = doubleDataHandler.DoubleDataHandler(testDoubleProvider)
sql_write.bind("doubleData1", doubleDataHandler.mockProviderA)
sql_write.bind("doubleData2", doubleDataHandler.mockProviderB)
doubleDataHandler.start()


try:
    sql_write.start()
except Exception as e:
    sql_write.kill()
    doubleDataHandler.killed = True
    doubleDataHandler.kill()
    exit()