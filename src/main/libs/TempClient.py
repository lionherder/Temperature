import select
import socket
import time
import threading

from libs import Utils

'''
Connects to a server that reports changes in temperature
'''
class TempClient(threading.Thread):

    def __init__(self, ip, port):
        super().__init__()
        self.IP = ip
        self.PORT = port

        self.currentTemp = 0.0
        self.done = False

    def run(self):
        print("Started Client")
        # Set up the socket stuff
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.connect((self.IP, self.PORT))

        # All we really need to do here is check for incoming data.
        while not self.done:
            data = ss.recv(100).decode()
            if (len(data) == 0):
                print("Server disconnected.  Shutting down.")
                ss.close()
                return
            (temp, timestamp) = data.split("@")
            self.currentTemp = temp
            print(temp)
                
            time.sleep(1)

    def alive(self):
        return not self.done

    def getCurrentTemp(self):
        return self.currentTemp

    def shutdown(self):
        self.done = True
