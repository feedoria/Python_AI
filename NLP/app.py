import nltk
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")
nltk.download("vader_lexicon")

from transformers import pipeline

analizor = pipeline(
"text-classification",
model="unitary/toxic-bert"
)

# text = "You are stupid"
text = input("Scrie comentariul: ")

rezultat = analizor(text)
print(rezultat)