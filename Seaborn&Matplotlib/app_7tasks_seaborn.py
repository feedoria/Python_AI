import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 1. Fitness - Puls si timp de antrenament

date = {
    "Minute": [10, 20, 30, 40, 50, 60],
    "Puls": [95, 110, 125, 138, 145, 152]
}

df = pd.DataFrame(date)

sns.scatterplot(
    data=df,
    x="Minute",
    y="Puls"
)

plt.title("Puls in timpul antrenamentului")
plt.xlabel("Minute")
plt.ylabel("Puls")

plt.show()


# 2. Magazin online - Comenzi pe categorii

# date = {
#     "Categorie": ["Laptop", "Telefon", "Monitor", "Tastatura", "Mouse"],
#     "Comenzi": [35, 62, 28, 44, 57]
# }

# df = pd.DataFrame(date)

# sns.barplot(
#     data=df,
#     x="Categorie",
#     y="Comenzi"
# )

# plt.title("Comenzi magazin online")
# plt.xlabel("Categorie")
# plt.ylabel("Comenzi")

# plt.show()


# 3. Transport - Viteza a doua trenuri

# date = {
#     "Ora": [8, 10, 12, 14, 8, 10, 12, 14],
#     "Viteza": [80, 100, 120, 110, 70, 95, 115, 125],
#     "Tren": ["A", "A", "A", "A", "B", "B", "B", "B"]
# }

# df = pd.DataFrame(date)

# sns.lineplot(
#     data=df,
#     x="Ora",
#     y="Viteza",
#     hue="Tren"
# )

# plt.title("Viteza trenurilor")
# plt.xlabel("Ora")
# plt.ylabel("Viteza")

# plt.show()


# 4. Cinema - Distributia duratei filmelor

# date = {
#     "Durata": [82, 90, 95, 100, 105, 110, 110, 115, 120, 125, 130, 145, 160]
# }

# df = pd.DataFrame(date)

# sns.histplot(
#     data=df,
#     x="Durata",
#     bins=5
# )

# plt.title("Durata filmelor")
# plt.xlabel("Minute")
# plt.ylabel("Numar de filme")

# plt.show()


# 5. Curierat - Timp de livrare

# date = {
#     "TimpLivrare": [18, 20, 22, 22, 24, 25, 27, 29, 31, 60]
# }

# df = pd.DataFrame(date)

# sns.boxplot(
#     data=df,
#     y="TimpLivrare"
# )

# plt.title("Timpul de livrare")
# plt.ylabel("Timp livrare")

# plt.show()


# 6. Muzica - Rating pe doua genuri

# date = {
#     "Gen": ["Rock", "Rock", "Rock", "Rock", "Rock",
#             "Pop", "Pop", "Pop", "Pop", "Pop"],
#     "Rating": [6, 7, 8, 8, 9, 5, 6, 7, 9, 10]
# }

# df = pd.DataFrame(date)

# sns.violinplot(
#     data=df,
#     x="Gen",
#     y="Rating"
# )

# plt.title("Distributia ratingurilor")
# plt.xlabel("Gen")
# plt.ylabel("Rating")

# plt.show()


# 7. Scoala - Notele a doua clase

# date = {
#     "Clasa": ["A", "A", "A", "A", "A", "A",
#               "B", "B", "B", "B", "B", "B"],
#     "Nota": [5, 6, 7, 8, 8, 10, 4, 6, 6, 7, 9, 10]
# }

# df = pd.DataFrame(date)

# sns.violinplot(
#     data=df,
#     x="Clasa",
#     y="Nota"
# )

# sns.swarmplot(
#     data=df,
#     x="Clasa",
#     y="Nota"
# )

# plt.title("Notele claselor")
# plt.xlabel("Clasa")
# plt.ylabel("Nota")

# plt.show()