import keras 
from keras import layers
import numpy as np

x = np.array([[10],[20],[30],[40],[50],[60]])
y = np.array([1,1,1,0,0,0])

model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(4, "relu"),
    layers.Dense(1, "sigmoid")
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.05),
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
    np.array([25]),
    verbose=0
)

print("Pentru biletul de 25 de lei, probabilitatea de a merge la cinema este: ", 
      predictie)
