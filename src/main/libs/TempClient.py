import select
import socket
import time

'''
Connects to a server that reports changes in temperature
'''
class TempClient(object):

    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port

        self.currentTemp = 0.0

    def start(self):
        # Set up the socket stuff
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.connect((self.IP, self.PORT))

        # All we really need to do here is check for incoming data.
        while True:
            data = ss.recv(100).decode()
            if (len(data) == 0):
                print("Server disconnected.  Shutting down.")
                ss.close()
                return

            (temp, timestamp) = data.split("@")
            print(temp)
                
            time.sleep(1)

    def getCurrentTemp(self):
        return self.currentTemp
