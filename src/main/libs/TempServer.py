import json
import requests
import select
import socket
import time

''' A tcp server that reports changes in temperature to a bound port.
Remote clients can connect to receive updates.  Simple and to the
point using low level networking.
'''

class TempServer(object):

    def __init__(self, ip, port, ts_ip, ts_port, poll_time=1, delta=0.0):
        self.IP = ip
        self.PORT = port
        self.TS_IP = ts_ip
        self.TS_PORT = ts_port
        self.POLL_TIME = poll_time
        self.DELTA = delta  # Change before an update is done

        self.input_conns = []
        self.lastTemp = 0.0

        print("IP: {}".format(self.IP))
        print("PORT: {}".format(self.PORT))
        print("TSIP: {}".format(self.TS_IP))
        print("TSPORT: {}".format(self.TS_PORT))
        print("POLLTIME: {}".format(self.POLL_TIME))
        print("DELTA: {}".format(self.DELTA))

        
    '''
    Check if the temperature has changed enough to push out another
    update
    '''

    def update_temp(self):
        '''
        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        querystring = {"q":"San Jose, CA ,US","lat":"37.3382","lon":"-121.8863","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}

        headers = {
            'x-rapidapi-key': "36d1aa7a52msh924d0f83f2384e0p17bacejsn933e0b81622d",
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        
        print(response.text)
        '''

        # Canned response
        resp = json.loads('{"coord":{"lon":-121.895,"lat":37.3394},"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"base":"stations","main":{"temp":288.89,"feels_like":287.96,"temp_min":287.04,"temp_max":290.93,"pressure":1021,"humidity":55},"visibility":10000,"wind":{"speed":8.23,"deg":330},"clouds":{"all":90},"dt":1617495941,"sys":{"type":1,"id":5845,"country":"US","sunrise":1617457765,"sunset":1617503500},"timezone":-25200,"id":5392171,"name":"San Jose","cod":200}')

        temp = resp['main']['temp']

        if (abs(time.time() - self.lastTemp) > self.DELTA):
            self.lastTemp = temp
            return True
        return False

    '''
    Main routine for handling and updating clients
    '''
    def start(self):
        # Set up the server socket stuff
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM | socket.SOCK_NONBLOCK)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.bind((self.IP, self.PORT))
        ss.listen(10)

        while True:
            # Check for change in time
            doUpdate = self.update_temp()
            msg = "{} @ {}".format(self.lastTemp, time.ctime())
            
            # Check for any new connections
            print("Checking for new connections")
            (readable, writable, exceptional) = select.select([ss],[],[], 0)
            # print(len(readable), len(writable), len(exceptional))
            for newConn in readable:
                (conn, addr) = ss.accept()
                conn.setblocking(0)
                self.input_conns.append(conn)
                print ('Connection Address is: ' , addr)
                conn.send(msg.encode())

            # Update all our connections
            for conn in self.input_conns:
                print("Checking connection: " + str(conn))
                (readable, writable, exceptional) = select.select([conn],[conn],[conn], 0)
                # print(len(readable), len(writable), len(exceptional))
                # If it's exceptional, kill the connection
                if (len(exceptional) > 0):
                    print("Client disconnected")
                    self.input_conns.remove(conn)
                    conn.close()
                    continue
                
                # We should only get readable data on client
                # disconnect.  If we do get data, toss it
                if (len(readable) > 0):
                    data = conn.recv(1024)
                    if (len(data) == 0):
                        print("Client disconnected")
                        self.input_conns.remove(conn)
                        conn.close()
                        continue
                    else:
                        if (data.index("PUSH")):
                            (command, temp) = data.split(" ")
                        print(command, temp)

                # Check if the connection is writable.  If it's all
                # good, write the data
                if ((len(writable) > 0) and doUpdate):
                    conn.send(msg.encode())

            time.sleep(self.POLL_TIME)
