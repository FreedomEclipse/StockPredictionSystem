import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H

l = FT232H.enumerate_device_serials(0403, 6015)

print(l)


