import keras
from keras import layers
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

x = np.array([[1],[2],[3],[4],[5],[6]])
y = np.array([12,18,24,30,37,45])

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

print("Pentru 7 km parcursi, pretul cursei de pizza este: ", predictie)

sns.barplot(
    x=x.flatten(),
    y=y,
    color="orange",
    alpha=0.5
)
plt.title("Pretul cursei de pizza in functie de km parcursi")
plt.xlabel("Km parcursi")
plt.ylabel("Pretul cursei de pizza")
plt.show()
