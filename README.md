# mini nmap
This Python script provides some of the core functionalities of the popular nmap network exploration tool. The script can check the status of specific ports, measure the latency to a given host and port, and perform basic HTTP GET and POST requests to simulate a curl command.

<br>

## Features
- Port Status Check: Verify if specific ports are open on a target IP address.
- Latency Measurement: Calculate the response time (latency) for connecting to a specified IP address and port.
- HTTP Requests: Send simulated GET and POST HTTP requests to a specified IP address and port.

<br>

## Usage
To execute the script, use the following command syntax:

```shell
python nmap.py [command] [arguments]
```

### Available Commands
1. Status Check:
Check the status of one or more ports on a target IP address. 
    ```shell
    python nmap.py -status [ip address] [port1] [port2] ... [portN]
    python nmap.py -status [ip address] -r [start port] [end port]
    ```

2. Latency Measurement:
Calculate the response time to connect to a specific IP address and port.
    ```shell
    python nmap.py -latency [ip address] [port]
    ```
   
3. Simulated HTTP Requests:
Send GET or POST HTTP requests to a specific IP address and port.
    ```shell
    python nmap.py -curl [ip address] [port] -GET [id]
    python nmap.py -curl [ip address] [port] -POST [name] [age]
    ```
