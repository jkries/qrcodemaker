#! /usr/bin/python3
import qrcode
import time
from PIL import Image, ImageDraw, ImageFont

img = qrcode.make(input('What should the QR code say? '))
qrLabel = input('What should the label be on your QR code? ')

if len(str(qrLabel)) == 0:
    qrLabel = "1234567890123456789012345"

draw = ImageDraw.Draw(img)
# use a truetype font
font = ImageFont.truetype("fonts/FreeMono.ttf", 20)
draw.text((0, 0), qrLabel, font=font)

img.save('saved.png')

time.sleep(1)

img.show('saved.png') #You can remove this line if you do not need to see a preview after QR generation
