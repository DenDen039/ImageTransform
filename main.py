import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def CountE(img):
    E = np.array([0,0,0])
    n = img.shape[0]*img.shape[1]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                E[k]+=img[i][j][k]
    for i in range(3):
        E[i] = E[i]/n
    return E
    
def CountD(img,E):
    D = np.array([0,0,0])
    n = img.shape[0]*img.shape[1]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                D[k]+=(img[i][j][k]-E[k])**2
    for i in range(3):
        D[i] = (D[i]/n)**(1/2)
    return D

def TransformImagepalette(img_s,img_t):
    Es = CountE(img_s)
    Ds = CountD(img_s,Es)
    Et = CountE(img_t)
    Dt = CountD(img_t,Et)
    for i in range(img_t.shape[0]):
        for j in range(img_t.shape[1]):
            for k in range(img_t.shape[2]):
                img_t[i][j][k]=(Es[k]+(img_t[i][j][k]-Et[k])*(Ds[k]/Dt[k]))%255
    return img_t


def TransformImages():
    try:
        palette = cv.cvtColor(cv.imread(palette_path), cv.COLOR_BGR2RGB)
        original = cv.cvtColor(cv.imread(original_path), cv.COLOR_BGR2RGB)
    except:
        messagebox.showerror(title="Invalid image", message="Cannot load file as an image")
        return
    fig, ax = plt.subplots(3, 3, figsize=(12, 12))
    fig.tight_layout()
    for j in range(3):
        ax[2][j].axis('off')
        ax[0][j].axis('off')

    ax[0][0].imshow(palette)
    ax[0][0].set_title("Color palettee")

    ax[0][1].imshow(original)
    ax[0][1].set_title("Original")

    result = cv.cvtColor(TransformImagepalette(cv.cvtColor(palette, cv.COLOR_RGB2LAB),cv.cvtColor(original, cv.COLOR_RGB2LAB)), cv.COLOR_LAB2RGB)
    ax[0][2].imshow(result)
    ax[0][2].set_title("Transformed")

    ax[2][0].set_title("Red")
    ax[2][0].imshow(result[:,:,0])

    ax[2][1].set_title("Green")
    ax[2][1].imshow(result[:,:,1])

    ax[2][2].set_title("Blue")
    ax[2][2].imshow(result[:,:,2])


    color = ('r','g','b')
    for i,col in enumerate(color):
        histr = cv.calcHist([palette],[i],None,[256],[0,256])
        ax[1][0].plot(histr,color = col)
    for i,col in enumerate(color):
        histr = cv.calcHist([original],[i],None,[256],[0,256])
        ax[1][1].plot(histr,color = col)
    for i,col in enumerate(color):
        histr = cv.calcHist([result],[i],None,[256],[0,256])
        ax[1][2].plot(histr,color = col)
    plt.show()

def searchForFilePath():
    currdir = os.getcwd()
    file = filedialog.askopenfile(parent=window,mode='r',  initialdir=currdir,title='Please select an image')
    if file:
      filepath = os.path.abspath(file.name)
    return filepath

def importPalette():
    global palette_path
    global targetLabel
    path = searchForFilePath()
    print(path)
    try:
        cv.imread(path)
    except:
        messagebox.showerror(title="Invalid image", message="Cannot load file as an image")
        return
    palette_path = path
    image = Image.open(palette_path)
    image = image.resize((50,50), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    paletteLabel.configure(image=photo)
    paletteLabel.image=photo

def importOriginal():
    global original_path
    global paletteLabel
    path = searchForFilePath()
    try:
        cv.imread(path)
    except:
        messagebox.showerror(title="Invalid image", message="Cannot load file as an image")
        return
    original_path = path
    image = Image.open(original_path)
    image = image.resize((50,50), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    targetLabel.configure(image=photo)
    targetLabel.image=photo

window = Tk()

window.title("Image transformation")
window.geometry('350x200')

targetLabel = Label()
paletteLabel = Label()
paletteLabel.grid(column=1,row=0)
targetLabel.grid(column=1,row=1)

palette_path = ""
original_path = ""

loadPaletteButton = Button(window,text='Load color palette', command=importPalette)
loadPaletteButton.grid(column=0,row=0)
loadTartgetButton = Button(window,text='Load target image', command=importOriginal)
loadTartgetButton.grid(column=0,row=1)
transButton = Button(window,text='Transform images', command=TransformImages)
transButton.grid(column=0,row=2)

window.mainloop()


