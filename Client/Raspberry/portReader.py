import serial
import threading
import json
import time


class PortReader:
    def __init__(self, port, baud, isRaw = False):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(port, baud)
        self.ser.flush()
        print("Connection established with device in port", port, "with", baud, "baud rate.")
        self.packet_loss = 0
        self.killed = False
        # Start the thread that reads data from the Arduin
        self.thread = threading.Thread(target=self.read_data_from_arduino)
        self.thread.start()
        
        self.binders_queue =[]
        self.binders_call = []
        self.raw_data = isRaw

    def read_data_from_arduino(self):
        while not self.killed:
            # Put the latest data into the queue
            data = SerialData(self.ser.readline(), self.raw_data)
            if (data.lost_packet):
                self.packet_loss += 1
                print("Packet loss on port",self.port ,": ", self.packet_loss)
            else:
                self.new_data(data)
        self.ser.close()

    def bind_queue(self, queue):
        #We any queue given to us to our queue array
        self.binders_queue.append(queue)


    def new_data(self, data):
        #broadcast new data to the all binders
        for binder in self.binders_queue:
            binder.put(data)
        for call in self.binders_call:
            call()

    def bind_call(self, fnc):
        self.binders_call.append(fnc)

    def kill(self):
        self.killed = True
        self.thread.join()

class SerialData:
    def __init__(self, data, isRaw):
        self._raw_data = data
        self.lost_packet = False
        self.timestamp = time.monotonic_ns()
        self.isRaw = isRaw
        self.interpret()


    def interpret(self):
        try:
            data = self._raw_data.decode("utf-8") if self.isRaw else float(self._raw_data.decode("utf-8"))

            self.data = {
                "timestamp": self.timestamp,
                "value": data
                }

                
        except ValueError:
            self.lost_packet = True
        
    def to_json(self):
        return json.dumps(self.data)
    
    def to_list(self):
        return [v for k, v in self.data.items()]
