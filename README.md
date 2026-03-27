# 🐠 Underwater Animal Detection using CNN

A deep learning project for detecting and classifying 23 different underwater marine animals using Convolutional Neural Networks (CNN). This project implements multiple CNN architectures including custom CNN, MobileNetV2, and ResNet50 for image classification.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Dataset](#dataset)
- [Models Implemented](#models-implemented)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Results](#results)
- [Future Work](#future-work)

---

## 🎯 Project Overview

This is a final year project focused on underwater animal detection using deep learning. The current implementation covers:
- ✅ Dataset collection and preprocessing
- ✅ Multiple CNN model architectures
- ✅ Training and evaluation pipelines
- ✅ Single image and batch prediction
- 🔄 LLM integration for animal descriptions (Future work)

### Detected Animals (23 Classes)
Clams, Corals, Crabs, Dolphin, Eel, Fish, Jelly Fish, Lobster, Nudibranchs, Octopus, Otter, Penguin, Puffers, Sea Rays, Sea Urchins, Seahorse, Seal, Sharks, Shrimp, Squid, Starfish, Turtle/Tortoise, Whale

---

## 📊 Dataset

- **Total Images:** 12,713
- **Training Set:** 5,854 images (46%)
- **Validation Set:** 3,357 images (26%)
- **Test Set:** 3,502 images (28%)
- **Image Size:** 224x224 pixels
- **Classes:** 23 underwater animals

### Dataset Structure
```
Week4_Dataset_collection/Dataset/
├── Train/
│   ├── Clams/
│   ├── Corals/
│   ├── Crabs/
│   └── ... (23 classes)
├── validation/
│   └── ... (same structure)
└── Test/
    └── ... (same structure)
```

---

## 🧠 Models Implemented

### 1. Custom CNN
- 3 Convolutional layers (32, 64, 128 filters)
- MaxPooling and Dropout layers
- Dense layers for classification
- **Training:** 15 epochs

### 2. MobileNetV2 (Transfer Learning)
- Pre-trained on ImageNet
- Custom classification head
- Lightweight and fast
- **Training:** 10 epochs
- **Recommended for deployment**

### 3. ResNet50 (Transfer Learning)
- Pre-trained on ImageNet
- Deep residual architecture
- High accuracy potential
- **Training:** 10 epochs

---

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip package manager
- (Optional) GPU with CUDA for faster training

### Setup

1. **Clone the repository**
```bash
cd underwater-animal-detection-cnn-llm
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python -c "import tensorflow as tf; print(tf.__version__)"
```

---

## 💻 Usage

### 1. Data Exploration
Analyze the dataset and generate statistics:
```bash
cd Week4_Dataset_collection/src
python data_exploration.py
```

**Outputs:**
- `class_distribution.png` - Bar chart of class distribution
- `sample_images.png` - Sample images from each class
- `dataset_report.csv` - Dataset statistics
- `class_weights.csv` - Computed class weights

### 2. Train a Model

#### Option A: Train MobileNetV2 (Recommended)
```bash
cd week6_ModelTraining
python train_mobilenet.py
```

#### Option B: Train Custom CNN
```bash
python train_cnn_model.py
```

#### Option C: Train ResNet50
```bash
python train_resnet.py
```

**Training Outputs:**
- `outputs/mobilenet_model.h5` - Trained model
- `outputs/mobilenet_accuracy.png` - Accuracy curves
- `outputs/mobilenet_loss.png` - Loss curves

### 3. Evaluate Model
```bash
cd week6_ModelTraining
python evaluate_model.py
```

**Evaluation Outputs:**
- `outputs/confusion_matrix.png` - Confusion matrix heatmap
- `outputs/classification_report.txt` - Precision, recall, F1-score

### 4. Predict Single Image

Classify a single underwater animal image:
```bash
cd week6_ModelTraining
python predict_single_image.py --image path/to/image.jpg
```

**Example:**
```bash
python predict_single_image.py --image ../Week4_Dataset_collection/Dataset/Test/Dolphin/dolphin_001.jpg
```

**Advanced Options:**
```bash
# Use custom model
python predict_single_image.py --image test.jpg --model outputs/cnn_model.h5

# Show top 5 predictions
python predict_single_image.py --image test.jpg --top_k 5

# Save results to JSON
python predict_single_image.py --image test.jpg --save results.json
```

### 5. Batch Prediction

Predict multiple images in a directory:
```bash
cd week6_ModelTraining
python batch_predict.py --input_dir path/to/images --output predictions.csv
```

**Example:**
```bash
python batch_predict.py --input_dir ../Week4_Dataset_collection/Dataset/Test/Fish --output fish_predictions.csv
```

---

## 📁 Project Structure

```
underwater-animal-detection-cnn-llm/
├── README.md                          # This file
├── PROJECT_ANALYSIS.md                # Detailed project analysis
├── requirements.txt                   # Python dependencies
│
├── Week1_Base_paper/
│   └── week1_research_papers_list.md # Literature review
│
├── Week4_Dataset_collection/
│   ├── Dataset/                       # Training data
│   │   ├── Train/
│   │   ├── validation/
│   │   └── Test/
│   ├── outputs/                       # Dataset analysis outputs
│   └── src/
│       └── data_exploration.py        # Dataset exploration script
│
├── Week5/
│   ├── train_model.py                 # Initial data loading
│   └── outputs/
│       └── dataset_report.txt         # Dataset statistics
│
└── week6_ModelTraining/
    ├── train_cnn_model.py             # Custom CNN training
    ├── train_mobilenet.py             # MobileNetV2 training
    ├── train_resnet.py                # ResNet50 training
    ├── evaluate_model.py              # Model evaluation
    ├── predict_single_image.py        # Single image prediction
    ├── batch_predict.py               # Batch prediction
    └── outputs/                       # Trained models & results
```

---

## 📈 Results

### Expected Performance (After Training)

| Model | Accuracy | Training Time | Model Size |
|-------|----------|---------------|------------|
| Custom CNN | ~70-75% | ~30 min | ~50 MB |
| MobileNetV2 | ~85-90% | ~20 min | ~30 MB |
| ResNet50 | ~88-92% | ~40 min | ~100 MB |

*Note: Actual results depend on hardware and training configuration*

### Sample Prediction Output
```
🔍 Analyzing image: dolphin_test.jpg

============================================================
🐠 PREDICTION RESULTS
============================================================

🎯 Predicted Animal: Dolphin
📊 Confidence: 94.32%

📈 Top 3 Predictions:
------------------------------------------------------------
1. Dolphin              94.32% ███████████████████████████████████████████████
2. Whale                 3.21% █
3. Seal                  1.15% 
============================================================
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Model not found error**
```
❌ Error: Model not found at outputs/mobilenet_model.h5
```
**Solution:** Train a model first using `train_mobilenet.py`

**2. Out of memory error**
```
ResourceExhaustedError: OOM when allocating tensor
```
**Solution:** Reduce batch size in training scripts (e.g., BATCH_SIZE = 16)

**3. Import errors**
```
ModuleNotFoundError: No module named 'tensorflow'
```
**Solution:** Install dependencies: `pip install -r requirements.txt`

---

## 🎓 Research Foundation

This project is based on the research paper:
**"Advancing Underwater Vision: A Survey of Deep Learning Models for Underwater Object Recognition and Tracking"**

### Key Challenges Addressed:
- Color distortion in underwater images
- Light scattering and reduced visibility
- Dynamic lighting conditions
- Complex marine environments

### Deep Learning Approaches:
- Convolutional Neural Networks (CNN)
- Transfer Learning with pre-trained models
- Data augmentation for robustness
- Multi-class classification

---

## 🚀 Future Work

### Phase 2: LLM Integration (Planned)
- [ ] Integrate Large Language Model (LLM)
- [ ] Generate detailed animal descriptions
- [ ] Provide habitat information
- [ ] Add conservation status
- [ ] Include interesting facts

### Additional Enhancements
- [ ] Web-based user interface
- [ ] Real-time video detection
- [ ] Mobile app deployment
- [ ] API for integration
- [ ] Model optimization for edge devices

---

## 📝 Quick Start for Review

### Minimum Steps to Demo:

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Train MobileNetV2 (fastest)**
```bash
cd week6_ModelTraining
python train_mobilenet.py
```

3. **Test prediction**
```bash
python predict_single_image.py --image ../Week4_Dataset_collection/Dataset/Test/Dolphin/dolphin_001.jpg
```

**Expected Time:** ~25 minutes (20 min training + 5 min setup)

---

## 👥 Contributors

- **Your Name** - Final Year Project
- **Institution:** [Your University]
- **Year:** 2026

---

## 📄 License

This project is created for educational purposes as part of a final year project.

---

## 🙏 Acknowledgments

- Dataset sources: [Kaggle/Custom Collection]
- TensorFlow/Keras framework
- Research paper authors
- Project supervisors and mentors

---

## 📞 Contact

For questions or feedback:
- Email: [your.email@example.com]
- GitHub: [your-github-username]

---

**Last Updated:** March 21, 2026

**Status:** ✅ Ready for Review (CNN Implementation Complete)