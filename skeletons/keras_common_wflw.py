import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# 1. Prepare the data
# Replace with your own data loading and preprocessing
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train.reshape(-1, 28*28).astype("float32") / 255
x_test = x_test.reshape(-1, 28*28).astype("float32") / 255

# 2. Define the model
model = keras.Sequential([
    layers.Dense(64, activation="relu", input_shape=(28*28,)),
    layers.Dense(32, activation="relu"),
    layers.Dense(10, activation="softmax")
])

# 3. Compile the model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# 4. Train the model
history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

# 5. Evaluate the model
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"Test accuracy: {test_acc:.3f}")

# 6. Make predictions
predictions = model.predict(x_test[:5])
print("Predictions shape:", predictions.shape)