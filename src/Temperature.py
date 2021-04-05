#!/bin/python3.6m

import argparse
import yaml

from libs import TempServer
from libs import TempClient

if __name__ == '__main__':
    config = {}

    # Load the configuration file and set the defaults for the code
    try:
        with open(r'src/config.yaml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            print(config)
    except Exception:
        print("Warning: No 'config.yaml' present.")
        
    serverConfig = config.get('SERVER', {})
    clientConfig = config.get('CLIENT', {})

    parser = argparse.ArgumentParser(description='Temperature Server/Client',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparsers = parser.add_subparsers(title="Runtime Modes", dest="mode")

    parser_server = subparsers.add_parser("server", help="Server Mode")
    parser_server.add_argument("--ip", help="Server ip", default=serverConfig.get('IP', '127.0.0.1'), type=str, required=False)
    parser_server.add_argument("--port", help="Server port", default=serverConfig.get('PORT', 5000), type=int, required=False)
    parser_server.add_argument("--tsip", help="Temperature server IP", default=serverConfig.get('TSIP', '127.0.0.1'), type=str, required=False)
    parser_server.add_argument("--tsport", help="Temperature server port", default=serverConfig.get('TSPORT', 5000), type=str, required=False)
    parser_server.add_argument("--polltime", help="Interval to refresh temperature", default=serverConfig.get('POLLTIME', 3), type=int)
    parser_server.add_argument("--delta", help="Change in temp before update", default=serverConfig.get('DELTA', 0.05), type=int)

    parser_client = subparsers.add_parser("client", help="Client Mode")
    parser_client.add_argument("--ip", help="Client ip", type=str, default=clientConfig.get('IP', '127.0.0.1'), required=False, )
    parser_client.add_argument("--port", help="Client port", type=int, default=clientConfig.get('PORT', 5000), required=False)

    args = parser.parse_args()
    # print(args)

    if (not args.mode):
        parser.print_help()

    if (args.mode == "server"):
        ts = TempServer.TempServer(args.ip, args.port, args.tsip, args.tsport, poll_time=args.polltime, delta=args.delta)
        ts.start()
    elif (args.mode == "client"):
        ts = TempClient.TempClient(args.ip, args.port)
        ts.start()
    else:
        pass

    
