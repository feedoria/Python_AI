import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("vader_lexicon")

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

#Task 1
# text = "Astazi avem pizza, paste, burger si salata"
# cuvinte = word_tokenize(text)
# print(cuvinte)
# print(f"Numar de cuvinte: {len(cuvinte)}")

#Task 2
# text = "Andrei s-a trezit dimineata. A mers la scoala. A avut ora de Python. Seara s-a jucat pe calculator."
# propozitii = sent_tokenize(text)
# print(f"Numar de propozitii: {len(propozitii)} \n")
# for propozitie in propozitii:
#     print(propozitie, "\n")


#Task 3
# text = input("Scrie mesajul tau: ")
# cuvinte = word_tokenize(text)
# print(f"Numar de cuvinte: {len(cuvinte)}")
# print(cuvinte)

#Task 4
# text = "Esti foarte enervant lenesule si obraznicule"
# cuvinte_interzise = ["lenesule", "obraznicule"]
# cuvinte = word_tokenize(text)
# cuvinte_acceptate = []
# for cuvant in cuvinte:
#     if cuvant.lower() not in cuvinte_interzise:
#         cuvinte_acceptate.append(cuvant)
# print("Text original: ", cuvinte)
# print("Text acceptat: ", cuvinte_acceptate)

#Task 5
# text = "Jocul este foarte bun dar developerul este prostule"
# cuvinte_vulgare = ["prostule", "idiotule", "fraiere"]
# cuvinte = word_tokenize(text)
# cuvinte_acceptate = []
# eliminate = 0
# for cuvant in cuvinte:
#     if cuvant.lower() not in cuvinte_vulgare:
#         cuvinte_acceptate.append(cuvant)
#     else:
#         eliminate += 1
# print("Text acceptat: ", cuvinte_acceptate)
# print("Numar de cuvinte eliminate: ", eliminate)

#Task 6
from transformers import pipeline

# analizor = pipeline(
# "text-classification",
# model="unitary/toxic-bert"
# )

# text = "You are stupid"

# print(analizor(text))

#Task 7
text = input("Scrie comentariul: ")
analizor = pipeline(
"text-classification",
model="unitary/toxic-bert"
)
rezultat = analizor(text)
print(rezultat)