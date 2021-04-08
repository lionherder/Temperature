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

'''
Test multiple connections to the temperature server
'''
class MultipleConns_UnitTests(object):

    def multiple_clients_unittest(self):
        config = Utils.load_config()
        ts_config = config['TESTSERVER']
        ts_client = config['TESTCLIENT']
        ct = []
        # Start temp server
        st = TempServer.TempServer(ts_config['IP'], ts_config['PORT'], ts_config['TSIP'], ts_config['TSPORT'])
        st.start()
        # Give thin
        time.sleep(1)
        st.push(100.0)
        # Create 15 clients to connect
        for i in range(0, 15):
            local_ct = TempClient.TempClient(ts_client['IP'], ts_client['PORT'])
            local_ct.start()
            ct.append(local_ct)
            time.sleep(.2)

        # Let everything connect and run for 60 seconds
        done = False
        now = time.time()
        while not done:
            print("Thread check")

            # Check server thread
            if (not st.is_alive()):
                print("Server thread dead")
                st.join()

            # Check client threads
            for thread in ct:
                if (not thread.is_alive()):
                    ct.remove(thread)
                    print("Client thread dead")
                    thread.join()
                print(thread.getCurrentTemp())

            # End when clients all are closed
            if (len(ct) == 0):
                done = True
                continue
            
            # Shutdown the server thread
            if (time.time() - now) > 20:
                if (st.is_alive()):
                    print("Shutting down server thread")
                    st.shutdown()
            time.sleep(1)

        print("All threads dead")

if __name__ == "__main__":
    tc = MultipleConns_UnitTests()
    tc.multiple_clients_unittest()
