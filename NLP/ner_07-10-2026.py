#NLP --> Natural language Programming
#NLP --> Named Entity Recognition 

#Importam pipeline din Transformars 
#Pipeline ne ajuta sa folosim foarte usor un model de AI gata antrenat 
from transformers import pipeline

#Importam pandas
import pandas as pd 
#Importam Seaborn
import seaborn as sns 
#Importam ultima librarie matplotlib
import matplotlib.pyplot as plt 

#Exercitiul 1 
#Cream analiztoul NER --> Named Entity Recognition 
analizor = pipeline (
    #Spunem programului ca vrem sa facem NER 
    "ner",
    #Alegem modelul AI gata antrenat
    model = "dslim/bert-base-NER", #Pentru recunoastere tari, nume, obiecte, organizatii
    aggregation_strategy ="simple" #"Simple incearca sa uneasca bucatile aceluiasi nume"
)

#Exercitiul 2
#Analizam un text 
text = "Alina works at Microsoft in London and Silviu Works ata Google in Paris"

#Trimitem textul catre modelul AI
rezultate = analizor(text)
#Facem un print cu rezultatele complete
print("\nRezultate complete: ")
print(rezultate)

#Afisam rezultatul mai frumos
for rezultat in rezultate:
    #Luam cuvantul gasit de AI
    cuvant = rezultat["word"]

    #Luam categoria gasita de AI
    categorie = rezultat["entity_group"]

    #Afise scorul
    scor = rezultat["score"]

    #Afisam cuvantul gasit 
    print("\nCuvant:",cuvant)
    #Afisam si categoria
    print("Categorie:",categorie)
    print("Scor:",scor)

#ORG --> Organitaion
#LOC --> Location

#Exercitiul 3 
#Categorii principale 
#PER --> Person 
#ORG --> Organitaion
#LOC --> Location
#Misc --> inseeamna alte entitati 

#Facem o lista goala pentru numele gasite 
nume = []
categorii = []
scoruri = []

#PArcurgem fiecare rezultat gasit de AI 
for rezultat in rezultate:
    #Adaugam cuvantul gasit in lista nume 
    nume.append(rezultat["word"])
    categorii.append(rezultat["entity_group"])
    scoruri.append(rezultat["score"])

#Facem un tabel cu pandas 
date = {
    "Entintate":nume,
    "Categorie":categorii,
    "Scor":scoruri
}
tabel = pd.DataFrame(date)
print("\nTabelul Nostru")
print(tabel)

#Facem un grafic cu seaborn 

sns.countplot(
    #Alegem tabelyl
    data=tabel,
    #PE axa x Punem categoria 
    x="Categorie"
)
plt.title("Entitate gasita de AI")
plt.xlabel("Tipul Entitatii")
plt.ylabel("Numar")
plt.tight_layout()
plt.show()

#Exercitiu cu adaugare de la tastatura 

text_utilizator = input("\nSCrie un text in engleza:")
#Trimitem textul utilizatorului catre AI 
rezultate_utilizator = analizor(text_utilizator)

#Afisam un titlu
print("\nAi-ul a gasit:")

#Parcurgem rezultatele gasite 
for rezultat in rezultate_utilizator:
    cuvant = rezultat["word"]
    categorie = rezultat["entity_group"]
    scor = rezultat["score"]

    print("\nEntitate:",cuvant)
    print("Categorie:",categorie)
    print("Scor:",scor)