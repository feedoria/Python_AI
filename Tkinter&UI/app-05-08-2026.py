import tkinter as tk # Importam modulul tkinker pentru aplicatii desktop
from tkinter import messagebox #importam messagebox pentru ferestre de tip popup( alerta, eroare etc)

class MiniCRM:
    def __init__(self, root):
        self.root = root #Root inseamna fereastra (aplicatia desktop)
        self.root.title("Mini CRM -Tkinker")
        self.root.geometry("4500x500") #Dimensiunea
        self.root.config(bg="#253a4a")

        self.clients = [] #Lista in care vom stoca clientii

        #Titlul aplicatiei
        title = tk.Label(
            root,
            text="Mini CRM",
            font=("Arial",22,"bold"),
            bg="#4e677a",
            fg="#162a39"
        )
        title.pack(pady=10) #Am pus spatiu de 10px 

        #Formular de introducere date client 
        form_frame = tk.Frame(root, bg="#3C4B56")
        form_frame.pack(pady=10) #Spatiu de 10px

        #Tabelul nume client
        tk.Label(
            form_frame,
            text="Nume:",
            bg="#0c2444",
            font=("Arial",12)
        ).grid(row=0,column=0, sticky="w") #Pozitionam label-ul in grid (rand 0, coloana 0)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0,column=1, pady=10) #Pady inseamna ca punem un spatiu intre ele de 10px

        #Email client 
        tk.Label(
            form_frame,
            text="Email",
            bg="#0c2444",
            font=("Arial",12)
        ).grid(row=0,column=0, sticky="w")
        self.email_entry = tk.Entry(form_frame,width=30)
        self.email_entry.grid(row=1,column=1,pady=5)

        tk.Label(
            form_frame,
            text="Telefon",
            bg="#0c2444",
            font=("Arial",12)
        ).grid(row=2,column=0, sticky="w")
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=2,column=1,pady=5)

        tk.Label(
            form_frame,
            text="Adresa",
            bg="#0c2444",
            font=("Arial",12)
        ).grid(row=3,column=0, sticky="w")
        self.adresa_entry = tk.Entry(form_frame,width=30)
        self.adresa_entry.grid(row=3,column=2,pady=5)

        #Buton pentru adaugare client
        add_btn = tk.Button(
            root,
            text="Adauga Client",
            font=("Arial",12,"bold"),
            bg="#577fb3",
            fg="white",
            width=20,
            command=self.add_client
        )
        add_btn.pack(pady=10)

        #Lista de clienti (vizlualizare)
        self.client_listbox = tk.Listbox(
            root,
            width=50,
            height=12,
            font=("Arial",11),
            bg="white", #background
            fg="#040a12" #asta e culaorea scrisului
        )
        self.client_listbox.pack(pady=10)

        #Buton de stergere
        delete_btn = tk.Button(
            root,
            text="Sterge Client",
            font=("Arial",12,"bold"),
            bg="white", #background
            fg="black",
            command=self.delete_client
        )
        delete_btn.pack(pady=10)
    def add_client(self):
        name = self.name_entry.get().strip()
        email=self.email_entry.get().strip()
        phone=self.phone_entry.get().strip()
        address=self.adresa_entry.get().strip()

        #Validare simpla - verificam daca nu sunt goale
        if not name or not email or not phone or not address:
            messagebox.showwarning("Eroare","Completeaza toate campurile")
            return

        #Cream un dictionar cu datele clientului
        client = {
            "name":name,
            "email":email,
            "phone":phone,
            "address":address
        }
        self.clients.append(client)
        #Adaugam clientul in listbox pentru vizualizare
        self.client_listbox.insert(
            tk.END,
            f"{name} | {email} | {phone} | {address}"
        )
        #Curatam campurile dupa adaugare 
        self.name_entry.delete(0,tk.END)
        self.email_entry.delete(0,tk.END)
        self.phone_entry.delete(0,tk.END)
        self.adresa_entry.delete(0,tk.END)

    #Functie pentru stergere
    def delete_client(self):
        selected = self.client_listbox.curselection()

        if not selected:
            messagebox.showwarning("Eroare","Selecteaza un client din lista")
            return

        index = selected[0]
        self.client_listbox.delete(index)
        del self.clients[index]

root = tk.Tk()
app = MiniCRM(root)
root.mainloop()