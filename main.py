from machine import Pin, I2C
from time import sleep
import BME280
import time
import urequests
global motion
motion = False

# pin for DHT11 and PIR sensor
sensor = dht.DHT11(Pin(2))
pir = Pin(14, Pin.IN)

# ESP32 - Pin assignment for BME280 sensor
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=10000)


# Get the readings from BME and DHT sensors
def read_bme_dht():
    global dht_temp, temp, hum, dew, pres
    dht_temp = temp = hum = dew = pres = 0
    # sleep(2)
    # BME280 measurements. Provided sensor was Bmp280
    # only measure temperature and pressure
    bme = BME280.BME280(i2c=i2c)
    temp = bme.temperature
    pres = bme.pressure

    # DHT to measure temperature and humidity
    # Dew point calculated using
    sensor.measure()
    hum = sensor.humidity()
    dht_temp = sensor.temperature()


# motion detection and interrupt with PIR
# Interrupt handling function
def handle_interrupt(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin


# Interrupt caused by motion sensor module
pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
# time variables used if motion detected
motion_start = None
motion_time = 5000  # delay in ms after which motion is set to false


# openWeather api. function returns current temperature of Helsinki
def get_openweather_temp():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "*********"  # openweather API key
    CITY_NAME = "Helsinki"
    URL = BASE_URL + "q=" + CITY_NAME + "&appid=" + API_KEY

    response = urequests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temp_open = main['temp']-273.15
    return temp_open


# Asksensor setup
ASKSENSOR_BASE = 'https://api.asksensors.com/write/'
ASKSENSOR_API_1 = '*******'  # API write key for sensor_1
ASKSENSOR_API_2 = '*******'  # API write key for sensor_2
ASK_URL_1 = ASKSENSOR_BASE + ASKSENSOR_API_1
ASK_URL_2 = ASKSENSOR_BASE + ASKSENSOR_API_2

# update interval for sending data to asksensors platform
UPDATE_TIME_INTERVAL = 60000*30  # in ms ## 30 seconds used in demo
last_update = time.ticks_ms()

# main loop
while True:
    # Read sensors data and also call function to get data from Openweather
    if time.ticks_diff(time.ticks_ms(), last_update) >= UPDATE_TIME_INTERVAL:
        read_bme_dht()
        print('BME Temperature: ', temp)
        print('Pressure: ', pres)
        print('Dht temperature', dht_temp)
        print('Humidity: ', hum)
        # send data to asksensors platform using http
        request = urequests.get(ASK_URL_1+'?'+'module1='+str(temp)+'&module2=' +
                                str(dht_temp)+'&module3='+str(hum)+'&module4='+str(pres))
        request.close()
        temp_open = get_openweather_temp()
        print('Helsinki weather: ', temp_open)
        request = urequests.get(
            ASK_URL_2+'?'+'module1='+str(temp)+'&module4='+str(temp_open))
        request.close()
        last_update = time.ticks_ms()

# if motion is detected by PIR and interrupt is executed send 1 to asksensor
    elif motion:
        print('motion detected')
        motion = False
        motion_start = time.ticks_ms()
        request = urequests.get(ASK_URL_2+'&module2=' +
                                str(1)+'&module3='+str(1))
        request.close()
# motion is reset after some delay(=motion_time defined above) and 0 is send to asksensor module
    elif motion_start and time.ticks_diff(time.ticks_ms(), motion_start) >= motion_time:
        motion_start = None
        request = urequests.get(ASK_URL_2+'&module2=' +
                                str(0)+'&module3='+str(0))
        request.close()
