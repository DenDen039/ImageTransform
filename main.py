import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os


def TransformImagepalette(imgS, imgT):
    Et = np.mean(imgT, axis=(0, 1))
    Dt = np.std(imgT, axis=(0, 1))
    Es = np.mean(imgS, axis=(0, 1))
    Ds = np.std(imgS, axis=(0, 1))
    result = (Es + (imgT - Et) * (Ds / Dt)).astype("uint8")
    result[result>255] = 255
    result[result<0] = 0
    return result

def PlotColorChannels(image):
    #Check if not empty
    try:
        image[0][0][0]
    except:
        return

    fig, ax = plt.subplots(1, 3, figsize=(12, 6))

    for j in range(3):
        ax[j].axis('off')

    fig.canvas.set_window_title('3 channels')
    fig.tight_layout()

    #Draw image in three channels
    ax[0].set_title("Red")
    ax[0].imshow(image[:,:,0])

    ax[1].set_title("Green")
    ax[1].imshow(image[:,:,1])

    ax[2].set_title("Blue")
    ax[2].imshow(image[:,:,2])
    plt.show()

def TransformImages():
    global resultImage
    transfomationType = {
        "LAB": (cv.COLOR_RGB2LAB, cv.COLOR_LAB2RGB),
        "HSV": (cv.COLOR_RGB2HSV_FULL, cv.COLOR_HSV2RGB_FULL),
        "HLS": (cv.COLOR_RGB2HLS_FULL, cv.COLOR_HLS2RGB_FULL),
    }

    #Read Images and convert them to RGB
    try:
        palette = cv.cvtColor(cv.imread(palettePath), cv.COLOR_BGR2RGB)
        original = cv.cvtColor(cv.imread(originalPath), cv.COLOR_BGR2RGB)
    except:
        messagebox.showerror(title="Invalid image",
                             message="Cannot load file as an image")
        return
    #Create figure
    fig, ax = plt.subplots(2, 3, figsize=(12, 8))
    fig.tight_layout()
    fig.canvas.set_window_title('Transformation')
    for j in range(3):
        ax[0][j].axis('off')

    #Display palettte Image
    ax[0][0].imshow(palette)
    ax[0][0].set_title("Color palettee")

    #Display orginal
    ax[0][1].imshow(original)
    ax[0][1].set_title("Original")

    #Apply transformation
    result = cv.cvtColor(TransformImagepalette(cv.cvtColor(
        palette, transfomationType[colorSpace.get()][0]), cv.cvtColor(original, transfomationType[colorSpace.get()][0])), transfomationType[colorSpace.get()][1])

    #Disable not checked channels
    for k in range(len(channels)):
        if channels[k].get() != 1:
            for i in range(result.shape[0]):
                for j in range(result.shape[1]):
                    result[i][j][k] = original[i][j][k]

    ax[0][2].imshow(result)
    ax[0][2].set_title("Transformed")

    #Plot RGB historgams for images
    color = ('r', 'g', 'b')
    for i, col in enumerate(color):
        histr = cv.calcHist([palette], [i], None, [256], [0, 256])
        ax[1][0].plot(histr, color=col)
    for i, col in enumerate(color):
        histr = cv.calcHist([original], [i], None, [256], [0, 256])
        ax[1][1].plot(histr, color=col)
    for i, col in enumerate(color):
        histr = cv.calcHist([result], [i], None, [256], [0, 256])
        ax[1][2].plot(histr, color=col)

    #Add result to interface
    image = Image.fromarray(result)
    image = image.resize((50, 50), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    resultLabel.configure(image=photo)
    resultLabel.image = photo

    resultImage = result
    #Show figure
    plt.show()


def searchForFilePath():
    currdir = os.getcwd()
    file = filedialog.askopenfile(
        parent=window, mode='r',  initialdir=currdir, title='Please select an image')
    if file:
      filepath = os.path.abspath(file.name)
    return filepath


def importPalette():
    global palettePath,paletteLabel,paletteImage
 
    path = searchForFilePath()
    print(path)
    try:
        cv.imread(path)
    except:
        messagebox.showerror(title="Invalid image",
                             message="Cannot load file as an image")
        return
    palettePath = path
    image = Image.open(palettePath)
    paletteImage = np.array(image)
    image = image.resize((50, 50), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    paletteLabel.configure(image=photo)
    paletteLabel.image = photo


def importOriginal():
    global originalPath,targetLabel,originalImage
    path = searchForFilePath()
    try:
        cv.imread(path)
    except:
        messagebox.showerror(title="Invalid image",
                             message="Cannot load file as an image")
        return
    originalPath = path
    image = Image.open(originalPath)
    originalImage = np.array(image)
    image = image.resize((50, 50), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    targetLabel.configure(image=photo)
    targetLabel.image = photo


window = Tk()

window.title("Image transformation")
window.geometry('350x200')
for i in range(3):
    window.columnconfigure(i, weight=1)


#Global vars
palettePath = ""
originalPath = ""
paletteImage,originalImage,resultImage = "","",""

#Text for result
textLabel = Label(text="Result:")
textLabel.grid(column=0, row=3)

#Images
targetLabel = Label(cursor= "hand2")
paletteLabel = Label(cursor= "hand2")
resultLabel = Label(cursor= "hand2")

paletteLabel.grid(column=1, row=0)
targetLabel.grid(column=1, row=1)
resultLabel.grid(column=1, row=3)

paletteLabel.bind("<Button-1>",lambda tmp: PlotColorChannels(paletteImage))
targetLabel.bind("<Button-1>",lambda  tmp: PlotColorChannels(originalImage))
resultLabel.bind("<Button-1>",lambda  tmp: PlotColorChannels(resultImage))

#Buttons
loadPaletteButton = Button(
    window, text='Load color palette', command=importPalette, width=15)
loadPaletteButton.grid(column=0, row=0)

loadTargetButton = Button(
    window, text='Load target image', command=importOriginal, width=15)
loadTargetButton.grid(column=0, row=1)

transButton = Button(window, text='Transform image',
                     command=TransformImages, width=15)
transButton.grid(column=0, row=2)

# Create Dropdown menu
options = ["LAB", "HLS", "HSV"]
colorSpace = StringVar()
colorSpace.set("LAB")
drop = OptionMenu(window, colorSpace, *options)
drop.grid(column=1, row=2)

#Checkboxes
channels = [IntVar(), IntVar(), IntVar()]
Checkbutton(window, text="R", variable=channels[0]).grid(column=3, row=2)
Checkbutton(window, text="G", variable=channels[1]).grid(column=4, row=2)
Checkbutton(window, text="B", variable=channels[2]).grid(column=5, row=2)

window.mainloop()
