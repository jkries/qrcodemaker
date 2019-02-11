#! /usr/bin/python3

import qrcode # Import QR Code library with pip install qrcode[pil]
import sys #To exit the program if QR data is not given
import os #To create the save folder if not already there
import csv #CSV file support
from PIL import Image #Display the image
import time #For the waiting

qrName = 'qr'

# Prompt user for the data that you want to store, the filename, desired size, and format of the QR code image:
print('===============================================')
csvFile = input('What is your data file named (leave blank for default: demo.csv)? ')
print('===============================================')
qrFolder = input('What do you want to name the QR code folder? ')
print('===============================================')
boxPixels = input('If you want to make the boxes bigger than 10 pixels wide, enter a number here: ')
print('===============================================')
imageType = input('Press enter to save as PNG (default), 1 for JPG, 2 for JPEG, 3 for BMP: ')
print('===============================================')

if len(str(csvFile)) == 0:
    print('You did not pick a data file.  Using the demo.csv file as a data source.')
    print('===============================================')
    csvFile = 'demo.csv'
#Make a sub folder for saved QRcodes from this run:
if not os.path.exists(csvFile):
    print('Could not locate any data file named ' + str(csvFile) + '.  Exiting Program...')
    sys.exit()

if len(str(qrFolder)) == 0:
    print('You did not pick a folder name.  Using "myQr" as the folder name.')
    print('===============================================')
    qrFolder = 'savefolder/myQR/'
else:
    qrFolder = 'savefolder/' + qrFolder + '/'

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
    print('Creating folder: "savefolder"')
    print('===============================================')

#Make a sub folder for saved QRcodes from this run:
if not os.path.exists(qrFolder):
    os.makedirs(qrFolder)
    print('Creating folder: ' + qrFolder)
    print('===============================================')

#Open the CSV file, loop through each line and create a QR code:
lineCount = 0
with open(csvFile) as f:
    lines = csv.reader(f)
    for line in lines:
        lineCount += 1
        qrFilename = qrName + str(lineCount)

        #Check to see if we already have a previously created file with the same name:
        if os.path.exists(qrFolder + str(qrFilename) + imageExt):
            print('You already have a code named ' + qrFilename + '. I am renaming it ' + qrFilename + '-COPY')
            print('===============================================')
            qrFilename = qrFilename + '-COPY'

        # Create qr code instance
        qr = qrcode.QRCode()

        # Add data
        qr.box_size = int(boxPixels)
        qr.add_data(line[0]) #Add the data from column 1 of the CSV
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image()

        # Save it somewhere, change the extension as needed:
        img.save(qrFolder + qrFilename + imageExt)
        print('QR Code successfully save as ' + qrFolder + qrFilename + imageExt)

print('===============================================')
print('Done!')
print('You successfully created ' + str(lineCount) + ' QR codes!')
print('===============================================')
