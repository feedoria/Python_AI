import keras
from keras import layers
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([[1],[2],[3],[4],[5],[6]]) # km parcursi
y = np.array([10,15,20,25,30,35]) # pretul cursei

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
    color="blue",
    alpha=0.5
)
plt.title("Pretul cursei in functie de km parcursi")
plt.xlabel("Km parcursi")
plt.ylabel("Pretul cursei")
plt.show()
