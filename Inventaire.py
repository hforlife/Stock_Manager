import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedStyle
import datetime
from dateutil.parser import parse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


class Category:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("INVENTAIRES")
        self.root.config(bg="lightgray")
        self.root.focus_force()
    # Dégradé de couleur en arrière-plan
        style = ThemedStyle(root)
        style.set_theme("plastik")

# Titre
        gestion_title = tk.Label(root, text="INVENTAIRE", font=("Poppins", 20, "bold"), bg="#F66B0E", fg="white")
        gestion_title.place(x=150, y=3 , width=1000)

# Entrées pour les dates
        date_label = tk.Label(root, text="Date du: ", font=("Poppins", 20), bg="lightgray")
        date_label.place(x=300, y=130)
        self.date_debut = tk.Entry(root, font=("Poppins", 15))
        self.date_debut.place(x=430, y=130, width=150, height=38)
        date_label = tk.Label(root, text="Au: ", font=("Poppins", 20), bg="lightgray")
        date_label.place(x=620, y=130)
        self.date_fin = tk.Entry(root, font=("Poppins", 15))
        self.date_fin.place(x=670, y=130, width=150, height=38)

# Bouton Recherche
        btn_ok = tk.Button(root, text="Recherche", font=("Poppins", 15), command=self.on_submit, bd=5,relief=tk.GROOVE, bg="#F66B0E")
        btn_ok.place(x=520, y=185, height=50, width=150)
        btn_pdf = tk.Button(root, text="PDF", font=("Poppins", 15), command=self.create_pdf, bd=5,relief=tk.GROOVE, bg="#F66B0E")
        btn_pdf.place(x=720, y=185, height=50, width=150)

# Affichage
        result_Frame = tk.Frame(root, bd=5, relief=tk.GROOVE, bg="#F66B0E")
        result_Frame.place(x=200, y=250, width=850, height=335)

