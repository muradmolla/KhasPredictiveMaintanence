import asyncio
from queue import Queue
import portReader
import sqlWrite
import sqlite3

#con = sqlite3.connect(date + ".sqlite")
data_provider = portReader.PortReader("COM3", 9600)
sql_write = sqlWrite.SqlWrite(data_provider,"test", "testtype")


try:
    while True:
        True
except KeyboardInterrupt:
    data_provider.kill()
    sql_write.kill()
    print("Server Terminated by the user.")
    exit()