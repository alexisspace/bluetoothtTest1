import sys
import bluetooth
import time

# execfile("client_cmd_send.py")

# Application specific commands
READ_CMD = "r"      # Issued for request ADC measurements
RELEASE_CMD = "b"   # Issued for disconnect from server (does not finish server execution)
EXIT_CMD = "x"      # Issued for order server to finnish execution
START_CMD = "s"     # Not used by client

# Application constants
DATA_LENGTH = 26 # Message length coming from server


# Sumulation of connection and disconnection from server
# Connect and disconnect NUMBER_OF_CONN times
NUMBER_OF_CONN = 2
for k in range(NUMBER_OF_CONN):

    # Search for  "Plate Server" service on the Pi
    uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
    serviceName = "Plate Server"
    print "Searching service \"%s\"" % serviceName
    service_matches = bluetooth.find_service( name = serviceName )

    # Check if no server was encountered
    print "Services matches: ", len(service_matches)
    if len(service_matches) == 0:
        print "Couldn't find the \"%s\" service" % serviceName 
        print "Terminating program"
        sys.exit(0)

    # See if some of the services is the one we are looking for
    serviceFound = False
    for elem in service_matches:
        if elem['name'] == serviceName:
            serviceFound = True
            port = elem["port"]
            name = elem["name"]
            host = elem["host"]
            break

    if serviceFound == False:
        print "Couldn't find the \"%s\" service" % serviceName 
        print "Terminating program"
        sys.exit(0)

    # Create a comm socket and conect to server
    print "Connecting to \"%s\" on %s" % (name, host)
    sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((host, port))
    # Delay to allow accept onnecting
    print "Delay to accept connection"
    delayTime = 2
    time.sleep(delayTime)
    # Send NUMBER_OF_REQUESTS test commands
    NUMBER_OF_REQUESTS = 2
    for kk in range(NUMBER_OF_REQUESTS):
        # Send read command
        sock.send("r")
        data = sock.recv(DATA_LENGTH)
        print "Received data is: %s" % data
        time.sleep(1)

    if k == NUMBER_OF_CONN - 1:
        # Number of test connection achieved, now send EXIT_CMD
        sock.send(EXIT_CMD)
    else:
        # Disconnect from actual socket
        sock.send(RELEASE_CMD)

    # Close socket
    sock.close()

# Terminate program
print "Client program terminated"