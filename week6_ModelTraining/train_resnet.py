import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import layers, models

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

train_dir = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "Train")
valid_dir = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "validation")

output_dir = os.path.join(BASE_DIR, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Data
train_datagen = ImageDataGenerator(rescale=1./255)
valid_datagen = ImageDataGenerator(rescale=1./255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical'
)

valid_data = valid_datagen.flow_from_directory(
    valid_dir,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical'
)

num_classes = train_data.num_classes

# Load ResNet50
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

# Freeze layers
for layer in base_model.layers:
    layer.trainable = False

# Add custom head
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)

output = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=output)

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    train_data,
    validation_data=valid_data,
    epochs=10
)

# Save
model.save(os.path.join(output_dir, "resnet_model.h5"))

print("ResNet model saved!")