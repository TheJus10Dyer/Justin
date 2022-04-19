
#Justin Dyer

import time
import board
import microcontroller
import analogio
import adafruit_thermistor
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService


ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

thermistor = adafruit_thermistor.Thermistor(board.TEMPERATURE, 10000, 10000, 25, 3950)
light = analogio.AnalogIn(board.LIGHT)
boardtemp = microcontroller.cpu.temperature * 9/5 +32


def scale(value):
    return value / 65535 * 50


from rainbowio import colorwheel
import neopixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)


color_chase_demo = 1
def color_chase(color, wait):
    for i in range(10):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)



while True:
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        color_chase(BLUE, 0.1)
        color_chase(OFF, 0.1)
        time.sleep(.1)
    ble.stop_advertising()



    while ble.connected:
        temp = thermistor.temperature*9/5 + 32


        if 60 <= temp <= 80 :
            pixels.fill((0, 150, 0))
            pixels.show()
        if temp < 60:
            pixels.fill((0, 0, 150))
            pixels.show()
        if temp > 80:
            pixels.fill((150, 0, 0))
            pixels.show()

        print((scale(light.value), temp, boardtemp))
        uart_server.write("{},{},{}\n".format(scale(light.value), temp, boardtemp))
        time.sleep(0.5)
