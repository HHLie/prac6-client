import socket
import sys
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from datetime import datetime

################TCP SEND SETUP###########################

#TODO Add code to setup the tcp connection with the correct IP and same port as the tcp_server on the other pi
    #Test this locally before trying to deploy via balena using test messages instead of ADC values
    #Use localmode when deploying to balena and use the advertised local address (using public IPs is possible but more complicated to configure due to the security measures BalenaOS imposes by default.  These are a good thing for real world deployment but over complicate the prac for the immediate purposes
import socket

#the tcp setup for the TCP server

TCP_IP = '192.168.0.116'
TCP_PORT = 5003
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#the tcp setup for the webserver
web_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web_s.settimeout(0.000001)

#####
#connect to servers
connected = False
while not connected:
    try:
        print("attempting to connect to web server")
        web_s.connect(('192.168.0.116', 5050))
        print("attempting to connect to tcp server")
        s.connect((TCP_IP, TCP_PORT))
        connected = True
    except Exception as e:
        time.sleep(5)
        pass
##################ADC Setup##############################

#TODO using the adafruit circuit python SPI and MCP libraries setup the ADC interface
#Google will supply easy to follow instructions
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
ADC = AnalogIn(mcp, MCP.P1)

# create an analog input channel on pin 1
LDR = AnalogIn(mcp, MCP.P2)

def ConvertTemp(data):
    temp = data - 0.5
    temp = temp / 0.01
    return round(temp, 2)
#########################################################

print("Sensor Node it awake\n")     #Print statements to see what's happening in balena logs
#f.write("Sensor Node it awake\n")   #Write to file statements to see what's happening if you ssh into the device and open the file locally using nano
#f.flush()
s.send(b'Sensor Node it awake\n')   #send to transmit an obvious message to show up in the balena logs of the server pi


sensor_ONOFF = True
while(True):
    #TODO add code to read the ADC values and print them, write them, and send them
    func_data = '0'
    try:
        func_data = web_s.recv(20).decode()
    except socket.timeout as e:
        pass
    if func_data == '1':
        sensor_ONOFF = True
    elif func_data == '2':
        sensor_ONOFF = False
    elif func_data == '3':
        web_s.send(str(sensor_ONOFF).encode())
    elif func_data == '5':
        sensor_ONOFF = not sensor_ONOFF
        print(sensor_ONOFF)
    if sensor_ONOFF == True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        data_str = (str(current_time)).ljust(12, ' ')
        data_str = data_str + str(ADC.value).ljust(10, ' ')
        data_str = data_str + (str(ConvertTemp(ADC.voltage)) + "C").ljust(9, ' ')
        data_str = data_str + str(LDR.value)
        print(data_str)
        s.send(data_str.encode())
        time.sleep(9.9)
