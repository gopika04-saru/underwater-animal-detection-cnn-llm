import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

train_dir = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "Train")
valid_dir = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "validation")
test_dir  = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "Test")

output_dir = os.path.join(BASE_DIR, "outputs")
os.makedirs(output_dir, exist_ok=True)

# -----------------------------
# Parameters
# -----------------------------
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15

# -----------------------------
# Data Generators
# -----------------------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8,1.2]
)

valid_datagen = ImageDataGenerator(rescale=1./255)

# -----------------------------
# Load Dataset
# -----------------------------
train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

valid_data = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

num_classes = train_data.num_classes

print("Number of classes:", num_classes)

# -----------------------------
# CNN Model Architecture
# -----------------------------
model = Sequential([

    Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),

    Dense(256, activation='relu'),
    Dropout(0.5),

    Dense(num_classes, activation='softmax')

])

# -----------------------------
# Compile Model
# -----------------------------
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# -----------------------------
# Train Model
# -----------------------------
history = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=EPOCHS
)

# -----------------------------
# Save Model
# -----------------------------
model.save(os.path.join(output_dir, "cnn_model.h5"))

print("Model saved successfully!")

# -----------------------------
# Accuracy Graph
# -----------------------------
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(["Train", "Validation"])

plt.savefig(os.path.join(output_dir, "accuracy_graph.png"))
plt.close()

# -----------------------------
# Loss Graph
# -----------------------------
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend(["Train", "Validation"])

plt.savefig(os.path.join(output_dir, "loss_graph.png"))
plt.close()

print("Training graphs saved!")