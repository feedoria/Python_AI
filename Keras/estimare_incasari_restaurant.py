import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import keras
from keras import layers

# Date de antrenare
x_train = np.array([[10],[20],[30],[40],[50],[60]])
y_train = np.array([200,400,600,800,1000,1200])

# Date de test
x_test = np.array([[70],[80]])
y_test = np.array([1400,1600])

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

mse, mae = model.evaluate(
    x_test,
    y_test,
    verbose=0
)

predict = model.predict(
    np.array([[95]]),
    verbose=0
)

print(f"Eroarea medie este: {mae}")

print(f"Incasarile estimate pentru 95 de clienti sunt: {predict[0][0]} lei")

sns.barplot(
    x=x_train.flatten(),
    y=y_train
)

plt.title("Incasari restaurant")
plt.xlabel("Numar clienti")
plt.ylabel("Incasari lei")
plt.show()


