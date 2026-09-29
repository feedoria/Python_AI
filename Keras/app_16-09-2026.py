import numpy as np 
import keras #Keras este 'atelierul' in care construim AI-ul
from keras import layers #Layers sunt piesele din care construim reteaua 

x = np.array([[1],[2],[3],[4],[5],[6]])#Ore invatate ca si cum am avea 6 elevi 
y = np.array([0,0,0,1,1,1]) #0 = picat, 1 = provovat 

model = keras.Sequential([ #Cream AI-ul ca un lant de pasi, unul dupa altu 
    keras.Input(shape=(1,)),#Ai-ul primeste o singura informatie: numarul de ore 
    layers.Dense(4,activation="relu"),#neuroni care cauta modele, exact ca 4 oameni care analizeaza situatia 
    layers.Dense(1, activation="sigmoid")#Ultimul neuron care da un raspuns intre 0 si 1 
])

model.compile(optimizer="adam",#Adam corecteaza modelul dupa greseli, exact ca un profesor
             loss="binary_crossentropy",#masoara cat de multe multe gresli face AI
             metrics=["Accuracy"])#Cat de corect a nimerit raspunsul

model.fit(x,y,epochs=100, verbose=0)#Ai-ul repta de 100 de ori ca sa invete
rezultat = model.predict(np.array([[5]]), verbose=0) #Ce parere ai despre cinvea care a invata 5 ore 
print(rezultat[0][0])