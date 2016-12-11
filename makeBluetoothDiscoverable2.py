import subprocess
import time
import signal
import select
import sys
import string

global discover
discover = True
    

# Create system subprocess to control bluetooth
proc = subprocess.Popen(['/bin/sh'],
        shell = True,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
        )



# Open the bluetooth config shell
proc.stdin.write('bluetoothctl\n')
print proc.stdout.readline()

# Periodically make Bluetooth discoverable 
while discover == 1:
    proc.stdin.write('discoverable on\n')
    print proc.stdout.readline()
    print proc.stdout.readline()

    # Dealy before new activation of the bluetooth discoverable mode
    delayT = 30 
    for k in range(delayT):
        obj = []
        obj = select.select([sys.stdin], [], [], 0)
        if obj[0]:
            line = sys.stdin.readline() 
            print "CHILD stdin: %s" % line
            if string.find(line, "x") != -1:
                proc.stdin.write('discoverable off\n')
                time.sleep(1)
                print proc.stdout.readline()
                print proc.stdout.readline()
                proc.stdin.write('quit\n')
                print proc.stdout.readline()
                time.sleep(1)
                discover = False
        if discover:
            time.sleep(1) # Wait 1 seconds to try again
        else:
            break

print "CHILD: exiting"
print proc.communicate() # End process


