import nltk #Libraria pentru nlp care ne ajuta sa lucram cu texte
nltk.download("punkt") #pachetul necesar pentru impartirea textului in cuvinte
nltk.download("punkt_tab") #E pachet pentru tokenizare
nltk.download("stopwords") #Descarca o lista de cuvinte comune this, and , is , the
nltk.download("vader_lexicon") #Asta e pentru sentimente
 
#Importam functia care sparge o propozitie in cuvinte
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
 
#Exercitiul 1 impartim textul in cuvinte
# text = "ne place extraordinar de tare cursul de python"
# cuvinte = word_tokenize(text)
# print(cuvinte)
#Exercitiul 2 --> Numaram cuvintele
text = "Python is very easy"
cuvinte = word_tokenize(text)
numar = len(cuvinte)
print("Numar de cuvinte: ", numar)
 
#Exercitiul 3
#impart textul in propozitiie
text = "Astazi Bogdan s-a trezit la ora 5. Dupa a alergat putin. Am terminat proiectul de 8000 de euro. Face foamea pe aici"
propozitii = sent_tokenize(text)
 
print(propozitii)
#Parcurgem fiecare propozitie
for propozitie in propozitii:
    print(propozitie,"\n")
 
 
#Exercitiul 4 -- Eliminam cuvintele jignitoare
 
text = "sa-i porti tu cu tactu pentru ca nu imi sunt buni, milogule, milogule"
cuvinte=word_tokenize(text)
#Lista noastra de cuvinte jignitoare
cuvinte_vulgare = ["tactu", "milogule"]
#Cream o lista goala
cuvinte_importante = []
#Luam fiecare cuvant
for cuvant in cuvinte:
    #Verificam daca cuvantul nu este in lista de cuvinte vulgare
    if cuvant.lower() not in cuvinte_vulgare:
        cuvinte_importante.append(cuvant)
print("Text original: ", cuvinte)
print("Important: ", cuvinte_importante)
 
from transformers import pipeline
analizor = pipeline("text-classification",model="unitary/toxic-bert")
text= "suck my dick nigga"
rezultat = analizor(text)
print(rezultat)