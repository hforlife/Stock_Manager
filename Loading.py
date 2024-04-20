import os
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk

root = Tk()

# Taille de la fenêtre principale
width = 770
height = 430

# Récupérer les dimensions de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculer les coordonnées x et y pour placer la fenêtre au centre de l'écran
x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.config(background='#F66B0E')

welcome_label = Label(root, text="BIENVENUE", bg="#F66B0E", font=("Poppins", 20, "italic bold"), fg="#FFF")
welcome_label.place(x=280, y=25)


progress_label = Label(root, text="Patienter...", bg="#343A40", font=("Poppins", 15, "italic"), fg="#FFF")
progress_label.place(x=300, y=330)

progress = ttk.Style()
progress.theme_use('clam')
progress.configure('red.Horizontal', background='#108CFF')

progress_bar = Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate', style='red.Horizontal.TProgressbar')
progress_bar.place(x=180, y=370)

def top():
    root.withdraw()
    os.system('python login.py')
    root.destroy()

i = 0

def load():
    global i
    if i <= 10:
        txt = "Patienter... " + str(10 * i) + '%'
        progress_label.config(text=txt, font=("Poppins", 15, "italic"), bg='#F66B0E')
        progress_bar['value'] = 10 * i
        i += 1
        progress_label.after(600, load)
    else:
        top()

load()
root.resizable(False, False)
root.mainloop()
