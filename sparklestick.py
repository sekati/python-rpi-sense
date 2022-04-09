
#!/usr/bin/python
from sense_hat import SenseHat
from random import randint
from time import sleep
import time
sense = SenseHat()

sense.rotation = 90
sleep_delay = 0.001
message_speed = 0.05
is_paused = False
is_sparkling = True
displayMode = 2
animationMode = 0

# colors
red = (255, 0, 0)        # red
orange = (255, 128, 0)   # orange
yellow = (255, 255, 0)   # yellow
green = (0, 255, 0)      # green
cyan = (0, 255, 255)     # cyan
blue = (0, 0, 255)       # blue
purple = (255, 0, 255)   # purple
pink = (255, 128, 128)   # pink
white = (255, 255, 255)  # white
blank = (0, 0, 0)        # blank

# rainbow array
pixels = [
    [255, 0, 0], [255, 0, 0], [255, 87, 0], [255, 196, 0], [205, 255, 0], [95, 255, 0], [0, 255, 13], [0, 255, 122],
    [255, 0, 0], [255, 96, 0], [255, 205, 0], [196, 255, 0], [87, 255, 0], [0, 255, 22], [0, 255, 131], [0, 255, 240],
    [255, 105, 0], [255, 214, 0], [187, 255, 0], [78, 255, 0], [0, 255, 30], [0, 255, 140], [0, 255, 248], [0, 152, 255],
    [255, 223, 0], [178, 255, 0], [70, 255, 0], [0, 255, 40], [0, 255, 148], [0, 253, 255], [0, 144, 255], [0, 34, 255],
    [170, 255, 0], [61, 255, 0], [0, 255, 48], [0, 255, 157], [0, 243, 255], [0, 134, 255], [0, 26, 255], [83, 0, 255],
    [52, 255, 0], [0, 255, 57], [0, 255, 166], [0, 235, 255], [0, 126, 255], [0, 17, 255], [92, 0, 255], [201, 0, 255],
    [0, 255, 66], [0, 255, 174], [0, 226, 255], [0, 117, 255], [0, 8, 255], [100, 0, 255], [210, 0, 255], [255, 0, 192],
    [0, 255, 183], [0, 217, 255], [0, 109, 255], [0, 0, 255], [110, 0, 255], [218, 0, 255], [255, 0, 183], [255, 0, 74]
]
msleep = lambda x: time.sleep(x / 1000.0)

def next_colour(pix):
    r = pix[0]
    g = pix[1]
    b = pix[2]
    if (r == 255 and g < 255 and b == 0):
        g += 1
    if (g == 255 and r > 0 and b == 0):
        r -= 1
    if (g == 255 and b < 255 and r == 0):
        b += 1
    if (b == 255 and g > 0 and r == 0):
        g -= 1
    if (b == 255 and r < 255 and g == 0):
        r += 1
    if (r == 255 and b > 0 and g == 0):
        b -= 1
    pix[0] = r
    pix[1] = g
    pix[2] = b

def rainbowSparkle():
    global pixels
    for pix in pixels:
        next_colour(pix)
    sense.set_pixels(pixels)

def randomSparkle():
    x = randint(0, 7)
    y = randint(0, 7)
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    #print("x", x, "y", y, ": ",r,",",g,",",b)
    sense.set_pixel(x, y, r, g, b)

def sparkle():
    global is_paused, displayMode, animationMode
    if displayMode == 0:
        return()
    if not is_paused and animationMode == 0:
        randomSparkle()
    elif not is_paused and animationMode == 1:
        rainbowSparkle()

def showMessage(str):
    is_paused = True
    sense.show_message(str, text_colour=purple, back_colour=cyan, scroll_speed=message_speed)
    sleep(1)
    is_paused = False

def toggleDisplayBrightness():
    global displayMode
    displayMode += 1
    if displayMode > 2:
        displayMode = 0
        sense.clear()
    elif displayMode == 1:
        sense.low_light = False
    else:
        sense.low_light = True
    print("displayMode = ",displayMode)

def showTemp():
    celsius = sense.get_temperature()
    fahrenheit = round((celsius * 1.8) + 32, 2)
    showMessage("Temp %s F" % fahrenheit)

def showPressure():
    pressure = round(sense.get_pressure(), 2)
    showMessage("Pressure %s" % pressure)

def showHumidity():
    humidity = round(sense.get_humidity(), 2)
    showMessage("Humidity %s" % humidity)

def showCompass():
    north = round(sense.get_compass(), 2)
    showMessage("Compass %s" % north)

try:
    while True:
        sparkle()
        msleep(sleep_delay)
        for event in sense.stick.get_events():
            if event.action == "pressed":
                #print(event.direction)
                if event.direction == 'up':
                    #showMessage("Up")
                    #showMessage("<- Left")
                    showHumidity()
                elif event.direction == 'down':
                    #showMessage("Down")
                    #showMessage("Right ->")
                    showTemp()
                elif event.direction == 'left':
                    #showMessage("Left")
                    #showMessage("Down \/")
                    animationMode = 1
                    #showTemp()
                elif event.direction == 'right':
                    #showMessage("Right")
                    #showMessage("/\\ Up")
                    animationMode = 0
                    #showCompass()
                elif event.direction == 'middle':
                    #showMessage("Click")
                    toggleDisplayBrightness()
except KeyboardInterrupt:
    print('Goodbye World!')