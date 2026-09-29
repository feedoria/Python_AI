# """
# Date de intrare
# x = np.array([[10],[20],[30],[40],[50],[60]])
# y = np.array([1,1,1,0,0,0])
# Semnificație
# • x = prețul produsului
# • y = 1 dacă produsul este cumpărat
# • y = 0 dacă produsul nu este cumpărat
# Cerințe
# • creează un model keras.Sequential
# • folosește keras.Input(shape=(1,))
# • primul strat să aibă Dense(4, activation="relu")
# • ultimul strat să aibă Dense(1, activation="sigmoid")
# • compilează cu optimizer="adam", loss="binary_crossentropy",
# metrics=["accuracy"]
# • antrenează modelul cu epochs=100, verbose=0
# • fă o predicție pentru un produs care costă 25
# • afișează rezultatul în terminal
# """

# # import numpy as np
# # import keras
# # from keras import layers

# # x = np.array([[10],[20],[30],[40],[50],[60]])
# # y = np.array([1,1,1,0,0,0])

# # model = keras.Sequential([
# #     keras.Input(shape=(1,)),
# #     layers.Dense(4, activation="relu"),
# #     layers.Dense(1, activation="sigmoid")
# # ])

# # model.compile(optimizer="adam",
# #               loss="binary_crossentropy",
# #               metrics=["accuracy"])

# # model.fit(x, y, epochs=100, verbose=0)
# # rezultat = model.predict(np.array([[25]]), verbose=0)
# # print(rezultat[0][0])

# """
# Date de intrare
# x = np.array([[10],[20],[30],[40],[50],[60]])
# y = np.array([2,3,4,5,6,7])
# Semnificație
# • x = distanța parcursă
# • y = combustibil consumat
# Cerințe
# • creează un model keras.Sequential
# • folosește keras.Input(shape=(1,)), layers.Dense(4, activation="relu"),
# layers.Dense(1)
# • compilează cu optimizer="adam", loss="mse"
# • antrenează modelul cu epochs=200, verbose=0
# • fă o predicție pentru 70 km parcurși
# • afișează consumul estimat
# • creează un sns.barplot(): pe X distanța, pe Y consumul (folosește x.flatten())
# • titlul graficului: Consum in functie de distanta
# """

# # import numpy as np
# # import keras
# # from keras import layers
# # import seaborn as sns
# # import matplotlib.pyplot as plt

# # x = np.array([[10], [20], [30], [40], [50], [60]])
# # y = np.array([2, 3, 4, 5, 6, 7])

# # model = keras.Sequential([
# #     keras.Input(shape=(1,)),
# #     layers.Dense(4, activation="relu"),
# #     layers.Dense(1)
# # ])

# # model.compile(
# #     optimizer="adam",
# #     loss="mse"
# # )

# # model.fit(x, y, epochs=200, verbose=0)

# # rezultat = model.predict(np.array([[70]]), verbose=0)

# # print("Consum estimat:", rezultat[0][0])

# # sns.barplot(
# #     x=x.flatten(),
# #     y=y
# # )

# # plt.title("Consum in functie de distanta")
# # plt.xlabel("Distanta")
# # plt.ylabel("Consum")
# # plt.show()

# """
# Exercițiul 3
# Restaurant – Număr de clienți și încasări
# Date de intrare
# x = np.array([[10],[20],[30],[40],[50],[60]])
# y = np.array([200,400,650,850,1100,1300])
# Semnificație
# • x = numărul de clienți
# • y = încasările restaurantului
# Cerințe
# • creează modelul exact pe structura: keras.Input(shape=(1,)), layers.Dense(4,
# activation="relu"), layers.Dense(1)
# • compilează cu optimizer="adam", loss="mse"
# • antrenează modelul cu epochs=200
# • fă o predicție pentru 70 clienți
# • afișează: Incasare estimata:
# • creează un barplot: X = numărul de clienți, Y = încasările
# • titlul graficului: Incasari restaurant
# """

# import numpy as np
# import keras
# from keras import layers
# import seaborn as sns
# import matplotlib.pyplot as plt

# x = np.array([[10], [20], [30], [40], [50], [60]])
# y = np.array([200, 400, 650, 850, 1100, 1300])

# model = keras.Sequential([
#     keras.Input(shape=(1,)),
#     layers.Dense(4, activation="relu"),
#     layers.Dense(1)
# ])

# model.compile(
#     optimizer="adam",
#     loss="mse"
# )

# model.fit(x, y, epochs=200, verbose=0)

# rezultat = model.predict(np.array([[70]]), verbose=0)

# print("Incasare estimata:", rezultat[0][0])

# sns.barplot(
#     x=x.flatten(),
#     y=y
# )

# plt.title("Incasari restaurant")
# plt.xlabel("Numar de clienti")
# plt.ylabel("Incasari")
# plt.show()

# """
# Exercițiul 4
# Gaming – Ore jucate și scor
# Date de intrare
# x = np.array([[1],[2],[3],[4],[5],[6]])
# y = np.array([100,180,250,340,430,520])
# Semnificație
# • x = ore jucate
# • y = scor obținut
# Cerințe
# • creează un model Keras; intrarea să primească o singură valoare
# • folosește 4 neuroni cu relu
# • ultimul strat să aibă un singur neuron
# • compilează cu optimizer="adam", loss="mse"
# • antrenează cu epochs=200
# • fă o predicție pentru 7 ore jucate
# • afișează scorul estimat
# • creează un sns.barplot(): X = ore jucate, Y = scor
# • titlul graficului: Scor in functie de orele jucate
# Exerciții Keras – Rețele neuronale simple Pagina 3


# Exercițiul 5
# Fitness – Slăbește sau nu slăbește
# Date de intrare
# x = np.array([[1],[2],[3],[4],[5],[6]])
# y = np.array([0,0,0,1,1,1])
# Semnificație
# • x = numărul de antrenamente pe săptămână
# • y = 0 nu slăbește
# • y = 1 slăbește
# Cerințe
# • creează un model keras.Sequential
# • folosește keras.Input(shape=(1,)), layers.Dense(4, activation="relu"),
# layers.Dense(1, activation="sigmoid")
# • compilează cu optimizer="adam", loss="binary_crossentropy",
# metrics=["accuracy"]
# • folosește epochs=100, verbose=0
# • fă o predicție pentru o persoană care face 5 antrenamente pe săptămână
# • afișează rezultatul
# Exerciții Keras – Rețele neuronale simple 
# """
