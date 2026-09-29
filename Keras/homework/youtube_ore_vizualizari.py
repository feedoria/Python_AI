import keras
from keras import layers
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([[1],[2],[3],[4],[5],[6]])
y = np.array([100,180,300,450,600,800])

model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(4, activation="relu"),
    layers.Dense(1)
])

model.compile(
    optimizer="adam",
    loss="mse"
)

model.fit(
    x,
    y,
    epochs=200,
    verbose=0
)

predictie = model.predict(
    np.array([[7]]),
    verbose=0
)

sns.barplot(
    x=x.flatten(),
    y=y,
    color="pink",
    alpha=0.5
)

plt.title("Vizualizari in functie de timp")
plt.xlabel("Ore vizualizate")
plt.ylabel("Numar vizualizari")
plt.show()


