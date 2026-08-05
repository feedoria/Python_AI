import tkinter as tk


def afiseaza_profil():
    nume = entry_nume.get()
    varsta = entry_varsta.get()

    if nume == "" or varsta == "":
        label_rezultat.config(
            text="Te rog completeaza toate campurile!"
        )
    else:
        label_rezultat.config(
            text=f"Salut, {nume}! Ai {varsta} de ani."
        )


def sterge_datele():
    entry_nume.delete(0, tk.END)
    entry_varsta.delete(0, tk.END)
    label_rezultat.config(
        text=""
    )


def inchide_aplicatia():
    fereastra.destroy()


fereastra = tk.Tk()

fereastra.title("Profil Utilizator")

fereastra.geometry("500x350")


label_titlu = tk.Label(
    fereastra,
    text="Fisa utilizatorului",
    font=("Arial", 18)
)

label_titlu.pack(pady=10)


label_nume = tk.Label(
    fereastra,
    text="Nume:"
)
label_nume.pack()


entry_nume = tk.Entry(
    fereastra,
    width=30
)
entry_nume.pack(pady=5)


label_varsta = tk.Label(
    fereastra,
    text="Varsta:"
)
label_varsta.pack()


entry_varsta = tk.Entry(
    fereastra,
    width=30
)
entry_varsta.pack(pady=5)


button_afiseaza = tk.Button(
    fereastra,
    text="Afiseaza",
    command=afiseaza_profil
)
button_afiseaza.pack(pady=5)


button_sterge = tk.Button(
    fereastra,
    text="Sterge",
    command=sterge_datele
)
button_sterge.pack(pady=5)


button_inchide = tk.Button(
    fereastra,
    text="Inchide aplicatia",
    command=inchide_aplicatia
)
button_inchide.pack(pady=5)


label_rezultat = tk.Label(
    fereastra,
    text="",
    font=("Arial", 12)
)
label_rezultat.pack(pady=10)


fereastra.mainloop()