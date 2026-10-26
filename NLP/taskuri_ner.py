from transformers import pipeline
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

analizor = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)


# Task 1 - Persoane si companii

text = "Emma works at Microsoft, David works at Google and Sarah works at Amazon."

rezultate = analizor(text)

for rezultat in rezultate:
    cuvant = rezultat["word"]
    categorie = rezultat["entity_group"]
    scor = rezultat["score"]

    print("\nEntitate:", cuvant)
    print("Categorie:", categorie)
    print("Scor:", scor)


# Task 2 - Stire despre tehnologie

text = "James works at Apple and Michael works at Microsoft."

rezultate = analizor(text)

entitati = []
categorii = []
scoruri = []

for rezultat in rezultate:
    entitati.append(rezultat["word"])
    categorii.append(rezultat["entity_group"])
    scoruri.append(rezultat["score"])

date = {
    "Entitate": entitati,
    "Categorie": categorii,
    "Scor": scoruri
}

tabel = pd.DataFrame(date)

print("\nTabel:")
print(tabel)


# Task 3 - Comentariu introdus de utilizator

text_utilizator = input("\nScrie un text in engleza: ")

rezultate_utilizator = analizor(text_utilizator)

entitati = []
categorii = []
scoruri = []

for rezultat in rezultate_utilizator:
    entitati.append(rezultat["word"])
    categorii.append(rezultat["entity_group"])
    scoruri.append(rezultat["score"])

date = {
    "Entitate": entitati,
    "Categorie": categorii,
    "Scor": scoruri
}

tabel = pd.DataFrame(date)

print("\nTabel:")
print(tabel)

sns.countplot(
    data=tabel,
    x="Categorie"
)

plt.title("Entitati gasite de AI")
plt.xlabel("Categorie")
plt.ylabel("Numar")
plt.tight_layout()
plt.show()