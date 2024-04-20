from tkinter import *
from tkinter import messagebox
import os

def login():
    username = entry1.get()
    password = entry2.get()

    if username == " " and password == " ":
        messagebox.showerror('login', 'Champ vide non approuvé !')
    elif username == "login" and password == "12345":
        messagebox.showinfo('login', 'Vous êtes connecté avec succès !')
        root.destroy()
        os.system("python Admin_dashboard.py")
    else:
        messagebox.showerror('login', 'Mot de passe ou Nom d\'utilisateur invalide')


#Un formulaire de connexion
root = Tk()
root.configure(bg="#F66B0E")
root.title("Connexion")
root.geometry("550x300")

global entry1
global entry2

label1 = Label(root, text="Page de Connexion", bg="#F66B0E", fg="white", font=("Poppins", 20, "bold italic"))
label1.place(x=170, y=50)

label2 = Label(root, text="Nom d'utilisateur", bg="#F66B0E", fg="white", font=("Lato", 15, "bold"))
label2.place(x=90, y=110)

label3 = Label(root, text="Mot de passe", bg="#F66B0E", fg="white", font=("Lato", 15, "bold"))
label3.place(x=90, y=150)

entry1 = Entry(root, font=("Lato", 15))
entry1.place(x=250, y=110)

entry2 = Entry(root, font=("Lato", 15), show='*')
entry2.place(x=250, y=150)

button = Button(root, text="Connexion", bg="#F66B0E", fg="white", font=("lato", 12, "bold"), bd=5, command=login)
button.place(x=200, y=200)

root.bind('<Return>', lambda event=None: login())

root.mainloop()
