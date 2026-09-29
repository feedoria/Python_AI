import numpy as np 
import keras
from keras import layers
 
#Datele pentru invatare, pentru learning
x_train=np.array([[1],[2],[3],[4],[5],[6]])
y_train=np.array([10,20,30,40,50,60])
 
#Datele pentru examen
x_test=np.array([[7],[8]])
y_test=np.array([70,80])
 
#Construim o retea neuronala
model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(1)
])
 
#Pregatim modul in care Ai-ul invata
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.05),
    loss="mse",#MSE masoara cat de mare este greseala
    metrics=["mae"]#MAE ne spune cate de mult greseste in medie
)
 
#AI-ul invata doar din datele de train
model.fit(
    x_train,
    y_train,
    epochs=300,
    verbose=0
)
 
mse,mae= model.evaluate(
    x_test,
    y_test,
    verbose=0
)
 
#Afisam cat de mult a gresit la un examen
print("Eroare medie :", mae)
 
#I dam o situatie complet noua 
predictie = model.predict(np.array([9]), verbose=0) #Cat costa 9 caiete
print("Pret estimat pentru 9 caiete: ", predictie[0][0])