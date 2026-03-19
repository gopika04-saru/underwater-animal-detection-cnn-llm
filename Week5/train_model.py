from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

train_dir = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "Train")
valid_dir = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "validation")
test_dir  = os.path.join(BASE_DIR, "..", "Week4_Dataset_collection", "Dataset", "Test")

# -----------------------------
# Create outputs folder INSIDE Week5
# -----------------------------
output_dir = os.path.join(BASE_DIR, "outputs")
os.makedirs(output_dir, exist_ok=True)

IMG_SIZE = 224
BATCH_SIZE = 32

# -----------------------------
# Training Data Augmentation
# -----------------------------
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8,1.2],
    fill_mode='nearest'
)

# Validation Data
valid_datagen = ImageDataGenerator(rescale=1./255)

# Test Data
test_datagen = ImageDataGenerator(rescale=1./255)


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

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# -----------------------------
# Class Mapping (start from 1)
# -----------------------------
class_mapping = {v+1: k for k, v in train_data.class_indices.items()}

print("\nClass Mapping (Starting from 1)")
print("--------------------------------")

for k, v in class_mapping.items():
    print(k, ":", v)

# -----------------------------
# Dataset Statistics
# -----------------------------
train_count = train_data.samples
valid_count = valid_data.samples
test_count  = test_data.samples

total_images = train_count + valid_count + test_count

print("\nDataset Summary")
print("--------------------")
print("Train images:", train_count)
print("Validation images:", valid_count)
print("Test images:", test_count)
print("Total images:", total_images)

# -----------------------------
# Count images per class
# -----------------------------
class_counts = {}

for class_name in os.listdir(train_dir):
    class_path = os.path.join(train_dir, class_name)

    if os.path.isdir(class_path):
        class_counts[class_name] = len(os.listdir(class_path))

# -----------------------------
# Detect Class Imbalance
# -----------------------------
max_images = max(class_counts.values())
min_images = min(class_counts.values())
imbalance_ratio = max_images / min_images

print("\nClass Imbalance Analysis")
print("-----------------------")
print("Max images in class:", max_images)
print("Min images in class:", min_images)
print("Imbalance Ratio:", round(imbalance_ratio,2))

if imbalance_ratio > 2:
    imbalance_status = "Dataset is Imbalanced"
else:
    imbalance_status = "Dataset is Balanced"

print("Status:", imbalance_status)

# -----------------------------
# Save Dataset Report
# -----------------------------
report_path = os.path.join(output_dir, "dataset_report.txt")

with open(report_path, "w") as f:

    f.write("UNDERWATER ANIMAL DATASET REPORT\n")
    f.write("================================\n\n")

    f.write("Dataset Split Information\n")
    f.write("-------------------------\n")
    f.write(f"Train Images: {train_count}\n")
    f.write(f"Validation Images: {valid_count}\n")
    f.write(f"Test Images: {test_count}\n\n")

    f.write(f"Total Images:\n{train_count} + {valid_count} + {test_count} = {total_images}\n\n")

    f.write("Class Mapping (Starting from 1)\n")
    f.write("-------------------------------\n")

    for k,v in class_mapping.items():
        f.write(f"{k} : {v}\n")

    f.write("\nClass Distribution (Train Set)\n")
    f.write("-------------------------------\n")

    for k,v in class_counts.items():
        f.write(f"{k} : {v}\n")

    f.write("\nClass Imbalance Analysis\n")
    f.write("------------------------\n")
    f.write(f"Max Images in Class: {max_images}\n")
    f.write(f"Min Images in Class: {min_images}\n")
    f.write(f"Imbalance Ratio: {round(imbalance_ratio,2)}\n")
    f.write(f"Status: {imbalance_status}\n")

print("\nDataset report saved successfully!")
print("Location:", report_path)