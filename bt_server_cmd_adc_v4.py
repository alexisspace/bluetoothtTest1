import bluetooth
import time
import os
import subprocess
import signal
import select
from gpiozero import MCP3008

# Fixed application commands
READ_CMD = "r"     # To read ADC channels
RELEASE_CMD = "b"  # To release actual connection
EXIT_CMD = "x"     # To stop program
START_CMD = "s"    # To start and keep running the program

# Configure ADC
load_cell1 = MCP3008(0)     # Channel 0
load_cell2 = MCP3008(1)     # Channel 1

# Configure connection to bluetooth driver
port = 6; # Communication port: Can be any number from 1 to 30
cmd = START_CMD
while cmd != EXIT_CMD:
    
    # Make bluetooth discoverable
    proc = subprocess.Popen(['sudo python makeBluetoothDiscoverable2.py'],
    shell = True,
    preexec_fn = os.setsid, 
    stdin = subprocess.PIPE, 
#    stdout = subprocess.PIPE
    )   # Create system subprocess

    
    # Create communication socket
    server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    server_sock.bind(("",port))     # Bind socket to system port "port"
    server_sock.listen(1)           # Accept up to one (1) connection
    print "Listening on port %d" % port

    # Advertise service "Plate Server"
    print "starting advertising"
    uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
    #bluetooth.advertise_service( server_sock, "Plate Server")
    bluetooth.advertise_service( server_sock, "Plate Server",
                       service_id = uuid,
                       service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
                       profiles = [ bluetooth.SERIAL_PORT_PROFILE ], 
    #                   protocols = [ bluetooth.OBEX_UUID ] 
    )

    # Wait for an incomming conection
    print "Waiting for client connection"
    client_sock,address = server_sock.accept()
    print "Accepted connection from: ",address
    
    # Stop advertising
    print "Stoping advertising"
    bluetooth.stop_advertising(server_sock)

    # Wait for commands
    while True:
        cmd = client_sock.recv(1)
        print "command is: %s" % cmd
        if cmd == READ_CMD:
            # Take ADC measurements
            # Send meassurements back to client
            lcv1 = load_cell1.value
            lcv2 = load_cell2.value
            s = "lcv1 = %05.2f; lcv2 = %05.2f" % (lcv1,lcv2) # 26 characters 
            client_sock.send(s)
        if cmd == RELEASE_CMD:
            # Release connection from actual client and wait for another
            break
        if cmd == EXIT_CMD:
            # Exit program, stop executing
            break
        if len(cmd) == 0:
            # Connection lost or closed from client
            break
    # Close actual communication sockets and wait for
    # another connection
    client_sock.close()
    server_sock.close()
    print "Disconnected from: ", address
    print "Send command to finish bluetooth process"
    proc.stdin.write('x\n')
    time.sleep(2)
    proc.communicate() # End process



# If last command was EXIT_CMD then terminate execution of the program

print("Program termitated")
