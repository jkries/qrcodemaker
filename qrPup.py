#! /usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import filedialog
from tkinter import *
import tkinter.messagebox as box
import qrcode # Import QR Code library with pip install qrcode[pil]
import sys #To exit the program if QR data is not given
import csv #CSV file support
import os #To create the save folder if not already there
import codecs
from PIL import Image, ImageDraw, ImageFont #Save and display the image
import time #For the waiting

root = Tk()
label1 = Label(root)

#Are you making 1 or loading many QR codes from a csv file?
#Captions? (You need a field for a single QR caption)
#QR Code file name (for single)
#Preview checkbox for single?
#Box box
#Image format
#Save folder name for CSV

root.title('QR Pup QR Code Creation Wizard')
root.call('wm', 'iconphoto', root._w, PhotoImage(file='images/favicon.png'))

csvFile = 'N/A'
multiStatus = 'Save'

def getFile():
    global csvFile
    print(csvFile)
    root.filename =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("CSV files","*.csv"),("all files","*.*")))
    print (root.filename)
    csvFile = root.filename
    #Confirm successful
    box.showinfo('Success!', str(csvFile) + ' CSV File Loaded!')

def makeSingle():
    print('You clicked Make 1 QR Code')
    data = e1.get()
    qrLabel = e2.get()
    qrName = e3.get()
    imageExt = saveType.get()
    boxPixels = qrSize.get()
    doCaption = 1
    fontFile = 'fonts/FreeMono.ttf'
    fontName = 'FreeMono.ttf'
    if len(str(qrLabel)) == 0:
        doCaption = 0
    else:
        if not os.path.exists(fontFile):
            doCaption = 0
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('I could not find a font file to make your caption!\nPlease download ' + fontName + ' and put it in the fonts folder.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    if len(str(data)) == 0:
        print('You did not enter anything.  Exiting Program...')
        sys.exit()

    if len(str(qrName)) == 0:
        print('You did not pick a filename.  Using "myQr" as the filename.')
        print('===============================================')
        qrName = 'myQR'

    if len(str(boxPixels)) == 0:
        print('You did not set a pixel size for boxes. Using 10 pixels per box.')
        print('===============================================')
        boxPixels = 10

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
        QRwidth, QRheight = img.size
        fontSize = 1 #starting font size
        img_fraction = 0.90 # portion of image width you want text width to be, I've had good luck with .90
        fontHeightMax = qr.border * qr.box_size - 10
        captionX = 0
        captionY = 0
        print('Font height max is set to: ' + str(fontHeightMax))
        font = ImageFont.truetype(fontFile, fontSize)
        while font.getsize(qrLabel)[0] < img_fraction*QRwidth and font.getsize(qrLabel)[1] < fontHeightMax:
            fontSize += 1
            font = ImageFont.truetype(fontFile, fontSize)
        captionX = int(QRwidth - font.getsize(qrLabel)[0]) / 2 #Center the label
        print('Offset: ' + str(captionX))
        draw.text((captionX, captionY), qrLabel, font=font)

    # Save it somewhere, change the extension as needed:
    img.save("savefolder/" + str(qrName) + imageExt)
    print('QR Code successfully save as ' + str(qrName) + imageExt)

    #Confirm successful
    box.showinfo('Success!', 'QR Code Successfully Created!')

    #Display the image:
    time.sleep(2)
    showImage = Image.open("savefolder/" + str(qrName) + imageExt)
    showImage.show()

def makeMulti():
    print('You clicked Make Multi QR Code')
    qrName = 'qr'
    qrLabel = qrCaptions.get()
    qrFolder = e4.get()
    imageExt = saveType.get()
    boxPixels = qrSize.get()
    global multiStatus
    global csvFile
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
    if qrLabel:
        doCaption = 1
        fontFile = 'fonts/FreeMono.ttf'
        fontName = 'FreeMono.ttf'
    if doCaption:
        if not os.path.exists(fontFile):
            doCaption = 0
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print('I could not find a font file to make your caption!\nPlease download ' + fontName + ' and put it in the fonts folder.')
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

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

    #Confirm start
    box.showinfo('Warm it up!', 'Creating codes from your CSV file.  I will pop up again when I am done!')

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
                fontHeightMax = qr.border * qr.box_size - 10 #Maximum height for captions
                captionX = 0 #Where to start the caption X coordinate
                captionY = 0 #Where to start the caption y coordinate
                print('Font height max is set to: ' + str(fontHeightMax))
                font = ImageFont.truetype(fontFile, fontSize)
                while font.getsize(qrLabel)[0] < img_fraction*QRwidth and font.getsize(qrLabel)[1] < fontHeightMax:
                    fontSize += 1
                    font = ImageFont.truetype(fontFile, fontSize)
                captionX = int(QRwidth - font.getsize(qrLabel)[0]) / 2 #Center the label
                print('Offset: ' + str(captionX))
                draw.text((captionX, captionY), qrLabel, font=font)

            # Save it somewhere, change the extension as needed:
            img.save(qrFolder + qrFilename + imageExt)
            print('QR Code successfully save as ' + qrFolder + qrFilename + imageExt)

    #Confirm successful
    box.showinfo('Success!', str(lineCount) + ' QR Codes Successfully Created!')

                                                                                                                                                                                                                                                                                          
#Load top logo:
img = PhotoImage(file="images/toplogo.png")
panel = Label(root, image = img)
panel.grid(row=0, column=0, columnspan=3, rowspan=1, padx=100, pady=5)

#Experimental
Label(root, text="Create 1 QR Code:", font=("Helvetica", 20)).grid(row=1, column=0, sticky=W, pady=5)
Label(root, text="Create a batch from CSV:", font=("Helvetica", 20)).grid(row=1, column=2, sticky=W, pady=5)

Label(root, text="OR", font=("Helvetica", 32)).grid(row=1, column=1, sticky=N, pady=0, padx=10)

Label(root, text="Enter QR Code Data:", font=(12)).grid(row=2, column=0, sticky=W)
Label(root, text="Enter QR Caption (optional):", font=(12)).grid(row=4, column=0, sticky=W)
Label(root, text="Save File Name (optional):", font=(12)).grid(row=6, column=0, sticky=W)
Label(root, text="QR Code Image Size:", font=(12)).grid(row=8, column=0, sticky=W)
Label(root, text="Image Type:", font=(12)).grid(row=12, column=0, sticky=W)

e1 = Entry(root, width=40, font=(12))
e2 = Entry(root, width=35, font=(12))
e3 = Entry(root, width=25, font=(12))

e1.grid(row=3, column=0, sticky=W)
e2.grid(row=5, column=0, sticky=W)
e3.grid(row=7, column=0, sticky=W)

qrSize = IntVar()
Radiobutton(root, text="Small", variable=qrSize, value=10).grid(row=9, column=0, sticky=W)
Radiobutton(root, text="Medium", variable=qrSize, value=25).grid(row=10, column=0, sticky=W)
Radiobutton(root, text="Large", variable=qrSize, value=50).grid(row=11, column=0, sticky=W)
qrSize.set(10)

saveType = StringVar()
Radiobutton(root, text="PNG (default)", variable=saveType, value=".png").grid(row=13, column=0, sticky=W)
Radiobutton(root, text="JPG", variable=saveType, value=".jpg").grid(row=14, column=0, sticky=W)
Radiobutton(root, text="BMP", variable=saveType, value=".bmp").grid(row=15, column=0, sticky=W)
saveType.set(".png")

singleButton = Button(text='Create My QR Code', font=(14), command=makeSingle)
singleButton.grid(row=16, column=0, pady=5, padx=15, sticky=W)
#End of the first column grid

csvButton = Button(text='Choose CSV File', font=(14), command=getFile)
csvButton.grid(row=2, column=2, pady=5)

Label(root, text="Do you have captions in your CSV:", font=(12)).grid(row=3, column=2, sticky=W)

qrCaptions = IntVar()
Radiobutton(root, text="Yes", variable=qrCaptions, value=1).grid(row=4, column=2, sticky=W)
Radiobutton(root, text="No", variable=qrCaptions, value=0).grid(row=5, column=2, sticky=W)
qrCaptions.set(0)

Label(root, text="Save Folder Name:", font=(12)).grid(row=6, column=2, sticky=W)
e4 = Entry(root, width=20, font=(12))
e4.grid(row=7, column=2, sticky=W)

Label(root, text="QR Code Image Size:", font=(12)).grid(row=8, column=2, sticky=W)
Radiobutton(root, text="Small", variable=qrSize, value=10).grid(row=9, column=2, sticky=W)
Radiobutton(root, text="Medium", variable=qrSize, value=25).grid(row=10, column=2, sticky=W)
Radiobutton(root, text="Large", variable=qrSize, value=50).grid(row=11, column=2, sticky=W)

Label(root, text="Image Type:", font=(12)).grid(row=12, column=2, sticky=W)
Radiobutton(root, text="PNG (default)", variable=saveType, value=".png").grid(row=13, column=2, sticky=W)
Radiobutton(root, text="JPG", variable=saveType, value=".jpg").grid(row=14, column=2, sticky=W)
Radiobutton(root, text="BMP", variable=saveType, value=".bmp").grid(row=15, column=2, sticky=W)

multiButton = Button(text='Create All The QR Codes!', font=(14), command=makeMulti)
multiButton.grid(row=16, column=2, pady=5, padx=15, sticky=W)

root.mainloop()
