import tkinter as tk
from tkinter import ttk


class CRM:

    def __init__(self, root):
        self.root = root

        self.root.title("CRM - Gestionare Clienti")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F6F8")

        # Titlu
        self.title_label = tk.Label(
            root,
            text="CRM Gestionare Clienti",
            font=("Arial", 20, "bold"),
            bg="#F4F6F8",
            fg="#2C3E50"
        )
        self.title_label.pack(pady=15)

        # Frame pentru datele clientului
        self.form_frame = tk.Frame(root, bg="#F4F6F8")
        self.form_frame.pack()

        # Nume Client
        self.name_label = tk.Label(
            self.form_frame,
            text="Nume Client",
            bg="#F4F6F8"
        )
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.name_entry = tk.Entry(
            self.form_frame,
            width=30
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Email
        self.email_label = tk.Label(
            self.form_frame,
            text="Email",
            bg="#F4F6F8"
        )
        self.email_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.email_entry = tk.Entry(
            self.form_frame,
            width=30
        )
        self.email_entry.grid(row=1, column=1, padx=10, pady=5)

        # Telefon
        self.phone_label = tk.Label(
            self.form_frame,
            text="Telefon",
            bg="#F4F6F8"
        )
        self.phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.phone_entry = tk.Entry(
            self.form_frame,
            width=30
        )
        self.phone_entry.grid(row=2, column=1, padx=10, pady=5)

        # Oras
        self.city_label = tk.Label(
            self.form_frame,
            text="Oras",
            bg="#F4F6F8"
        )
        self.city_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.city_entry = tk.Entry(
            self.form_frame,
            width=30
        )
        self.city_entry.grid(row=3, column=1, padx=10, pady=5)

        # Stare Client
        self.status_label = tk.Label(
            self.form_frame,
            text="Stare Client",
            bg="#F4F6F8"
        )
        self.status_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.status_combobox = ttk.Combobox(
            self.form_frame,
            values=["Prospect", "Activ", "VIP", "Inactiv"],
            state="readonly",
            width=27
        )
        self.status_combobox.grid(row=4, column=1, padx=10, pady=5)

        # Butoane
        self.button_frame = tk.Frame(root, bg="#F4F6F8")
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(
            self.button_frame,
            text="Adauga Client",
            command=self.adauga_client,
            bg="#3498DB",
            fg="white",
            width=15
        )
        self.add_button.grid(row=0, column=0, padx=5)

        self.delete_button = tk.Button(
            self.button_frame,
            text="Sterge Client",
            command=self.sterge_client,
            bg="#E74C3C",
            fg="white",
            width=15
        )
        self.delete_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(
            self.button_frame,
            text="Goleste Tot",
            command=self.goleste_campuri,
            bg="#95A5A6",
            fg="white",
            width=15
        )
        self.clear_button.grid(row=0, column=2, padx=5)

        self.close_button = tk.Button(
            self.button_frame,
            text="Inchide Aplicatia",
            command=self.inchide_aplicatia,
            bg="#2C3E50",
            fg="white",
            width=15
        )
        self.close_button.grid(row=0, column=3, padx=5)

        # Listbox
        self.clients_listbox = tk.Listbox(
            root,
            width=75,
            height=8
        )
        self.clients_listbox.pack(pady=10)

        # Total clienti
        self.total_label = tk.Label(
            root,
            text="Total clienti: 0",
            bg="#F4F6F8",
            fg="#2C3E50",
            font=("Arial", 10, "bold")
        )
        self.total_label.pack()

        # Cautare client
        self.search_frame = tk.Frame(root, bg="#F4F6F8")
        self.search_frame.pack(pady=10)

        self.search_entry = tk.Entry(
            self.search_frame,
            width=30
        )
        self.search_entry.grid(row=0, column=0, padx=5)

        self.search_button = tk.Button(
            self.search_frame,
            text="Cauta Client",
            command=self.cauta_client,
            bg="#8E44AD",
            fg="white"
        )
        self.search_button.grid(row=0, column=1, padx=5)

        # Export simulat
        self.export_button = tk.Button(
            root,
            text="Export Simulat",
            command=self.export_simulat,
            bg="#16A085",
            fg="white"
        )
        self.export_button.pack(pady=5)

        # Mesaje
        self.message_title_label = tk.Label(
            root,
            text="Mesaje",
            bg="#F4F6F8"
        )
        self.message_title_label.pack()

        self.message_label = tk.Label(
            root,
            text="",
            bg="#F4F6F8"
        )
        self.message_label.pack(pady=5)

        # Footer
        self.footer_label = tk.Label(
            root,
            text="CRM Informatic M IT\nVersiunea 1.0",
            bg="#F4F6F8",
            fg="#7F8C8D"
        )
        self.footer_label.pack(side="bottom", pady=10)

    def adauga_client(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        city = self.city_entry.get()
        status = self.status_combobox.get()

        if name == "" or email == "" or phone == "" or city == "" or status == "":
            self.message_label.config(
                text="Completeaza toate campurile!",
                fg="red"
            )
            return

        client = f"{name} | {email} | {city} | {status}"

        self.clients_listbox.insert(tk.END, client)

        self.goleste_campuri()

        self.message_label.config(
            text="Client adaugat cu succes!",
            fg="green"
        )

        self.actualizeaza_total()

    def sterge_client(self):
        selected = self.clients_listbox.curselection()

        if not selected:
            self.message_label.config(
                text="Selecteaza un client!",
                fg="red"
            )
            return

        self.clients_listbox.delete(selected[0])

        self.actualizeaza_total()

    def goleste_campuri(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.city_entry.delete(0, tk.END)

        self.status_combobox.set("")

        self.message_label.config(text="")

    def inchide_aplicatia(self):
        self.root.destroy()

    def actualizeaza_total(self):
        total = self.clients_listbox.size()

        self.total_label.config(
            text=f"Total clienti: {total}"
        )

    def cauta_client(self):
        search_name = self.search_entry.get()

        found = False

        for client in self.clients_listbox.get(0, tk.END):
            name = client.split(" | ")[0]

            if name == search_name:
                found = True
                break

        if found:
            self.message_label.config(
                text="Client gasit!",
                fg="green"
            )
        else:
            self.message_label.config(
                text="Clientul nu exista!",
                fg="red"
            )

    def export_simulat(self):
        self.message_label.config(
            text="Datele au fost exportate cu succes!",
            fg="green"
        )


root = tk.Tk()
app = CRM(root)
root.mainloop()