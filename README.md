# Prac 6 EEE3095S
## Sensor Node ##
LXXHSI007 & VBNREE001

This is the code for our client side Pi

## Scripts ##
### adc.py ###
This script connects to the Server node, through 2 TCP connections with the tcp_server.py and webserver.py.
The Pi will be connected to a breadboard with a temperature and light sensor. (Unchanged circuit board from Prac 4).
With the use of timed threads, every 10 seconds data will be read from the ADC, converted, and formatted. The formatted data will be printed to the console and sent to tcp_server.py.
With the connection with the webserver, the node is able to receive commands such as Sensor On, Sensor Off and a Status check.


## Here are some screenshots of the logs from Balena: ##
Server Pi:
![server_logs](https://user-images.githubusercontent.com/53212860/140182339-c578249c-edb5-4548-80e4-2d5ad15a21f8.png)

Sensor Node Pi:
![client_logs](https://user-images.githubusercontent.com/53212860/140182363-d8ccdf27-51f5-4c0d-a0bb-c5c96611d2aa.png)
