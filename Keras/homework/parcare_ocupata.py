import keras
from keras import layers
import numpy as np

x = np.array([[8],[10],[12],[14],[16],[18]])
y = np.array([0,0,1,1,1,0])

model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(4, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    x,
    y,
    epochs=100,
    verbose=0
)

predictie = model.predict(
    np.array([13]),
    verbose=0
)

print("Pentru 13 locuri ocupate, probabilitatea ca parcarea sa fie ocupata este: ",
      predictie)

if predictie > 0.5:
    print("Parcarea este ocupata")
else:
    print("Parcarea este probabil libera")