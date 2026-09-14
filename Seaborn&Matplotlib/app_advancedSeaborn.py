import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 1. Magazin online - Pret, vanzari si reclame

# date = {
#     "Pret": [50, 70, 90, 110, 130, 150, 170, 190],
#     "Vanzari": [120, 110, 100, 85, 70, 60, 45, 30],
#     "Reclame": [2, 3, 4, 5, 6, 7, 8, 9]
# }

# df = pd.DataFrame(date)

# corelatie = df.corr()

# print(corelatie)

# sns.heatmap(
#     corelatie,
#     annot=True
# )

# plt.title("Corelatia magazinului online")

# plt.show()


# 2. Masini - Putere, viteza si consum

# date = {
#     "CaiPutere": [90, 120, 150, 180, 220, 300, 400],
#     "VitezaMaxima": [170, 190, 210, 225, 240, 270, 300],
#     "Consum": [5, 6, 7, 8, 10, 13, 17]
# }

# df = pd.DataFrame(date)

# sns.pairplot(
#     data=df
# )

# plt.show()


# 3. Joc video - Jucatori casual si profesionisti

# date = {
#     "OreJucate": [20, 30, 40, 50, 100, 130, 160, 200],
#     "Victorii": [2, 4, 6, 8, 20, 28, 35, 45],
#     "Scor": [500, 700, 900, 1100, 2500, 3200, 4000, 5000],
#     "Tip": [
#         "Casual",
#         "Casual",
#         "Casual",
#         "Casual",
#         "Pro",
#         "Pro",
#         "Pro",
#         "Pro"
#     ]
# }

# df = pd.DataFrame(date)

# sns.pairplot(
#     data=df,
#     hue="Tip"
# )

# plt.show()


# 4. Livrari - Distanta si timp

# date = {
#     "Distanta": [2, 5, 8, 10, 15, 20, 25, 30],
#     "Timp": [10, 15, 20, 25, 35, 42, 50, 60]
# }

# df = pd.DataFrame(date)

# sns.regplot(
#     data=df,
#     x="Distanta",
#     y="Timp"
# )

# plt.title("Distanta si timpul de livrare")
# plt.xlabel("Distanta km")
# plt.ylabel("Timp minute")

# # Linia urca, deci cu cat distanta este mai mare,
# # cu atat timpul de livrare creste.

# plt.show()


# 5. Turism - Pretul hotelului in functie de distanta fata de centru

date = {
    "DistantaCentru": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "PretNoapte": [180, 165, 150, 145, 130, 120, 110, 100, 90, 80]
}

df = pd.DataFrame(date)

sns.regplot(
    data=df,
    x="DistantaCentru",
    y="PretNoapte"
)

plt.title("Distanta fata de centru si pretul hotelului")
plt.xlabel("Distanta fata de centru km")
plt.ylabel("Pret pe noapte")

# Pretul hotelului scade atunci cand
# distanta fata de centru creste.

plt.show()