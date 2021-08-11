This is project work during the highway to code course from Kajaani Amattikorkeakoulu.
The project was to program an Esp32 development board to send data to Iot platform(asksensors.com).
The sensor module used were BMP280 which measures temperature and pressure, DHT11 which measures temperature and humidity and a PIR 
sensor which detects a motion.

The program sends the measured data to the Iot platform for visualization. All other data are send periodically while the motion detected data is sent whenever the motion sensor detects a motion and resets after some delay.

The files:
BME280.py file is used to read the BME sensor as micropython itself doesn’t have a
library to read BME sensors. urequests.py provides HTTP Library with a similar
interface to python-requests. Particularly well suited for usage with MicroPython to
send http requests,boot.py is a file which initializes the esp32 board and connect it
to the internet via wifi, main.py is the main implementation file.