import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import keras
from keras import layers

x_train = np.array([[100],[200],[300],[400],[500],[600]]) # distanta zborului
y_train = np.array([50,100,150,200,250,300]) # combustibil necesar

x_test = np.array([[700],[800]])
y_test = np.array([350,400])

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

print(f"Eroarea medie este: {mae}")

predict = model.predict(
    np.array([[950]]),
    verbose=0
)

print(f"Combustibilul estimat pentru 950 km este: {predict[0][0]} litri")

sns.scatterplot(
    x=x_train.flatten(),
    y=y_train
)

sns.regplot(
    x=x_train.flatten(),
    y=y_train
)

plt.title("Distanta zborului si combustibilul")
plt.xlabel("Distanta km")
plt.ylabel("Combustibil litri")
plt.show()