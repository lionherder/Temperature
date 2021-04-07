#!/bin/python3.6m

import os
import sys
lib_path = "{}/src/main".format(os.environ.get("PWD"))
sys.path.append(lib_path)

import time
import threading
import argparse
import yaml

from libs import TempServer
from libs import TempClient
from libs import Utils

class Temp_UnitTests(object):

    def __init__(self):
        self.config = Utils.load_config()
        
    def start_client(self):
        testClientConfig = self.config.get('TESTCLIENT', {})
        tc = TempClient.TempClient(testClientConfig.get("IP"),
                                   testClientConfig.get("PORT"))
        
        
if __name__ == "__main__":
    tc = Temp_UnitTests()
    tc_thread = threading.Thread(target=tc.start_client)
    tc_thread.start()
