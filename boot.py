# import libraries for garbage collection, python socket api for web server
try:
    import usocket as socket
except:
    import socket
import gc
# import network library to connect to wi-fi and pin class from machine module
import network
from machine import Pin
import dht
import esp

esp.osdebug(None)
gc.collect()
# provide access point credentials
# SSID name and Password
ssid = ''
password = ''
# set esp32 as wifi station
station = network.WLAN(network.STA_IF)
# activate station and connect to the network
station.active(True)
station.connect(ssid, password)
# connection test
while station.isconnected() == False:
    pass
# printing on connection success and printing interface parameters
print('Connection successful')
print(station.ifconfig())
