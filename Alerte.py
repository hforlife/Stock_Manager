from tkinter import *
from tkinter import ttk
import sqlite3
from ttkthemes import ThemedStyle


class Alerte:
    def __init__(self, root):
        roote = root
        roote.title("ALERTE")
        window_width = 700
        window_height = 480
        screen_width = roote.winfo_screenwidth()
        screen_height = roote.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        roote.geometry(f"{window_width}x{window_height}+{x}+{y}")
        roote.config(bg="lightgray")
        style = ThemedStyle(root)
        style.set_theme("plastik")


        Gestion_Frame = Frame(roote, bd=5, relief=GROOVE, bg="lightgray")
        gestion_title = Label(roote, text="ALERTE", font=("Poppins", 25, "bold"), bg="lightgray", fg="#343A40")
        gestion_title.place(x=300, y=5)
        # Affichage
        result_Frame = Frame(roote, bd=5, relief=GROOVE, bg="lightgray")
        result_Frame.place(x=100, y=100, width=500, height=375)
        # tableau
        scroll_y = Scrollbar(result_Frame, orient=VERTICAL)
        self.tabl_resul = ttk.Treeview(result_Frame, columns=("nom_produit", "quantites_vente"),
                                       yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        self.tabl_resul.pack(fill=BOTH, expand=1)
        scroll_y.config(command=self.tabl_resul.yview)
        # l'entete
        self.tabl_resul.heading("nom_produit", text="Nom Produit")
        self.tabl_resul.heading("quantites_vente", text="Quantités Restantes")
        self.l = []
        # afficher les elements dans l'entete
        self.tabl_resul["show"] = "headings"
        # la taille de chaque colonne
        self.tabl_resul.column("nom_produit", width=250)
        self.tabl_resul.column("quantites_vente", width=250)
        self.tabl_resul.pack()
        connection = sqlite3.connect("Alimentation.db")
        cur = connection.cursor()
        cur.execute("select nomproduit,quantiter from listeproduit where alerte>=quantiter ")
        rows = cur.fetchall()
        if len(rows) != 0:
            self.tabl_resul.delete(*self.tabl_resul.get_children())
            for row in rows:
                self.tabl_resul.insert("", END, values=row)
        connection.commit()
        connection.close()


if __name__ == "__main__":
    root = Tk()
    system = Alerte(root)
    root.mainloop()
