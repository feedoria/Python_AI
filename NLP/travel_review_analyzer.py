import tkinter as tk
#Importam caseta mare de text si ferestrele de avertizare
from tkinter import scrolledtext, messagebox

from transformers import pipeline


#Incarcam modelele o singura data, la pornirea programului
clasificator = pipeline(
    #I spunem ca vrem sa clasificam textul fara antrenare speciala
    "zero-shot-classification",

    #Alegem modelul preantrenat
    model="facebook/bart-large-mnli"
)

rezumator = pipeline(
    #I spunem ca vrem sa facem un rezumat al textului
    "summarization",

    #Alegem modelul preantrenat
    model="sshleifer/distilbart-cnn-12-6"
)

#Categoriile pe care le poate alege AI-ul
categorii = ["hotel", "food", "transport", "nightlife", "safety", "attractions", "customer service"]

#Etichetele pentru experienta turistului
experiente = ["positive experience", "negative experience", "mixed experience"]


#Facem o functie pentru analiza recenziei

def analizeaza():
    #Citim textul din caseta mare
    text = text_box.get("1.0", tk.END).strip()

    #Verificam daca utilizatorul a scris ceva sau nu
    if text == "":
        #Afisam un avertisment si ne oprim
        messagebox.showwarning("Atentie", "Scrie o recenzie mai intai!")
        return

    #Trimitem textul catre clasificator cu cele 7 categorii
    rezultat = clasificator(text, categorii)

    #Luam categoria cu cel mai mare scor
    subiect = rezultat["labels"][0]

    #Luam scorul categoriei
    scor = rezultat["scores"][0]

    #Afisam subiectul si scorul
    categorie_label.config(text="Subiect principal: " + subiect.capitalize())
    scor_label.config(text=f"Scor AI: {scor * 100:.1f}%")

    #Bonus - a doua clasificare pentru experienta turistului
    rezultat2 = clasificator(text, experiente)

    #Luam experienta cu cel mai mare scor
    experienta = rezultat2["labels"][0]

    #Alegem culoarea in functie de experienta
    if experienta == "positive experience":
        culoare = "green"
    elif experienta == "negative experience":
        culoare = "red"
    else:
        culoare = "orange"

    #Afisam experienta colorata
    experienta_label.config(
        text="Experienta turistului: " + experienta.capitalize(),
        fg=culoare
    )

    #Verificam daca textul este prea scurt pentru rezumat
    if len(text.split()) < 30:
        rezumat_label.config(text="Rezumat AI:\nText prea scurt pentru rezumare")
    else:
        #Trimitem textul catre rezumator
        rezultat3 = rezumator(text, max_length=60, min_length=20)

        #Luam rezumatul generat de AI
        rezumat = rezultat3[0]["summary_text"]

        #Afisam rezumatul
        rezumat_label.config(text="Rezumat AI:\n" + rezumat)


#Facem o functie pentru butonul Sterge

def sterge():
    #Golim caseta de recenzie
    text_box.delete("1.0", tk.END)

    #Golim toate rezultatele
    categorie_label.config(text="")
    scor_label.config(text="")
    experienta_label.config(text="")
    rezumat_label.config(text="")

    #Punem cursorul inapoi in caseta de text
    text_box.focus()


fereastra = tk.Tk()

fereastra.title("AI Travel Analyzer")

fereastra.geometry("520x620")

#Facem titlu

titlu = tk.Label(
    fereastra,
    text="AI TRAVEL ANALYZER",
    font=("Arial", 22, "bold")
)

titlu.pack(pady=10)

#Facem caseta mare unde scriem recenzia
text_box = scrolledtext.ScrolledText(
    fereastra,
    height=8,
    width=55,
    font=("Arial", 11)
)

text_box.pack(pady=10)

#Facem butonul pentru analiza
buton_analiza = tk.Button(
    fereastra,
    text="Analizeaza Review",
    command=analizeaza,
    font=("Arial", 13)
)

buton_analiza.pack(pady=5)

#Facem zona unde apar rezultatele

categorie_label = tk.Label(fereastra, text="", font=("Arial", 13))
categorie_label.pack(pady=3)

scor_label = tk.Label(fereastra, text="", font=("Arial", 13))
scor_label.pack(pady=3)

experienta_label = tk.Label(fereastra, text="", font=("Arial", 13, "bold"))
experienta_label.pack(pady=3)

rezumat_label = tk.Label(
    fereastra,
    text="",
    font=("Arial", 12),
    wraplength=480,
    justify="left"
)

rezumat_label.pack(pady=10)

#Facem butonul pentru stergere
buton_sterge = tk.Button(
    fereastra,
    text="Sterge",
    command=sterge,
    font=("Arial", 13)
)

buton_sterge.pack(pady=5)

#Punem cursorul direct in caseta de text
text_box.focus()

fereastra.mainloop()