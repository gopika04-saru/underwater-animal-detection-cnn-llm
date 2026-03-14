# Dataset – Underwater Animal Detection (CNN + LLM)

## Dataset Source

The dataset used for this project is the **Sea Animals Image Dataset** available on Kaggle.

Source: https://www.kaggle.com/datasets/vencerlanz09/sea-animals-image-dataste

This dataset contains images of various underwater animals used for training a Convolutional Neural Network (CNN) for underwater animal classification and detection.

---

## Dataset Download

### Method 1 – Kaggle Website

1. Open the dataset link.
2. Login to Kaggle.
3. Click **Download**.
4. Extract the downloaded ZIP file into the project folder.

### Method 2 – Kaggle API (Command Line)

Install Kaggle API:

```
pip install kaggle
```

Download dataset:

```
kaggle datasets download -d vencerlanz09/sea-animals-image-dataste
```

Extract dataset:

```
unzip sea-animals-image-dataste.zip
```

---

## Dataset Structure

After extraction, the dataset contains folders for each marine animal class:

```
Dataset/

 ├── Clams
 ├── Corals
 ├── Crabs
 ├── Dolphin
 ├── Eel
 ├── Fish
 ├── Jelly Fish
 ├── Lobster
 ├── Nudibranchs
 ├── Octopus
 ├── Otter
 ├── Penguin
 ├── Puffers
 ├── Sea Rays
 ├── Sea Urchins
 ├── Seahorse
 ├── Seal
 ├── Sharks
 ├── Shrimp
 ├── Squid
 ├── Starfish
 ├── Turtle_Tortoise
 └── Whale
```

Each folder contains images belonging to that specific underwater animal class.

---

## Total Classes

The dataset contains **23 underwater animal categories**:

* Clams
* Corals
* Crabs
* Dolphin
* Eel
* Fish
* Jelly Fish
* Lobster
* Nudibranchs
* Octopus
* Otter
* Penguin
* Puffers
* Sea Rays
* Sea Urchins
* Seahorse
* Seal
* Sharks
* Shrimp
* Squid
* Starfish
* Turtle / Tortoise
* Whale

---

## Usage in the Project

The dataset is used to train a **CNN model** to classify underwater animals.

Project pipeline:

```
Dataset Images
      ↓
CNN Model (Feature Extraction)
      ↓
Animal Classification
      ↓
LLM generates textual description of detected animal
```

Example Output:

```
Input Image → Jellyfish
CNN Prediction → Jellyfish
LLM Output → "Jellyfish are gelatinous marine animals known for their umbrella-shaped bodies."
```

---

## Notes

* Images are used for training and validation.
* Dataset split into **Train / Validation / Test** sets before training the CNN model.
* Data preprocessing includes image resizing, normalization, and augmentation.
