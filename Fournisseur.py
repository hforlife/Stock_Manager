from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import tkinter as tk
import datetime
from datetime import date,timedelta
from ttkthemes import ThemedStyle


class Supplier:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1110x570+240+110")
        self.root.title("Gestion des Fournisseur/client")
        self.root.config(bg="lightgray")
        style = ThemedStyle(root)
        style.set_theme("plastik")


        # system variables
        self.searchOption_var = StringVar()
        self.searchText_var = StringVar()
        self.apreciation = StringVar()
        self.supp_invoice_var = StringVar()
        self.name_var = StringVar()
        self.contact_var = StringVar()
        self.date = date.today()

        # search employee
        search_frame = LabelFrame(self.root, text="Chercher un Fournisseur", font=("Poppins", 11, "normal"), bg="white", bd=2)
        search_frame.place(x=250, y=260, width=800, height=70)

        # search options
        search_label = Label(search_frame, text="Recherche par Facture No.", font=("Poppins", 11, "normal"), bg="white")
        search_label.place(x=-5, y=10)

        search_box = Entry(search_frame, textvariable=self.searchText_var, font=("Poppins", 11, "normal"), bg="#EEE6CE")
        search_box.place(x=200, y=10, width=200, height=25)
        search_btn = Button(search_frame, text="Chercher", command=self.search_supp, font=("Poppins", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        search_btn.place(x=410, y=10, width=150, height=25)


        # title
        title = Label(self.root, text="Information du Fournisseur", font=("Poppins", 14, "normal"), bg="#F66B0E", fg="white")
        title.place(x=50, y=20, width=1000)
        # content
        # -----first row-----
        supp_invoice_label = Label(self.root, text="Facture No.", font=("Poppins", 14, "normal"), bg="lightgray")
        supp_invoice_label.place(x=50, y=70)
        supp_invoice_txt = Entry(self.root, textvariable=self.supp_invoice_var, font=("Poppins", 14, "normal"), bg="white", bd=1)
        supp_invoice_txt.place(x=170, y=70, width=180)

        # -----second row-----
        name_label = Label(self.root, text="Nom", font=("Poppins", 14, "normal"), bg="lightgray")
        name_label.place(x=50, y=110)
        name_txt = Entry(self.root, textvariable=self.name_var, font=("Poppins", 14, "normal"), bg="white", bd=1)
        name_txt.place(x=170, y=110, width=180)

        # -----third row-----
        contact_label = Label(self.root, text="Contact", font=("Poppins", 14, "normal"), bg="lightgray")
        contact_label.place(x=50, y=150)
        contact_txt = Entry(self.root, textvariable=self.contact_var, font=("Poppins", 14, "normal"), bg="white", bd=1)
        contact_txt.place(x=170, y=150, width=180)

        # -----fourth row-----

        address_desc = Label(self.root, text="Description", font=("Poppins", 14, "normal"), bg="lightgray")
        address_desc.place(x=50, y=190)
        self.desc_txt = Text(self.root, font=("Poppins", 14, "normal"), bg="white", bd=1)
        self.desc_txt.place(x=170, y=190, width=300, height=60)

        self.entr_nomproduit = ttk.Combobox(self.root, textvariable=self.apreciation, font=("Poppins", 15), state="readonly")
        self.entr_nomproduit["values"] = ("En Avance","A Temps","En Retard")
        self.entr_nomproduit.current(0)
        self.entr_nomproduit.place(x=500, y=100, width=300, height=60)

        # buttons
        add_btn = Button(self.root, text="Ajouter", command=self.add_supp, font=("Poppins", 11, "bold"), bg="#2EB086", fg="white", bd=3, cursor="hand2")
        add_btn.place(x=500, y=225, width=110, height=25)
        update_btn = Button(self.root, text="Modifier", command=self.update_supp, font=("Poppins", 11, "bold"), bg="#0AA1DD", fg="white", bd=3, cursor="hand2")
        update_btn.place(x=620, y=225, width=110, height=25)
        delete_btn = Button(self.root, text="Supprimer", command=self.delete_supp, font=("Poppins", 11, "bold"), bg="#B8405E", fg="white", bd=3, cursor="hand2")
        delete_btn.place(x=740, y=225, width=110, height=25)
        clear_btn = Button(self.root, text="Effacer", command=self.clear, font=("Poppins", 11, "bold"), bg="#313552", fg="white", bd=3, cursor="hand2")
        clear_btn.place(x=860, y=225, width=110, height=25)

        # supplier list
        supp_list_frame = Frame(self.root, bd=3, relief=RIDGE)
        supp_list_frame.place(x=0, y=350, relwidth=1, height=220)

        scroll_y = Scrollbar(supp_list_frame, orient=VERTICAL)
        scroll_x = Scrollbar(supp_list_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        list_columns = ("facture", "nom", "contact", "desc","appreciation","date")
        self.supp_list_table = ttk.Treeview(supp_list_frame, columns=list_columns, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.supp_list_table.pack(fill=BOTH, expand=1)
        scroll_x.config(command=self.supp_list_table.xview)
        scroll_y.config(command=self.supp_list_table.yview)

        self.supp_list_table.heading("facture", text="Facture No.")
        self.supp_list_table.heading("nom", text="Nom")
        self.supp_list_table.heading("contact", text="Contact")
        self.supp_list_table.heading("desc", text="Description")
        self.supp_list_table.heading("date", text="DATE")
        self.supp_list_table.heading("appreciation", text="Appreciation")
        self.supp_list_table["show"] = "headings"

        self.supp_list_table.column("facture", width=90)
        self.supp_list_table.column("nom", width=100)
        self.supp_list_table.column("contact", width=100)
        self.supp_list_table.column("desc", width=100)
        self.supp_list_table.column("date", width=100)
        self.supp_list_table.column("appreciation", width=100)

        self.supp_list_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_supp()

    # supplier methods
    def add_supp(self):
        con = sqlite3.connect("Alimentation.db")
        cur = con.cursor()
        try:
            if self.supp_invoice_var.get() == "":
                messagebox.showerror("Erreur", "Facture no. du fournissuer doit être saisie", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.supp_invoice_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Erreur", "Facture no. deja existant, saisir un autre", parent=self.root)
                else:
                    values_to_insert = (self.supp_invoice_var.get(),
                                        self.name_var.get(),
                                        self.contact_var.get(),
                                        self.desc_txt.get('1.0', END),
                                        self.apreciation.get(),
                                        self.date)
                    cur.execute("INSERT INTO supplier (invoice, name, contact, desc, apreciation,date) VALUES (?,?,?,?,?,?)", values_to_insert)
                    con.commit()
                    self.show_supp()
                    messagebox.showinfo("Succès", "Fournisseur est ajouté avec succès", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def show_supp(self):
        con = sqlite3.connect("Alimentation.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supp_list_table.delete(*self.supp_list_table.get_children())
            for row in rows:
                self.supp_list_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        table_focus = self.supp_list_table.focus()
        table_content = (self.supp_list_table.item(table_focus))
        row = table_content["values"]
        # print(row)

        self.supp_invoice_var.set(row[0])
        self.name_var.set(row[1])
        self.contact_var.set(row[2])
        self.desc_txt.delete('1.0', END)
        self.desc_txt.insert(END, row[3])
        self.apreciation.set(row[4])

    def update_supp(self):
        try:
            invoice_number = self.supp_invoice_var.get()

            if invoice_number == "":
                messagebox.showerror("Erreur", "Le numéro de facture du fournisseur doit être saisi", parent=self.root)
            else:
                with sqlite3.connect("Alimentation.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM supplier WHERE invoice=?", (invoice_number,))
                    row = cur.fetchone()

                    if row is None:
                        messagebox.showerror("Erreur", "Numéro de facture invalide", parent=self.root)
                    else:
                        # Validation des champs de saisie (ajoutez des validations selon vos besoins)
                        if not self.name_var.get() or not self.contact_var.get() or not self.desc_txt.get("1.0",
                                                                                                          "end-1c") or not self.apreciation.get():
                            messagebox.showerror("Erreur", "Veuillez remplir tous les champs", parent=self.root)
                            return

                        values_to_insert = (
                            self.name_var.get(),
                            self.contact_var.get(),
                            self.desc_txt.get("1.0", "end-1c"),
                            self.apreciation.get(),
                            invoice_number,
                        )

                        # Utilisation d'une transaction
                        cur.execute("UPDATE supplier SET name=?, contact=?, desc=?, apreciation=? WHERE invoice=?",
                                    values_to_insert)
                        con.commit()

                        self.show_supp()
                        messagebox.showinfo("Succès", "Fournisseur modifié avec succès", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def delete_supp(self):
        con = sqlite3.connect('Alimentation.db')
        cur = con.cursor()
        try:
            if self.supp_invoice_var.get() == "":
                messagebox.showerror("Erreur", "Facture no. doit être saisi", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.supp_invoice_var.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Erreur", "Facture no. Invalid", parent=self.root)
                else:
                    user_confirm = messagebox.askyesno("Confirmation", "Confirmer la suppression?", parent=self.root)
                    if user_confirm:
                        cur.execute("DELETE FROM supplier WHERE invoice=?", (self.supp_invoice_var.get(),))
                        con.commit()
                        messagebox.showinfo("Succès", "Fournisseur supprimé avec succès", parent=self.root)
                        self.show_supp()
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)

    def clear(self):
        self.supp_invoice_var.set("")
        self.name_var.set("")
        self.contact_var.set("")
        self.desc_txt.delete('1.0', END)
        self.searchText_var.set("")
        self.show_supp()

    def search_supp(self):
        con = sqlite3.connect('Alimentation.db')
        cur = con.cursor()
        try:
            if self.searchText_var.get() == "":
                messagebox.showerror("Erreur", "Champ de recherche vide", parent=self.root)
            else:
                cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.searchText_var.get(),))
                row = cur.fetchone()
                if row is not None:
                    self.supp_list_table.delete(*self.supp_list_table.get_children())
                    self.supp_list_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Erreur", "Aucun fournisseur trouvé!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Erreur", f"Erreur: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    system = Supplier(root)
    root.mainloop()
