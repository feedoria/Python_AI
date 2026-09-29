import numpy as np
import keras
from keras import layers
 
#Datele pentru invatare
x_train = np.array([[10],[20],[30],[40],[50],[60]])
y_train = np.array([1,2,3,4,5,6])
 
#Datele pentru test
x_test = np.array([[70],[80]])
y_test = np.array([7,8])
 
#Construim reteaua neuronala
model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(1)
])
 
#Pregatim modelul
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.05),
    loss="mse", #Maasoara cat de mare e greseala
    metrics=["mae"] #Arata cate greseli are in medie
)
 
#AI-ul nostru invata din datele de train
model.fit(
    x_train,
    y_train,
    epochs=300,
    verbose=0
)
 
mse,mae = model.evaluate(
    x_test,
    y_test,
    verbose=0
)
print("Eroare medie: ", mae)
 
predictie = model.predict(
    np.array([[104]]),
    verbose=0
)
print("Consum estimat pentru 104 km: ", predictie)
