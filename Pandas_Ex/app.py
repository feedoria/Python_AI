import pandas as pd 

nume_elevi = pd.Series(["Ana","Bogdan","Sara"])
print("O serie cu nume:")
print(nume_elevi)
print("================================================")
elevi = pd.DataFrame({
    "Nume":["Ana","Bogdan","Sara","Paul"],
    "Varsta":[19,20,18,21],
    "Orase":["Bucuresti","Cluj","Targu Jiu","Craiova"],
    "Nota":[9.8,7.0,10.0,8.0]
})
print(elevi)
print("================================================")
print(elevi.head(2))
print("================================================")
print(elevi.tail(1))
print("================================================")
print(elevi.columns)
print("================================================")
print(elevi.shape)
print("================================================")
print(elevi.dtypes)
print("=====================================================================================")




vanzari = pd.DataFrame({
    "Produs":["Laptop","Mouse","Aparat Foto","Casti","Laptop","Telefon","Imprimanta"],
    "Categorie":[
        "Calculatoare",
        "Accesorii",
        "Dispozitive de fotografiat",
        "Accesorii",
        "Calculatoare",
        "Electronice",
        "Electronice"
    ],
    "Pret":[3200.00,80.0,1000.0,51.8,7000.8,400.8,299.9],
    "Bucati":[5,3,6,4,5,9,2]
})


print(vanzari.info())
print(vanzari.describe())
print(vanzari.count())

print("================================================")

angajati = pd.DataFrame({
    "Nume":["Daria","Alex","Ioana","Radu","Mara","Bogdan"],
    "Departament":["HR","Polaris Dat cu lopata","IT","Paza","in piata sectiunea gutui","IT"],
    "Salariu":[4200,1800,3500,1900,900,8000],
    "Oras":["Iasi","Targu Jiu","Bucuresti","Cluj","Balesti","Craiova"]
})

print(angajati)

print(angajati["Salariu"])
print(angajati[["Nume","Salariu"]])
salarii_mari = angajati[angajati["Salariu"] > 2000]
print(salarii_mari)
print("================================================")
angajati_it = angajati[angajati["Departament"] == "IT"]
print(angajati_it)

it_cu_salariu_mare = angajati[
    (angajati["Departament"] == "IT") &
    (angajati["Salariu"] >= 3400)
]

print(it_cu_salariu_mare)


print("================================================")


comenzi = pd.DataFrame({
    "Client":["Ana","Bogdan","Carmen","Ana","Dan"],
    "Produs":["Carte","Caiet","Pix","Carte","Ghiozdan"],
    "Pret":[45.0,12.0,None,45.0,120.0],
    "Cantitate":[2,5,10,2,1]
})

print(comenzi)

print(comenzi.isna())

print(comenzi.isna().sum())

comenzi_fara_duplicate = comenzi.drop_duplicates()
print(comenzi_fara_duplicate)