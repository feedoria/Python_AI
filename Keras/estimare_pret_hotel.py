import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import keras
from keras import layers

x_train = np.array([[1],[2],[3],[4],[5],[6]]) # nr nopti
y_train = np.array([150,300,450,600,750,900]) # pret total cazare

x_test = np.array([[7],[8]])
y_test = np.array([1050,1200])

model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(1)
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.05),
    loss="mse",
    metrics=["mae"]
)

model.fit(
    x_train,
    y_train,
    epochs=300,
    verbose=0
)

mse, mae = model.evaluate(
    x_test,
    y_test,
    verbose=0
)

predict = model.predict(
    np.array([[10]]),
    verbose=0
)

sns.barplot(
    x=x_train.flatten(),
    y=y_train
)

plt.title("Pret hotel in functie de numarul de nopti")
plt.xlabel("Numar nopti")
plt.ylabel("Pret total cazare")
plt.show()