import os
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image
from tqdm import tqdm

# -----------------------------
# 0. Paths
# -----------------------------
dataset_path = "../Dataset/Train"
output_path = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(output_path, exist_ok=True)

# create output folder automatically
os.makedirs(output_path, exist_ok=True)

# valid image extensions
valid_ext = (".jpg", ".jpeg", ".png")

# -----------------------------
# 1. Count number of classes
# -----------------------------
classes = sorted(os.listdir(dataset_path))
num_classes = len(classes)

print("\nNumber of Classes:", num_classes)
print("Classes:", classes)

# -----------------------------
# 2. Count images per class
# -----------------------------
image_counts = {}

for cls in classes:
    class_path = os.path.join(dataset_path, cls)

    images = [img for img in os.listdir(class_path)
              if img.lower().endswith(valid_ext)]

    image_counts[cls] = len(images)

print("\nImages per class:")
print(image_counts)

# dataframe
df = pd.DataFrame(list(image_counts.items()), columns=["Class", "Count"])

# -----------------------------
# 3. Plot class distribution
# -----------------------------
plt.figure(figsize=(14,6))
sns.barplot(x="Class", y="Count", data=df)

plt.xticks(rotation=90)
plt.title("Class Distribution")
plt.tight_layout()

plt.savefig(os.path.join(output_path, "class_distribution.png"))
plt.close()

print("Saved: class_distribution.png")

# -----------------------------
# 4. Show sample images
# -----------------------------
plt.figure(figsize=(10,10))

for i, cls in enumerate(classes[:9]):

    class_path = os.path.join(dataset_path, cls)

    images = [img for img in os.listdir(class_path)
              if img.lower().endswith(valid_ext)]

    img_path = os.path.join(class_path, images[0])

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.subplot(3,3,i+1)
    plt.imshow(img)
    plt.title(cls)
    plt.axis("off")

plt.tight_layout()
plt.savefig(os.path.join(output_path, "sample_images.png"))
plt.close()

print("Saved: sample_images.png")

# -----------------------------
# 5. Image resolution analysis
# -----------------------------
widths = []
heights = []

print("\nChecking image resolutions...")

for cls in tqdm(classes):

    class_path = os.path.join(dataset_path, cls)

    images = [img for img in os.listdir(class_path)
              if img.lower().endswith(valid_ext)]

    for img_name in images[:50]:

        img_path = os.path.join(class_path, img_name)

        img = cv2.imread(img_path)

        if img is None:
            continue

        h, w = img.shape[:2]

        heights.append(h)
        widths.append(w)

avg_width = sum(widths)/len(widths)
avg_height = sum(heights)/len(heights)

print("Average Width:", avg_width)
print("Average Height:", avg_height)

# -----------------------------
# 6. Detect corrupted images
# -----------------------------
corrupted = []

print("\nChecking corrupted images...")

for cls in tqdm(classes):

    class_path = os.path.join(dataset_path, cls)

    images = [img for img in os.listdir(class_path)
              if img.lower().endswith(valid_ext)]

    for img_name in images:

        img_path = os.path.join(class_path, img_name)

        try:
            img = Image.open(img_path)
            img.verify()

        except:
            corrupted.append(img_path)

print("\nTotal corrupted images:", len(corrupted))

if len(corrupted) > 0:
    print("Example corrupted files:", corrupted[:5])

# -----------------------------
# 7. Save dataset report
# -----------------------------
report = {
    "Total Classes": num_classes,
    "Total Images": sum(image_counts.values()),
    "Average Width": avg_width,
    "Average Height": avg_height,
    "Corrupted Images": len(corrupted)
}

report_df = pd.DataFrame(report.items(), columns=["Metric", "Value"])

report_df.to_csv(os.path.join(output_path, "dataset_report.csv"), index=False)

print("\nSaved: dataset_report.csv")

print("\nData Exploration Completed Successfully")


# -----------------------------
# Detect Class Imbalance
# -----------------------------
max_images = max(image_counts.values())
min_images = min(image_counts.values())

imbalance_ratio = max_images / min_images

print("\nClass Imbalance Analysis")
print("Max images in a class:", max_images)
print("Min images in a class:", min_images)
print("Imbalance Ratio:", round(imbalance_ratio,2))

if imbalance_ratio > 3:
    print("⚠️ Dataset is highly imbalanced")
else:
    print("✅ Dataset is reasonably balanced")

# save class distribution csv
df.to_csv(os.path.join(output_path, "class_distribution.csv"), index=False)

print("Saved: class_distribution.csv")


# -----------------------------
# Compute class weights
# -----------------------------
from sklearn.utils.class_weight import compute_class_weight
import numpy as np

labels = []

for cls in classes:
    labels += [cls] * image_counts[cls]

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

weights_dict = dict(zip(np.unique(labels), class_weights))

weights_df = pd.DataFrame(list(weights_dict.items()), columns=["Class","Weight"])
weights_df.to_csv(os.path.join(output_path,"class_weights.csv"), index=False)

print("Saved: class_weights.csv")