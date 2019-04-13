# Import standard Python time library.
import time
import subprocess

# Import GPIO and FT232H modules.
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H

# Temporarily disable the built-in FTDI serial driver on Mac & Linux platforms.
FT232H.use_FT232H()
#subprocess.call('sudo kextunload -b com.apple.driver.AppleUSBFTDI', shell=True)
#subprocess.call('sudo kextunload /System/Library/Extensions/FTDIUSBSerialDriver.kext', shell=True)
#subprocess.call('kextunload -bundle-id com.FTDI.driver.FTDIUSBSerialDriver', shell=True)
#subprocess.call('kextunload /System/Library/Extensions/FTDIUSBSerialDriver.kext', shell=True)

# Create an FT232H object that grabs the first available FT232H device found.
ft232h = FT232H.FT232H()

# Configure digital inputs and outputs using the setup function.
# Note that pin numbers 0 to 15 map to pins D0 to D7 then C0 to C7 on the board.
ft232h.setup(7, GPIO.IN)   # Make pin D7 a digital input.
ft232h.setup(8, GPIO.OUT)  # Make pin C0 a digital output.
ft232h.setup(9, GPIO.OUT)  # Make pin C1 a digital output.
ft232h.setup(10, GPIO.OUT)  # Make pin C2 a digital output.
ft232h.setup(11, GPIO.OUT)  # Make pin C3 a digital output.
ft232h.setup(12, GPIO.OUT)  # Make pin C4 a digital output.
ft232h.setup(13, GPIO.OUT)  # Make pin C5 a digital output.
ft232h.setup(14, GPIO.OUT)  # Make pin C6 a digital output.
ft232h.setup(15, GPIO.OUT)  # Make pin C7 a digital output.

# Loop turning the LED on and off and reading the input state.
print 'Press Ctrl-C to quit.'
count = 0
markers = [0x100, 0x200, 0x300, 0x400, 0x500, 0x600, 0x700, 0x800, 0x900, 0xA17, 0xB17, 0xC17, 0xD17, 0xE17, 0xF17, 0x1000]
while count < 16:
	# Set pin C0 to a high level so the LED turns on.
	#ft232h.output(11, GPIO.LOW)
	#ft232h.output(8, GPIO.HIGH)
	i = count

	#ft232h.output(8, GPIO.HIGH)
	#ft232h.output_all(0x100)
	print(i)
	# Sleep for 1 second.
	#ft232h.output_all(0x100)

	#time.sleep(3)

	ft232h.output_all(markers[i])
	#ft232h.output(8, GPIO.LOW)
	time.sleep(3)


	#ft232h.output_all(0x0000)
	#ft232h.output(8, GPIO.HIGH)


	count += 1

ft232h.close()