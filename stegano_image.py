from PIL import Image
import tkinter as tk
from tkinter import filedialog

    
def binaire(n):
    b = bin(n)
    a = b[2:]
    while len(a) < 8:
        a = "0" + a
    return a


def dissimulation (imageforte, imagefaible, canaux_, canal_, bits_):
    if imageforte.size < imagefaible.size:
        (xmax, ymax) = imageforte.size
    else:
        (xmax, ymax) = imagefaible.size
        
    if imageforte.mode == "RGB" or imagefaible.mode == "RGB":
            image = Image.new("RGB", (xmax,ymax))

    else:
        image = Image.new("RGBA", (xmax,ymax))

            

    for x in range(xmax):
        for y in range(ymax):
            pxF = imageforte.getpixel((x,y))
            pxf = imagefaible.getpixel((x,y))
            if image.mode == "RGB":
                (rF, gF, bF) = pxF
                (rf, gf, bf) = pxf
            else:
                (rF, gF, bF, aF) = pxF
                (rf, gf, bf, af) = pxf

            a = []

            bits_fort = 8 - bits_
            compteur = canaux_
            
            for k in range(3):
                if canaux_ == 1 and k == canal_ :
                    F = binaire(pxF[canal_])
                    f = binaire(pxf[canal_])
                    newb = F[:bits_fort] + f[:bits_]
                    new = int(newb, 2) 
                    a.append(new)
                    continue

                if compteur > 0 and canaux_ != 1:
                    F = binaire(pxF[k]) 
                    f = binaire(pxf[k])
                    newb = F[:bits_fort] + f[:bits_]
                    new = int(newb, 2)
                    a.append(new)
                    compteur -= 1
                    continue

                if canaux_ != 3:
                    a.append(int(binaire(pxF[k]), 2))

            image.putpixel((x,y), tuple(a))

    return image



def recuperation(imageforte, canaux_, canal_, bits_):
    (xmax, ymax) = imageforte.size
    if imageforte.mode == "RGB":
        imageR = Image.new("RGB", (xmax,ymax))
    else:
        imageR = Image.new("RGBA", (xmax,ymax))
    
    for x in range(xmax):
        for y in range(ymax):
            pxF = imageforte.getpixel((x,y))
            if imageR.mode == "RGB":
                (rF, gF, bF) = pxF
            else:  
                (rF, gF, bF, aF) = pxF

            b = []

            bits_fort = 8 - bits_
            compteur = canaux_

            for k in range(3):
                if canaux_ == 1 and k == canal_:
                    F = binaire(pxF[canal_])
                    newb = F[bits_fort:] + "1" + "0"*(bits_fort-1)
                    new = int(newb, 2)
                    b.append(new)
                    continue

                if compteur > 0 and canaux_ != 1:
                    F = binaire(pxF[k])
                    newb = F[bits_fort:] + "1" + "0"*(bits_fort-1)
                    new = int(newb, 2)
                    b.append(new)
                    compteur -= 1
                    continue

                if canaux_ != 3:
                    b.append(00000000)
            imageR.putpixel((x,y), tuple(b))
    return imageR


def select_image_forte():
    filename = filedialog.askopenfilename(title="Sélectionner l'image de dissimulation")
    image_forte_entry.delete(0, tk.END)
    image_forte_entry.insert(0, filename)

def select_image_faible():
    filename = filedialog.askopenfilename(title="Sélectionner l'image à dissimuler")
    image_faible_entry.delete(0, tk.END)
    image_faible_entry.insert(0, filename)

def dissimuler():
    bits_ = int(bits_entry.get())
    canaux_ = int(canaux_entry.get())
    canal_ = canal_entry.get()
    if canal_ != "":
        canal_ = int(canal_)


    image_forte_path = image_forte_entry.get()
    image_faible_path = image_faible_entry.get()
    extension = extension_entry.get()
    

    imagefaible = Image.open(image_faible_path)
    imageforte = Image.open(image_forte_path)

    if imagefaible.mode == "RGB":
        imagefaible = Image.open(image_faible_path).convert("RGB")
        imageforte = Image.open(image_forte_path).convert("RGB")
    else:
        imagefaible = Image.open(image_faible_path).convert("RGBA")
        imageforte = Image.open(image_forte_path).convert("RGBA")

    
    imageD = dissimulation(imageforte, imagefaible, canaux_, canal_, bits_)
    imageD.save("imageSteganographiee" + extension)
    imageRecup = recuperation(imageD, canaux_, canal_, bits_)
    imageRecup.save("imageRecuperee" + extension)

    imageD.show()
    imageRecup.show()

    result_label.config(text="Dissimulation terminée")

window = tk.Tk()
window.title("Stéganographie - Dissimulation d'image")

bits_label = tk.Label(window, text="Nombre de bits à utiliser pour la méthode LSB :")
bits_label.pack()
bits_entry = tk.Entry(window)
bits_entry.pack()

canaux_label = tk.Label(window, text="Nombre de canaux (RGB) à utiliser :")
canaux_label.pack()
canaux_entry = tk.Entry(window)
canaux_entry.pack()

canal_label = tk.Label(window, text="Si vous avez choisi un seul canal, lequel voulez-vous utiliser ? (R = 0, G = 1, B = 2)")
canal_label.pack()
canal_entry = tk.Entry(window)
canal_entry.pack()

extension_label = tk.Label(window, text="Entrer le format souhaité (.png, .jpg, .bmp, ...)")
extension_label.pack()
extension_entry = tk.Entry(window)
extension_entry.pack()

image_forte_button = tk.Button(window, text="Sélectionner l'image de dissimulation", command=select_image_forte)
image_forte_button.pack()
image_forte_entry = tk.Entry(window)
image_forte_entry.pack()

image_faible_button = tk.Button(window, text="Sélectionner l'image à dissimuler", command=select_image_faible)
image_faible_button.pack()
image_faible_entry = tk.Entry(window)
image_faible_entry.pack()

dissimuler_button = tk.Button(window, text="Dissimuler", command=dissimuler)
dissimuler_button.pack()


result_label = tk.Label(window, text="")
result_label.pack()

window.mainloop()
