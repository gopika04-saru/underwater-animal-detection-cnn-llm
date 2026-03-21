import os
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models

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
EPOCHS = 10   # faster training

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
# Load Data
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

# -----------------------------
# Load Pretrained MobileNetV2
# -----------------------------
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

# Freeze base model
for layer in base_model.layers:
    layer.trainable = False

# -----------------------------
# Add Custom Layers
# -----------------------------
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)

output = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)

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
model.save(os.path.join(output_dir, "mobilenet_model.h5"))

print("MobileNet model saved!")

# -----------------------------
# Accuracy Graph
# -----------------------------
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("MobileNet Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(["Train","Validation"])

plt.savefig(os.path.join(output_dir, "mobilenet_accuracy.png"))
plt.close()

# -----------------------------
# Loss Graph
# -----------------------------
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("MobileNet Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend(["Train","Validation"])

plt.savefig(os.path.join(output_dir, "mobilenet_loss.png"))
plt.close()

print("Training graphs saved!")