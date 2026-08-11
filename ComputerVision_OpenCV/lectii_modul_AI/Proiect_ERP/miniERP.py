import tkinter as tk

from tkinter import ttk  # E pentru un design mult mai profesional

from tkinter import messagebox  # Ne permite sa afisam mesaje utilizatorilor


class ERP:

    def __init__(self, root):
        self.root = root

        self.root.title("Nexus ERP | Depozit")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)  # Ca sa nu marim sau micsoram fereastra
        self.root.configure(bg="#F4F6F8")

        # Datele aplicatiei
        self.products = []

        self.clients = []

        self.invoices = []

        # Id-uri
        self.product_id = 1
        self.client_id = 1
        self.invoice_id = 1001

        # Date de test
        self.products.append({
            "id": 1,
            "name": "Laptop Lenovo",
            "price": 3500.00,
            "stock": 12
        })

        self.products.append({
            "id": 2,
            "name": "Iphone 17 pro max",
            "price": 7000,
            "stock": 40
        })

        # Adaugam un client de test
        self.clients.append({
            "id": 1,
            "name": "SC Tech SRL",
            "email": "",
            "phone": ""
        })

        self.product_id = 3
        self.client_id = 2

        # Construim interfata
        self.create_sidebar()
        self.create_main_area()
        self.show_dashboard()


    def create_sidebar(self):

        # Creez un frame
        self.sidebar = tk.Frame(
            self.root,
            bg="#CACAD2",
            width=220
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        tk.Label(
            self.sidebar,
            text="Nexus",
            bg="#B9B9BC",
            fg="black",
            font=("Arial", 24, "bold")
        ).pack(
            pady=(35, 0)
        )

        # Subtitlul aplicatiei
        tk.Label(
            self.sidebar,
            text="ERP | Depozit",
            bg="#B9B9D1",
            fg="#8A99A8",
            font=("Arial", 9)
        ).pack(
            pady=(2, 35)
        )

        # Butoane din Sidebar
        self.create_menu_button(
            "Dashboard",
            self.show_dashboard
        )

        self.create_menu_button(
            "Produse",
            self.show_products
        )

        self.create_menu_button(
            "Clienti",
            self.show_clients
        )

        self.create_menu_button(
            "Facturi",
            self.show_invoices
        )


    def create_menu_button(self, text, command):

        tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg="#A5A5B5",
            fg="#65686B",
            bd=0,
            font=("Arial", 11),
            cursor="hand2",
            pady=14,
            padx=35
        ).pack(
            fill="x"
        )


    # Zona principala
    def create_main_area(self):

        self.main_area = tk.Frame(
            self.root,
            bg="#F4F6F8"
        )

        self.main_area.pack(
            side="right",
            fill="both",
            expand=True
        )


    # Stergem continutul din zona principala
    def clear_main_area(self):

        for widget in self.main_area.winfo_children():
            widget.destroy()


    # Dashboard
    def show_dashboard(self):

        self.clear_main_area()

        tk.Label(
            self.main_area,
            text="Dashboard",
            bg="#F4F6F8",
            fg="#222222",
            font=("Arial", 26, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(40, 10)
        )


    # Pagina Produse
    def show_products(self):

        self.clear_main_area()

        # Titlul
        tk.Label(
            self.main_area,
            text="Produse",
            bg="#F4F6F8",
            fg="#222222",
            font=("Arial", 26, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        # Subtitlu
        tk.Label(
            self.main_area,
            text="Gestioneaza produsele din depozit",
            bg="#F4F6F8",
            fg="#777777",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40,
            pady=(0, 20)
        )

        # Buton adaugare produs
        tk.Button(
            self.main_area,
            text="+ Adauga produs",
            command=self.add_product_window,
            bg="#4F46E5",
            fg="white",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(
            anchor="e",
            padx=40,
            pady=(0, 20)
        )

        # Tabelul cu produse
        table_frame = tk.Frame(
            self.main_area,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        # Cream tabelul
        self.product_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "price", "stock"),
            show="headings",
            height=15
        )

        # Coloane
        self.product_table.heading(
            "id",
            text="ID"
        )

        self.product_table.heading(
            "name",
            text="Produs"
        )

        self.product_table.heading(
            "price",
            text="Pret"
        )

        self.product_table.heading(
            "stock",
            text="Stoc"
        )

        # Dimensiuni coloane
        self.product_table.column(
            "id",
            width=70,
            anchor="center"
        )

        self.product_table.column(
            "name",
            width=350
        )

        self.product_table.column(
            "price",
            width=150,
            anchor="center"
        )

        self.product_table.column(
            "stock",
            width=120,
            anchor="center"
        )

        self.product_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Afisam produsele existente
        self.refresh_products()


    # Afisam produsele in tabel
    def refresh_products(self):

        # Stergem produsele existente din tabel
        for item in self.product_table.get_children():
            self.product_table.delete(item)

        # Adaugam produsele din lista
        for product in self.products:

            self.product_table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["name"],
                    f"{product['price']:.2f} lei",
                    product["stock"]
                )
            )


    # Fereastra pentru adaugarea unui produs
    def add_product_window(self):

        window = tk.Toplevel(self.root)

        window.title("Adauga produs")
        window.geometry("400x350")
        window.resizable(False, False)
        window.configure(bg="#F4F6F8")

        tk.Label(
            window,
            text="Adauga produs",
            bg="#F4F6F8",
            fg="#222222",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(25, 20)
        )

        # Nume produs
        tk.Label(
            window,
            text="Nume produs:",
            bg="#F4F6F8",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        name_entry = tk.Entry(
            window,
            font=("Arial", 11)
        )

        name_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 15)
        )

        # Pret
        tk.Label(
            window,
            text="Pret:",
            bg="#F4F6F8",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        price_entry = tk.Entry(
            window,
            font=("Arial", 11)
        )

        price_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 15)
        )

        # Stoc
        tk.Label(
            window,
            text="Stoc:",
            bg="#F4F6F8",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        stock_entry = tk.Entry(
            window,
            font=("Arial", 11)
        )

        stock_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 20)
        )


        # Functia care adauga produsul
        def save_product():

            name = name_entry.get()
            price = price_entry.get()
            stock = stock_entry.get()

            # Verificam daca utilizatorul a completat toate campurile
            if name == "" or price == "" or stock == "":
                messagebox.showerror(
                    "Eroare",
                    "Completeaza toate campurile!"
                )
                return

            # Incercam sa transformam pretul si stocul in numere
            try:
                price = float(price)
                stock = int(stock)

            except ValueError:

                messagebox.showerror(
                    "Eroare",
                    "Pretul trebuie sa fie numar, iar stocul numar intreg!"
                )

                return

            # Cream produsul
            product = {
                "id": self.product_id,
                "name": name,
                "price": price,
                "stock": stock
            }

            # Adaugam produsul in lista
            self.products.append(product)

            # Incrementam ID-ul pentru urmatorul produs
            self.product_id += 1

            # Inchidem fereastra
            window.destroy()

            # Reafisam pagina Produse
            self.show_products()


        # Buton salvare
        tk.Button(
            window,
            text="Salveaza produs",
            command=save_product,
            bg="#4F46E5",
            fg="white",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            pady=10
        ).pack(
            fill="x",
            padx=40
        )


    # Pagina Clienti
    def show_clients(self):

        self.clear_main_area()

        # Titlul
        tk.Label(
            self.main_area,
            text="Clienti",
            bg="#F4F6F8",
            fg="#222222",
            font=("Arial", 26, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(35, 5)
        )

        # Subtitlu
        tk.Label(
            self.main_area,
            text="Gestioneaza clientii din sistem",
            bg="#F4F6F8",
            fg="#777777",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40,
            pady=(0, 20)
        )

        # Buton adaugare client
        tk.Button(
            self.main_area,
            text="+ Adauga client",
            command=self.add_clients_window,
            bg="#4F46E5",
            fg="white",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(
            anchor="e",
            padx=40,
            pady=(0, 20)
        )

        # Tabelul cu clienti
        table_frame = tk.Frame(
            self.main_area,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=10
        )

        # Cream tabelul
        self.client_table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "email", "phone"),
            show="headings",
            height=15
        )

        # Coloane
        self.client_table.heading(
            "id",
            text="ID"
        )

        self.client_table.heading(
            "name",
            text="Nume firma"
        )

        self.client_table.heading(
            "email",
            text="Email"
        )

        self.client_table.heading(
            "phone",
            text="Telefon"
        )

        # Dimensiuni coloane
        self.client_table.column(
            "id",
            width=70,
            anchor="center"
        )

        self.client_table.column(
            "name",
            width=300
        )

        self.client_table.column(
            "email",
            width=280
        )

        self.client_table.column(
            "phone",
            width=180
        )

        self.client_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Afisam clientii existenti
        self.refresh_clients()


    # Afisam clientii in tabel
    def refresh_clients(self):

        # Stergem clientii existenti din tabel
        for item in self.client_table.get_children():
            self.client_table.delete(item)

        # Adaugam clientii din lista
        for client in self.clients:

            self.client_table.insert(
                "",
                "end",
                values=(
                    client["id"],
                    client["name"],
                    client["email"],
                    client["phone"]
                )
            )


    # Fereastra pentru adaugarea unui client
    def add_clients_window(self):

        window = tk.Toplevel(self.root)

        window.title("Adauga client")
        window.geometry("400x420")
        window.resizable(False, False)
        window.configure(bg="#F4F6F8")

        tk.Label(
            window,
            text="Adauga client",
            bg="#F4F6F8",
            fg="#222222",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(25, 20)
        )

        # Nume client
        tk.Label(
            window,
            text="Nume firma:",
            bg="#F4F6F8",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        name_entry = tk.Entry(
            window,
            font=("Arial", 11)
        )

        name_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 15)
        )

        # Email
        tk.Label(
            window,
            text="Email:",
            bg="#F4F6F8",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        email_entry = tk.Entry(
            window,
            font=("Arial", 11)
        )

        email_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 15)
        )

        # Telefon
        tk.Label(
            window,
            text="Telefon:",
            bg="#F4F6F8",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        phone_entry = tk.Entry(
            window,
            font=("Arial", 11)
        )

        phone_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 20)
        )


        # Functia care adauga clientul
        def save_client():

            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()

            # Verificam daca utilizatorul a completat toate campurile
            if name == "" or email == "" or phone == "":
                messagebox.showerror(
                    "Eroare",
                    "Completeaza toate campurile!"
                )
                return

            # Cream clientul
            client = {
                "id": self.client_id,
                "name": name,
                "email": email,
                "phone": phone
            }

            # Adaugam clientul in lista
            self.clients.append(client)

            # Incrementam ID-ul pentru urmatorul client
            self.client_id += 1

            # Inchidem fereastra
            window.destroy()

            # Reafisam pagina Clienti
            self.show_clients()


        # Buton salvare
        tk.Button(
            window,
            text="Salveaza client",
            command=save_client,
            bg="#4F46E5",
            fg="white",
            bd=0,
            font=("Arial", 11, "bold"),
            cursor="hand2",
            pady=10
        ).pack(
            fill="x",
            padx=40
        )


    # Pagina Facturi
    def show_invoices(self):

        self.clear_main_area()

        tk.Label(
            self.main_area,
            text="Facturi",
            bg="#F4F6F8",
            fg="#222222",
            font=("Arial", 26, "bold")
        ).pack(
            anchor="w",
            padx=40,
            pady=(40, 10)
        )


root = tk.Tk()
app = ERP(root)
root.mainloop()