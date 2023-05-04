from queue import Queue
import time
import threading

class DoubleDataHandler:
    def __init__(self, dataProvider):
        self.mockProviderA = DoubleDataProvider(self)
        self.mockProviderB = DoubleDataProvider(self)

        self.thread = threading.Thread(target=self.writeHelper)

        self.killed = False

        dataHolder = {
            "data_provider": dataProvider,
            "data_queue": Queue(maxsize=0)
        }
        dataHolder["data_provider"].bind_queue(dataHolder["data_queue"])
        self.provider = dataHolder

    
    def start(self):
        self.thread.start()

    def write(self):
        while not self.provider["data_queue"].empty():
            serialData = self.provider["data_queue"].get()
            selector = serialData.data["value"][0]
            try:
                serialData.data["value"] = float(serialData.data["value"][1:])
                if (selector == 'a'):
                    self.mockProviderA.queue.put(serialData)
                elif(selector == 'b'):
                    self.mockProviderB.queue.put(serialData)
                else:
                    print("Packet loss on dual value port")
            except ValueError:
                print("Packet loss on dual value port")
            


    def writeHelper(self):
        while not self.killed:
            self.write()
            time.sleep(0.01)

    def kill(self):
        self.killed = True
        self.provider["data_provider"].killed = True
        self.provider["data_provider"].kill()
        self.thread.join()


class DoubleDataProvider:
    def __init__(self, handler):
        self.handler = handler
        self.killed = False

    def bind_queue(self,queue):
        self.queue = queue

    def kill(self):
        self.handler.killed = True
        self.handler.kill()