# Tableau pour afficher les données
        scroll_x = tk.Scrollbar(result_Frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(result_Frame, orient=tk.VERTICAL)
        self.tabl_resul = ttk.Treeview(result_Frame, columns=("nom_produit", "prix_unit", "quantites_vente","total",
                                                              "date"),xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabl_resul.pack(fill=tk.BOTH, expand=1)
        scroll_x.config(command=self.tabl_resul.xview)
        scroll_y.config(command=self.tabl_resul.yview)

# Entête du tableau
        self.tabl_resul.heading("nom_produit", text="Nom Produit")
        self.tabl_resul.heading("prix_unit", text="Prix Unit")
        self.tabl_resul.heading("quantites_vente", text="Quantités de vente")
        self.tabl_resul.heading("total", text="Total")
        self.tabl_resul.heading("date", text="Date")
        self.tabl_resul["show"] = "headings"

# Largeur de chaque colonne
        self.tabl_resul.column("nom_produit", width=10)
        self.tabl_resul.column("prix_unit", width=10)
        self.tabl_resul.column("quantites_vente", width=10)
        self.tabl_resul.column("total", width=10)
        self.tabl_resul.column("date", width=10)

# Variables pour les totaux
        self.totalinventaire = tk.StringVar()
        self.totalinventairebotique = tk.StringVar()

# Affichage du total de vente
        total_label = tk.Label(root, text="Total de Vente :", font=("Lato", 20), bg="lightgray")
        total_label.place(x=410, y=600)
        id_total = tk.Entry(root, textvariable=self.totalinventaire, font=("times new roman", 20), bg="lightgray",state="readonly")
        id_total.place(x=610, y=600, width=200)
        self.totalinventairebotique = tk.StringVar()
        self.totalinventairebotique.set("0")  # Vous pouvez définir une valeur initiale si nécessaire
        connection = sqlite3.connect("Alimentation.db")
        cur = connection.cursor()
        cur.execute(f"select prix , quantiter from listeproduit ")
        rows = cur.fetchall()
        totale = sum([row[0] * row[1] for row in rows])
        self.totalinventairebotique.set(totale)  # Utilisez .set() pour mettre à jour la valeur de la variable StringVar
        connection.commit()
        connection.close()

      # id_total_boutique = tk.Label(root, text=f"Produits non Vendus : {totale} FCFA",font=("times new roman", 20), bg="lightgray")
        #id_total_boutique.place(x=200, y=70, width=850, height=50)

    def create_pdf(self):
        # Récupérez les données du tableau
        data = []
        # Entêtes de colonnes
        column_headers = ["Nom Produit", "Prix Unit", "Quantités de Vente","Total", "Date"]
        data.append(column_headers)
        for item in self.tabl_resul.get_children():
            values = self.tabl_resul.item(item, 'values')
            data.append(values)
        if data:
            # Récupérez les dates saisies par l'utilisateur
            date_debut = self.date_debut.get()
            date_fin = self.date_fin.get()
            # Crée un fichier PDF nommé "INVENTAIRE.pdf"
            doc = SimpleDocTemplate("INVENTAIRE.pdf", pagesize=letter)
            # Crée une liste vide pour stocker les données du tableau
            elements = []
            # Ajoute les dates saisies au PDF
            date_line = [f"Période : Du {date_debut} Au {date_fin}"]
            elements.append(Table([date_line]))
            # Crée un tableau à partir des données
            table = Table(data)
            # Ajoute le style au tableau
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Poppins'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])
            table.setStyle(style)
            # Ajoute le tableau à la liste d'éléments
            elements.append(table)
            # Ajoute une ligne avec le total de vente
            total_line = [f"Total de Vente : {self.totalinventaire.get()}"]
            elements.append(Table([total_line]))
            # Génère le fichier PDF
            doc.build(elements)
            messagebox.showinfo("Succès", "PDF Généré avec succés", parent=self.root)

    def afficher_erreurA(self):
        messagebox.showerror("Erreur", "Premier format incorrect. Veuillez utiliser le format JJ/MM/AAAA",parent=self.root)
    def afficher_erreurB(self):
        messagebox.showerror("Erreur", "Deuxième format incorrect. Veuillez utiliser le format JJ/MM/AAAA",parent=self.root)

    def on_submit(self):
        user_input_debut = self.date_debut.get()
        user_input_fin = self.date_fin.get()
        try:
            date1 = datetime.datetime.strptime(user_input_debut, "%d/%m/%Y").date()
        except ValueError:
            self.afficher_erreurA()
        try:
            date2 = datetime.datetime.strptime(user_input_fin, "%d/%m/%Y").date()
        except ValueError:
            self.afficher_erreurB()
        if date2 >= date1:
            try:
                connection = sqlite3.connect("Alimentation.db")
                cursor = connection.cursor()
                cursor.execute("SELECT nomproduit, prix, SUM(quantiter) AS quantiter,SUM(total) AS total, date FROM listevente WHERE date >= ? AND date <= ? GROUP BY nomproduit",(date1, date2))
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.tabl_resul.delete(*self.tabl_resul.get_children())
                    for row in rows:
                        self.tabl_resul.insert("", tk.END, values=row)
                else:
                    messagebox.showinfo("Information", "Aucune donnée trouvée pour cette période.", parent=self.root)
            except sqlite3.Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la requête SQL : {e}", parent=self.root)
            finally:
                connection.close()
                self.calculetotal()
        else:
            messagebox.showerror("Erreur","Votre demande est impossible car votre première date est plus récente que la deuxième date saisie", parent=self.root)

    def calculetotal(self):
        user_input_debut = self.date_debut.get()
        user_input_fin = self.date_fin.get()
        try:
            date1 = datetime.datetime.strptime(user_input_debut, "%d/%m/%Y").date()
        except ValueError:
            self.afficher_erreurA()
        try:
            date2 = datetime.datetime.strptime(user_input_fin, "%d/%m/%Y").date()
        except ValueError:
            self.afficher_erreurB()
        try:
            user_date = parse(user_input_debut)
            date_debut = user_date.date()
            try:
                user_date = parse(user_input_fin)
                date_fin = user_date.date()
                if date2 >= date1:
                    connection = sqlite3.connect("Alimentation.db")
                    cur = connection.cursor()
                    cur.execute("SELECT SUM(total) FROM listevente WHERE date >= ? AND date <= ?",(date1, date2))
                    result = cur.fetchone()
                    if result and result[0] is not None:
                        total = result[0]
                        self.totalinventaire.set(total)
                    else:
                        self.totalinventaire.set("1")
                    connection.commit()
                    connection.close()
                else:
                    messagebox.showerror("Erreur","Votre demande est impossible car votre premier date est plus récente que la deuxième date saisie",parent=self.root)
            except ValueError:
                messagebox.showerror("Erreur", "Deuxième format invalide", parent=self.root)
        except ValueError:
            messagebox.showerror("Erreur", "Premier format invalide", parent=self.root)


if __name__ == "__main__":
    root = tk.Tk()
    system = Category(root)
    root.mainloop()
