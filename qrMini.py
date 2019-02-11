#! /usr/bin/python3
import qrcode
img = qrcode.make(input('What should the QR code say? '))
qrLabel = "My QR Code"
img.save('saved.png')

img.show('saved.png') #You can remove this line if you do not need to see a preview after QR generation
