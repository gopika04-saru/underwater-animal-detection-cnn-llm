import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
test_dir  = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "Test")
model_path = os.path.join(BASE_DIR, "outputs", "mobilenet_model.h5")

# Load model
model = tf.keras.models.load_model(model_path)

# Data generator
test_datagen = ImageDataGenerator(rescale=1./255)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224,224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False   # IMPORTANT
)

# Predictions
predictions = model.predict(test_data)
y_pred = np.argmax(predictions, axis=1)
y_true = test_data.classes

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)

# Plot
plt.figure(figsize=(10,8))
sns.heatmap(cm, annot=False, cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig(os.path.join(BASE_DIR, "outputs", "confusion_matrix.png"))
plt.close()

# Classification Report
report = classification_report(y_true, y_pred, target_names=list(test_data.class_indices.keys()))

with open(os.path.join(BASE_DIR, "outputs", "classification_report.txt"), "w") as f:
    f.write(report)

print("Confusion Matrix & Report saved!")