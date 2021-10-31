# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import threading
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


import socket
TCP_IP = '192.168.0.116'
TCP_PORT = 50
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# SETUP
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

# set up button
button = digitalio.DigitalInOut(board.D26)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


# math to convert temp sensor voltage into *C
def ConvertTemp(data):
    temp = data - 0.5
    temp = temp / 0.01
    return round(temp, 2)


# interval for each new threads, default 10 = 10seconds runtime interval
interval = 10


# for cycling between intervals, for button
def cycle():
    global interval
    if interval == 10:
        interval = 5
    elif interval == 5:
        interval = 1
    else:
        interval = 10
    return interval


def print_time_thread():  # thread that prints readings from ADC
    global ADC, LDR, runtime, interval
    thread = threading.Timer(interval, print_time_thread)
    thread.daemon = True  # Daemon threads exit when the program does
    thread.start()
    # runtime
    print((str(round(time.time() - starttime)) + "s").ljust(9, ' '),
          # temp adc
          str(ADC.value).ljust(14, ' '),
          # temp C
          (str(ConvertTemp(ADC.voltage)) + "C").ljust(9, ' '),
          # light resistor reading
          LDR.value)


if __name__ == "__main__":
    print("Runtime   Temp Reading   Temp      Light Reading")
    starttime = time.time()
    print_time_thread()

    while True:
        if button.value == False:
            s.send('a')
