# Task – Aplicație Desktop pentru Gestionarea Bibliotecii (Tkinter)
# Context

# O bibliotecă dorește o aplicație desktop simplă pentru gestionarea 
# cărților disponibile. Aplicația trebuie să permită bibliotecarului să adauge,
#  să vizualizeze și să gestioneze cărțile într-o interfață ușor de utilizat.

# Aplicația trebuie realizată în Python folosind Tkinter și Programare Orientată 
# pe Obiecte (OOP).

# Cerințe

# Realizați o aplicație desktop numită Library Manager care să îndeplinească 
# următoarele cerințe:

# Interfață
# Fereastra trebuie să aibă un titlu sugestiv.
# Folosiți o interfață organizată și ușor de utilizat.
# Adăugați o zonă pentru introducerea datelor, o listă pentru afișarea cărților 
# și butoane pentru acțiuni.
# Formular

# Utilizatorul trebuie să poată introduce:

# Titlul cărții
# Autorul
# Categoria
# Anul apariției
# Numărul de exemplare disponibile
# Validare

# Înainte de adăugare verificați că:

# toate câmpurile sunt completate;
# anul este un număr;
# numărul de exemplare este un număr pozitiv.

# În cazul unei erori trebuie afișat un mesaj folosind messagebox.

# Funcționalități

# Aplicația trebuie să permită:

# adăugarea unei cărți;
# afișarea tuturor cărților într-o listă;
# ștergerea unei cărți selectate;
# editarea informațiilor unei cărți;
# golirea câmpurilor după adăugare.
# Căutare

# Adăugați o bară de căutare care să permită găsirea unei cărți după:

# titlu;
# autor;
# categorie.
# Statistici

# În partea de jos a ferestrei afișați:

# numărul total de cărți;
# numărul total de exemplare din bibliotecă.
# Bonus

# Implementați cel puțin trei dintre următoarele funcționalități:

# confirmare înainte de ștergere;
# sortare alfabetică după titlu;
# filtrare după categorie;
# afișarea datei și orei curente;
# generarea automată a unui ID pentru fiecare carte;
# buton pentru resetarea formularului.

# Obiectiv: dezvoltați o aplicație desktop simplă, bine organizată, 
# folosind Tkinter și OOP, care să permită gestionarea eficientă a unei 
# mici biblioteci.

import tkinter as tk
from tkinter import messagebox


class MiniCRM:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini CRM - Tkinter")
        self.root.geometry("450x700")
        self.root.config(bg="#ecbb8d")

        self.books = []
        self.total_copies = 0

        title = tk.Label(
            root,
            text="Library Manager",
            font=("Arial", 22, "bold"),
            bg="#422d05",
            fg="#AC9470"
        )
        title.pack(pady=10)

        form_frame = tk.Frame(root, bg="#5B432C")
        form_frame.pack(pady=10)

        tk.Label(
            form_frame,
            text="Title:",
            bg="#422d05",
            font=("Arial", 12)
        ).grid(row=0, column=0, sticky="w")

        self.title_entry = tk.Entry(form_frame, width=30)
        self.title_entry.grid(row=0, column=1, pady=10)

        tk.Label(
            form_frame,
            text="Author:",
            bg="#422d05",
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="w")

        self.author_entry = tk.Entry(form_frame, width=30)
        self.author_entry.grid(row=1, column=1, pady=5)

        tk.Label(
            form_frame,
            text="Category:",
            bg="#422d05",
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="w")

        self.category_entry = tk.Entry(form_frame, width=30)
        self.category_entry.grid(row=2, column=1, pady=5)

        tk.Label(
            form_frame,
            text="Year:",
            bg="#422d05",
            font=("Arial", 12)
        ).grid(row=3, column=0, sticky="w")

        self.year_entry = tk.Entry(form_frame, width=30)
        self.year_entry.grid(row=3, column=1, pady=5)

        tk.Label(
            form_frame,
            text="Copies Available:",
            bg="#422d05",
            font=("Arial", 12)
        ).grid(row=4, column=0, sticky="w")

        self.copies_entry = tk.Entry(form_frame, width=30)
        self.copies_entry.grid(row=4, column=1, pady=5)

        btn_add = tk.Button(
            root,
            text="Add Book",
            font=("Arial", 12, "bold"),
            bg="#271903",
            fg="white",
            width=20,
            command=self.add_book
        )
        btn_add.pack(pady=10)

        self.books_listbox = tk.Listbox(
            root,
            width=50,
            height=12,
            font=("Arial", 11),
            bg="white",
            fg="#040a12"
        )
        self.books_listbox.pack(pady=10)

        status_frame = tk.Frame(root, bg="#422d05")
        status_frame.pack(pady=10)

        stats_frame = tk.Frame(root, bg="#422d05")
        stats_frame.pack(side="bottom", pady=10)

        self.total_books_label = tk.Label(
            root,
            text="Total books: 0",
            bg="#ecbb8d",
            font=("Arial", 11, "bold")
        )
        self.total_books_label.pack()

        self.total_copies_label = tk.Label(
            root,
            text="Total copies: 0",
            bg="#ecbb8d",
            font=("Arial", 11, "bold")
        )
        self.total_copies_label.pack()

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        category = self.category_entry.get().strip()
        year = self.year_entry.get().strip()
        copies = self.copies_entry.get().strip()

        if not title or not author or not category or not year or not copies:
            messagebox.showerror("Error", "All fields must be filled.")
            return

        if not year.isdigit():
            messagebox.showerror("Error", "Year must be avalid number.")
            return

        if not copies.isdigit() or int(copies) < 0:
            messagebox.showerror("Error", "Copies must be a positive number.")
            return

        book_info = f"{title} by {author} - {category} ({year}) - Copies: {copies}"

        self.books.append(book_info)
        self.books_listbox.insert(tk.END, book_info)

        self.total_books_label.config(
            text=f"Total books: {len(self.books)}"
        )

        self.total_copies += int(copies)

        self.total_copies_label.config(
            text=f"Total copies: {self.total_copies}"
        )

        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.copies_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MiniCRM(root)
    root.mainloop()