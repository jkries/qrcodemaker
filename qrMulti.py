#! /usr/bin/python3

import qrcode # Import QR Code library with pip install qrcode[pil]
import sys #To exit the program if QR data is not given
import os #To create the save folder if not already there
import csv #CSV file support
from PIL import Image, ImageDraw, ImageFont #Display the image
import time #For the waiting

qrName = 'qr'

# Prompt user for the data that you want to store, the filename, desired size, and format of the QR code image:
print('===============================================')
csvFile = input('What is your data file named (leave blank for default: demo.csv)? ')
print('===============================================')
qrLabel = input('Do you want captions from column #2 in your file? Y/N ')
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

#Are we doing captions?
doCaption = 0
if qrLabel == 'Y' or qrLabel == "y" or qrLabel == "yes" or qrLabel == "YES":
    doCaption = 1
else:
    if not os.path.exists('fonts/FreeMono.ttf'):
        doCaption = 0
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('I could not find a font file to make your caption!\nPlease download FreeMono.ttf and put it in the fonts folder.')
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    if len(str(qrLabel)) > 24:
        #Removed for now
        print('We are doing a caption.')
        #qrLabel = qrLabel[0:24]
        #print('Truncating your caption to make it fit.')

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

        #Are we adding a caption?
        if doCaption:
            draw = ImageDraw.Draw(img)
            QRwidth, QRheight = img.size
            fontSize = 1 #starting font size
            qrLabel = line[1] #Get the caption from the 2nd column of the CSV file
            img_fraction = 0.90 # portion of image width you want text width to be
            fontHeightMax = qr.border * qr.box_size - 10
            captionX = 0
            captionY = 0
            print('Font height max is set to: ' + str(fontHeightMax))
            font = ImageFont.truetype("fonts/FreeMono.ttf", fontSize)
            while font.getsize(qrLabel)[0] < img_fraction*img.size[0] and font.getsize(qrLabel)[1] < fontHeightMax:
                fontSize += 1
                font = ImageFont.truetype("fonts/FreeMono.ttf", fontSize)
            captionX = int(img.size[0] - font.getsize(qrLabel)[0]) / 2 #Center the label
            print('Offset: ' + str(captionX))
            draw.text((captionX, captionY), qrLabel, font=font)

        # Save it somewhere, change the extension as needed:
        img.save(qrFolder + qrFilename + imageExt)
        print('QR Code successfully save as ' + qrFolder + qrFilename + imageExt)

print('===============================================')
print('Done!')
print('You successfully created ' + str(lineCount) + ' QR codes!')
print('===============================================')
