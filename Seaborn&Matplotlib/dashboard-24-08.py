import matplotlib.pyplot as plt

# zile = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata', 'Duminica']
# vanzari = [100, 150, 200, 250, 300, 350, 400]

# plt.plot(zile, vanzari)
# plt.xlabel('Zile')
# plt.ylabel('Vanzari')
# plt.title('Vanzari per zi')
# plt.show()

# studenti = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
# note = [8, 9, 7, 10, 6, 5, 9, 8, 7, 10]

# plt.title('Note per student')
# plt.plot(studenti, note, marker='o', color='pink', linestyle='--')
# plt.xlabel('Studenti')
# plt.ylabel('Note')
# plt.title('Note per student')
# plt.show()

# -- Task
# Task 1 — Aeroport ✈️

# Creează un line chart care să arate numărul de pasageri dintr-un aeroport
#  în fiecare lună a anului. Compară două aeroporturi pe același grafic. 
# Folosește marker, label, legend, titlu și grid.

# luni = ['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']
# aeroport1 = [1000, 1200, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000]
# aeroport2 = [800, 1000, 1300, 1800, 2300, 2800, 3300, 3800, 4300, 4800, 5300, 5800]

# plt.title('Numar pasageri per luna')
# plt.plot(luni, aeroport1, color='blue', marker='o', label='Aeroport 1')
# plt.plot(luni, aeroport2, color='red', marker='s', label='Aeroport 2')
# plt.xlabel('Luni')
# plt.ylabel('Numar pasageri')
# plt.legend()
# plt.grid(True)
# plt.show()

# Task 2 — Formula 1 🏎️

# Creează un bar chart care să arate punctele obținute de 10 piloți de Formula 1 
# într-un sezon. Folosește culori diferite pentru bare și adaugă titlu, xlabel 
# și ylabel.

# piloti = ['Verstappen', 'Leclerc', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8']
# puncte = [25, 20, 15, 12, 10, 8, 6, 4, 2, 1]
# culori = ['gold','silver','brown','red','blue','green','orange','purple','pink','yellow']

# plt.title('Puncte per pilot')
# plt.bar(piloti, puncte, color=culori)
# plt.xlabel('Piloti')
# plt.ylabel('Puncte')
# plt.show()

# Task 3 — Spital 🏥

# Creează un scatter plot care să arate relația dintre numărul de ore de somn 
# și pulsul măsurat pentru 12 persoane. Folosește s pentru dimensiunea punctelor 
# și adaugă titlu și etichete pentru axe.

# ore_somn = [6, 7, 8, 5, 9, 7, 6, 8, 7, 5, 6, 8]
# puls = [70, 65, 60, 75, 55, 65, 70, 60, 65, 75, 70, 60]

# plt.title('Relatie ore somn si puls')
# plt.scatter(ore_somn, puls, s=100, color='blue')
# plt.xlabel('Ore somn')
# plt.ylabel('Puls')
# plt.show()

# Task 4 — Călătorie 🌍

# Creează un pie chart care să arate cât timp ai petrecut într-o călătorie în 6 
# activități diferite: plajă, vizitare obiective, restaurante, transport, shopping 
# și excursii. Afișează procentele cu autopct.

activitati = ['plaja', 'vizitare obiective', 'restaurante', 'transport', 'shopping', 'excursii']
procente = [20, 25, 15, 10, 15, 15]

plt.title('Timp petrecut în călătorie')
plt.pie(procente, labels=activitati, autopct='%1.1f%%')
plt.show()

# Task 5 — Agricultură 🌾

# Creează un histogram care să arate distribuția cantității de recoltă obținute
#  de la mai multe parcele agricole. Folosește cel puțin 8 valori diferite și bins.
#  Adaugă titlu, xlabel și ylabel.

recolta = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
plt.hist(recolta, bins=5, color='green', edgecolor='black')
plt.title('Distributia cantitatii de recolta')
plt.xlabel('Cantitate')
plt.ylabel('Frecventa')
plt.show()
