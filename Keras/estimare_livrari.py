import numpy as np
import keras
from keras import layers
import seaborn as sns
import matplotlib.pyplot as plt

# Date de antrenare
x_train = np.array([[1],[2],[3],[4],[5],[6]])
y_train = np.array([8,16,24,32,40,48])

# Date de test
x_test = np.array([[7],[8]])
y_test = np.array([56,64])

# Construim reteaua neuronala
model = keras.Sequential([
    keras.Input(shape=(1,)),
    layers.Dense(1)
])

# Pregatim modelul pentru antrenare
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.05),
    loss="mse",
    metrics=["mae"]
)

# Antrenam modelul
model.fit(
    x_train,
    y_train,
    epochs=300,
    verbose=0
)

# Evaluam modelul
mse, mae = model.evaluate(
    x_test,
    y_test,
    verbose=0
)

print(f"Eroarea medie este: {mae}")

# Facem predictia pentru 10 km
predictie = model.predict(
    np.array([[10]]),
    verbose=0
)

print(f"Timpul estimat pentru 10 km este: {predictie[0][0]} minute")

# Cream graficul
sns.scatterplot(
    x=x_train.flatten(),
    y=y_train
)

plt.title("Distanta si timpul de livrare")
plt.xlabel("Distanta km")
plt.ylabel("Timp minute")
plt.show()