# Temperature Monitor

This code implements a temperature monitor to a remote server.  It allows connections from client and reports changes in temperature.

## Installation

The Temperature project in implemented in a virtual python environment using a Makefile.  To install, simply clone this repo and run the appropriate make command.

To set up the virtual environment, make the development job.

```bash
make develop
```

Be sure to activte the virtual environment

```bash
. env/bin/activate
```

## Usage

Before execution, you should edit the src/config.yaml file to update the default configuration values used by the script for server/client.
You have two options for execution: client or server.

For server mode:
```bash
make server
```

In server mode, the program tries to connect to a remote server API that returns current weather conditions based on lat/long information.
It waits for clients to connect, monitors the connections and reports any temperature deltas greater than the delta value in the config.yaml file.
This command does not exit.  You will have to ctrl-c out.

For client mode:
```bash
make client
```

A server needs to be running in order for a client to connect.  Once the client connects, it will immediately start receiving current temperature changes from the server.
Many clients can connect to a single server.  Connections are monitored for health and connection status.
This command does not exit.  You will have to ctrl-c out.

You can also run the server and client on your own.  If your config.yaml file is setup correctly, running the script is simple.

For server mode:
```bash
./src/Temperature server
```
For client mode:
```
./src/Temperature client
```

## Command Line Options

The script contains help for both modes: client and server.  The options and descriptions are available with the -h option.

Two Notes:

In client mode, we only need to know the host:ip to connect to.

In server mode, we need to know the ip:port to bind to.
The host:port of the temperature server.
How often to poll the temperature server.
What change in temperature to report.

## Notes

Most of the time, I start a server using Make.  Then use netcat to interact with the server, modify the current temperature and shutdown the server.
```
netcat localhost 5000
```

From netcat, there are two commands handled by the server:
```
PUSH <temp>
```
and
```
SHUTDOWN
```
