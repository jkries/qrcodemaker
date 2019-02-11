#! /usr/bin/python3

import qrcode # Import QR Code library with pip install qrcode[pil]
import sys #To exit the program if QR data is not given
import os #To create the save folder if not already there
from PIL import Image, ImageDraw, ImageFont #Save and display the image
import time #For the waiting

# Prompt user for the data that you want to store, the filename, desired size, and format of the QR code image:
print('===============================================')
data = input('What do you want in your QR code: ')
print('===============================================')
qrLabel = input('Do you want a caption? (Leave blank for no caption) ')
print('===============================================')
qrName = input('What do you want to name the QR code file? ')
print('===============================================')
boxPixels = input('If you want to make the boxes bigger than 10 pixels wide, enter a number here: ')
print('===============================================')
imageType = input('Press enter to save as PNG (default), 1 for JPG, 2 for JPEG, 3 for BMP: ')
print('===============================================')

if len(str(data)) == 0:
    print('You did not enter anything.  Exiting Program...')
    sys.exit()

doCaption = 1
if len(str(qrLabel)) == 0:
    doCaption = 0
else:
    if len(str(qrLabel)) > 24:
        qrLabel = qrLabel[0:24]
        print('Truncating your caption to make it fit.')

if len(str(qrName)) == 0:
    print('You did not pick a filename.  Using "myQr" as the filename.')
    print('===============================================')
    qrName = 'myQR'

if len(str(boxPixels)) == 0:
    print('You did not set a pixel size for boxes. I will use 10')
    print('===============================================')
    boxPixels = 10

#Set the image type:
if imageType == "1":
    imageExt = '.jpg'
elif imageType == "2":
    imageExt = '.jpeg'
elif imageType == "3":
    imageExt = '.bmp'
else:
    imageExt = '.png'

#Make a folder for saved QRcodes
if not os.path.exists('savefolder'):
    os.makedirs('savefolder')
    print('Creating subfolder: "savefolder"')
    print('===============================================')

#Check to see if we already have a previously created file with the same name:
if os.path.exists('savefolder/' + str(qrName) + imageExt):
    print('You already have a code named ' + qrName + '. I am renaming it ' + qrName + '-COPY')
    print('===============================================')
    qrName = qrName + '-COPY'

# Create qr code instance
qr = qrcode.QRCode()

# Add data
qr.box_size = int(boxPixels)
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image()

#Are we adding a caption?
if doCaption:
    draw = ImageDraw.Draw(img)
    # use a truetype font
    font = ImageFont.truetype("fonts/FreeMono.ttf", 20)
    draw.text((0, 0), qrLabel, font=font)

# Save it somewhere, change the extension as needed:
img.save("savefolder/" + str(qrName) + imageExt)
print('QR Code successfully save as ' + str(qrName) + imageExt)

#Display the image:
time.sleep(2)
showImage = Image.open("savefolder/" + str(qrName) + imageExt)
showImage.show()
