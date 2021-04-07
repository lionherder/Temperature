#!/bin/python3.6m

import os
import sys
lib_path = "{}/src/main".format(os.environ.get("PWD"))
print(lib_path)
sys.path.append(lib_path)

import time
import threading
import argparse
import yaml

from libs import TempServer
from libs import TempClient

class Server_Thread(object):

    def __init__(self):
        self.config = {}
        # This counts on this service being run from make
        configFilePath = "{}/config.yaml".format(os.environ.get('PWD'))
        # Load the configuration file and set the defaults for the code
        try:
            print(configFilePath)
            with open(configFilePath) as file:
                self.config = yaml.load(file)
                print(self.config)
        except Exception as e:
            print(e)
            print("Warning: No 'config.yaml' present.")
        
    def start_server(self):
        testServerConfig = self.config.get('TESTSERVER', {})
        ts = TempServer.TempServer(testServerConfig.get("IP"),
                                   testServerConfig.get("PORT"),
                                   testServerConfig.get("TSIP"),
                                   testServerConfig.get("TSPORT"),
                                   testServerConfig.get("POLLTIME"),
                                   testServerConfig.get("DELTA"))
        ts.start()

if __name__ == "__main__":
    tc = Server_Thread()
    print("Starting server...")
    serverThread = threading.Thread(target=tc.start_server)
    serverThread.start()
    serverThread.join()

