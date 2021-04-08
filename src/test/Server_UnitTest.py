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
from libs import Utils

class Server_UnitTests(object):

    def __init__(self):
        self.config = Utils.load_config()
        self.ts = None
        
    def start(self):
        testServerConfig = self.config.get('TESTSERVER', {})
        self.ts = TempServer.TempServer(testServerConfig.get("IP"),
                                        testServerConfig.get("PORT"),
                                        testServerConfig.get("TSIP"),
                                        testServerConfig.get("TSPORT"),
                                        testServerConfig.get("POLLTIME"),
                                        testServerConfig.get("DELTA"))
        print("Starting server.")
        self.ts.start()
        print("Sleeping for a 10 seconds.")
        time.sleep(10)
        if (not self.ts.is_alive()):
            print("Server crashed")
            exit(1)
        print("Shutting down server.")
        self.ts.shutdown()
        self.ts.join()

if __name__ == "__main__":
    tc = Server_UnitTests()
    tc.start()
    

