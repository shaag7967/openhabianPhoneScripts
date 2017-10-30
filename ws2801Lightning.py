import sys
import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
 
 
# Configure the count of pixels:
PIXEL_COUNT = 3
 
GPIO.setmode(GPIO.BCM)


SPICLK = 23 # The SPI clock pin on the raspberry pi, pin 23
SPIDO = 19 # The SPI data line (MOSI) on the raspberry pi, pin 19

SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)


if len(sys.argv) != 4:
   pixels.clear()
else:
   pixels.set_pixels_rgb(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

pixels.show()
