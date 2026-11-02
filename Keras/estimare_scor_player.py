import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import keras
from keras import layers

# Date de antrenare
x_train = np.array([[1],[2],[3],[4],[5],[6]])
y_train = np.array([100,200,300,400,500,600])

# Date de test
x_test = np.array([[7],[8]])
y_test = np.array([700,800])

# Construim reteaua neuronala
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
    np.array([[9]]),
    verbose=0
)

print(f"Eroarea medie este: {mae}")

sns.lineplot(
    x=x_train.flatten(),
    y=y_train
)

plt.title("Incasari livrari")
plt.xlabel("Ore jucate")
plt.ylabel("Scor jucator")
plt.show()