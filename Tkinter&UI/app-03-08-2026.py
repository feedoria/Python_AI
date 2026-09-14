import tkinter as tk


def adauga_elev():
    elev = entry_elev.get()

    if elev == "":
        label_mesaj.config(
            text="Introdu numele elevului!",
            fg="red"
        )
    else:
        lista_elevi.insert(
            tk.END,
            elev
        )

        label_mesaj.config(
            text="Elev adaugat cu succes!",
            fg="green"
        )

        entry_elev.delete(
            0,
            tk.END
        )


fereastra = tk.Tk()

fereastra.title("Catalog Elevi")

fereastra.geometry("400x400")

fereastra.config(
    bg="#d6eaf8"
)


label_titlu = tk.Label(
    fereastra,
    text="Catalogul Clasei",
    font=("Arial", 18, "bold"),
    bg="#d6eaf8"
)

label_titlu.pack(
    pady=10
)


label_elev = tk.Label(
    fereastra,
    text="Nume elev:",
    bg="#d6eaf8"
)

label_elev.pack()


entry_elev = tk.Entry(
    fereastra,
    width=30
)

entry_elev.pack(
    pady=5
)


button = tk.Button(
    fereastra,
    text="Adauga elev",
    command=adauga_elev,
    bg="lightblue"
)

button.pack(
    pady=10
)


lista_elevi = tk.Listbox(
    fereastra,
    width=30,
    height=8
)

lista_elevi.pack()


label_mesaj = tk.Label(
    fereastra,
    text="",
    bg="#d6eaf8",
    font=("Arial", 10)
)

label_mesaj.pack(
    pady=10
)


fereastra.mainloop()