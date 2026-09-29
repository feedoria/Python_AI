# import pandas as pd 
# import seaborn as sns
# import matplotlib.pyplot as plt 

# date = {
#     "varsta": [20,22,24,26,28,30],
#     "salariu": [300,3500,4200,5000,5800,7000]
# }

# df = pd.DataFrame(date)

# sns.scatterplot(
#     data=df,
#     x="varsta",
#     y="salariu"
# )
# plt.title("Varsta si salariu")
# plt.xlabel("Varsta")
# plt.ylabel("Salariu")
# plt.show()

# import pandas as pd 
# import seaborn as sns 
# import matplotlib.pyplot as plt 

# date = {
#     "Luna":[1,2,3,4,5,6],
#     "Vanzari":[230,190,400,170,210,250]
# }

# df = pd.DataFrame(date)

# sns.barplot(
#     data=df, 
#     x="Luna",
#     y="Vanzari"
# )

# plt.title("Vanzari pe luni")
# plt.xlabel("Luna")
# plt.ylabel("Vanzari")
# plt.show()

# import pandas as pd 
# import seaborn as sns 
# import matplotlib.pyplot as plt 

# date = {
#     "Ore":[2,3,4,5,6,7],
#     "Scor":[20,30,40,55,70,85],
#     "Nivel":[
#         "Incepator",
#         "Incepator",
#         "Incepator",
#         "Avansat",
#         "Avansat",
#         "Avansat"
#     ]
# }

# df = pd.DataFrame(date)

# sns.lineplot(
#     data=df,
#     x="Ore",
#     y="Scor",
#     hue="Nivel"
# )
# plt.title("Ore si scor")
# plt.xlabel("Ore jucate")
# plt.ylabel("Scor")
# plt.show()


# import pandas as pd 
# import seaborn as sns 
# import matplotlib.pyplot as plt 

# date = {
#     "Orase": [
#         "Roma", "Roma",
#         "Madrid","Madrid",
#         "Damasc","Damasc"
#     ],
#     "Cost":[
#         100,50,
#         120,60,
#         70,30
#     ],
#     "Categorie":[
#         "Mancare","Transport",
#         "Mancare","Transport",
#         "Mancare","Transport"
#     ]
# }

# df = pd.DataFrame(date)

# sns.barplot(
#     data=df,
#     x="Orase",
#     y="Cost",
#     hue="Categorie"
# )
# plt.title("Cheltuielile pe orase")
# plt.xlabel("Oras")
# plt.ylabel("Cost")
# plt.show()

# import pandas as pd
# import seaborn as sns 
# import matplotlib.pyplot as plt 

# date={
#     "Note":[5,6,6,4,4,4,8,8,9,9,10]
# }
# df = pd.DataFrame(date)

# sns.histplot(
#     data=df,
#     x="Note",
#     bins=5
# )
# plt.title("Notele elevilor")
# plt.xlabel("Nota")
# plt.ylabel("Numar studenti")

# plt.show()

#-----------

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# date = {
#     "Distanta": [300, 500, 700, 900, 1100, 1300],
#     "Combustibil": [120, 180, 240, 310, 370, 450]
# }

# df = pd.DataFrame(date)

# sns.scatterplot(
#     data=df,
#     x="Distanta",
#     y="Combustibil"
# )

# plt.title("Distanta si consumul avionului")
# plt.xlabel("Distanta km")
# plt.ylabel("Combustibil litri")

# plt.show()

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# date = {
#     "Zi": ["Luni", "Marti", "Miercuri", "Joi", "Vineri"],
#     "Comenzi": [45, 60, 38, 75, 95]
# }

# df = pd.DataFrame(date)

# sns.barplot(
#     data=df,
#     x="Zi",
#     y="Comenzi"
# )

# plt.title("Comenzi restaurant")
# plt.xlabel("Ziua")
# plt.ylabel("Numar comenzi")

# plt.show()

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# date = {
#     "Ora": [8, 12, 16, 20, 8, 12, 16, 20],
#     "Temperatura": [18, 24, 28, 22, 14, 19, 23, 17],
#     "Oras": [
#         "Bucuresti", "Bucuresti", "Bucuresti", "Bucuresti",
#         "Brasov", "Brasov", "Brasov", "Brasov"
#     ]
# }

# df = pd.DataFrame(date)

# sns.lineplot(
#     data=df,
#     x="Ora",
#     y="Temperatura",
#     hue="Oras"
# )

# plt.title("Temperatura pe parcursul zilei")
# plt.xlabel("Ora")
# plt.ylabel("Temperatura")

# plt.show()

# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt

# date = {
#     "Timp": [
#         20, 22, 25, 25, 28,
#         30, 30, 31, 35, 36,
#         40, 42, 45, 50, 65
#     ]
# }

# plt.title("Distribuirea timpilor de livrare")
# plt.xlabel("Minute")
# plt.ylabel("Numar livrari")

# plt.show()
# df = pd.DataFrame(date)

# sns.histplot(
#     data=df,
#     x="Timp",
#     bins=6
# )

