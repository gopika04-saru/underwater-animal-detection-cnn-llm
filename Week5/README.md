# Week 5: Data Loading and Preprocessing Setup

## 📋 Overview
Week 5 focuses on setting up the data loading pipeline, implementing data augmentation, and preparing the dataset for model training. This phase establishes the foundation for the actual model training in Week 6.

---

## 🎯 Objectives

1. ✅ Set up data loading pipeline using Keras ImageDataGenerator
2. ✅ Implement data augmentation techniques
3. ✅ Create train/validation/test data generators
4. ✅ Establish class mapping system
5. ✅ Generate comprehensive dataset statistics
6. ✅ Analyze class imbalance
7. ✅ Prepare data preprocessing configuration

---

## 📁 Week 5 Contents

```
Week5/
├── train_model.py           # Data loading and preprocessing script
└── outputs/
    └── dataset_report.txt   # Generated dataset statistics report
```

---

## 🔧 Implementation Details

### 1. Data Loading Pipeline (`train_model.py`)

#### Key Components:

**A. Path Configuration**
```python
train_dir = "../Week4_Dataset_collection/Dataset/Train"
valid_dir = "../Week4_Dataset_collection/Dataset/validation"
test_dir  = "../Week4_Dataset_collection/Dataset/Test"
```

**B. Image Parameters**
- **Image Size**: 224x224 pixels (standard for CNN models)
- **Batch Size**: 32 images per batch
- **Color Mode**: RGB (3 channels)

**C. Data Augmentation (Training Set)**
Implemented augmentation techniques:
- ✅ **Rescaling**: Normalize pixel values (0-1 range)
- ✅ **Rotation**: ±20 degrees random rotation
- ✅ **Zoom**: ±20% random zoom
- ✅ **Horizontal Flip**: Random horizontal flipping
- ✅ **Brightness**: ±20% brightness adjustment
- ✅ **Fill Mode**: 'nearest' for filling empty pixels

**Purpose**: Increase dataset diversity and model robustness

**D. Validation/Test Data Processing**
- Only rescaling applied (no augmentation)
- Maintains original image characteristics for fair evaluation

---

## 📊 Dataset Statistics Generated

### Dataset Split Information:
- **Training Images**: 5,854 (46%)
- **Validation Images**: 3,357 (26%)
- **Test Images**: 3,502 (28%)
- **Total Images**: 12,713

### Class Distribution (Training Set):

| Class | Image Count |
|-------|-------------|
| Turtle_Tortoise | 442 (Most) |
| Dolphin | 410 |
| Jelly Fish | 397 |
| Clams | 294 |
| Sea Rays | 288 |
| Sharks | 270 |
| Sea Urchins | 267 |
| Corals | 259 |
| Penguin | 256 |
| Starfish | 249 |
| Otter | 244 |
| Whale | 241 |
| Lobster | 227 |
| Squid | 227 |
| Eel | 225 |
| Fish | 214 |
| Shrimp | 208 |
| Crabs | 200 |
| Octopus | 192 |
| Seahorse | 190 |
| Seal | 190 |
| Nudibranchs | 188 |
| Puffers | 176 (Least) |

### Class Imbalance Analysis:
- **Max Images**: 442 (Turtle_Tortoise)
- **Min Images**: 176 (Puffers)
- **Imbalance Ratio**: 2.51
- **Status**: Dataset is Imbalanced (ratio > 2)

**Implication**: Will need to use class weights during training to handle imbalance

---

## 🔢 Class Mapping System

### Mapping (Starting from 1):
```
1  : Clams
2  : Corals
3  : Crabs
4  : Dolphin
5  : Eel
6  : Fish
7  : Jelly Fish
8  : Lobster
9  : Nudibranchs
10 : Octopus
11 : Otter
12 : Penguin
13 : Puffers
14 : Sea Rays
15 : Sea Urchins
16 : Seahorse
17 : Seal
18 : Sharks
19 : Shrimp
20 : Squid
21 : Starfish
22 : Turtle_Tortoise
23 : Whale
```

**Purpose**: Consistent class indexing for model training and prediction

---

## 🎨 Data Augmentation Strategy

### Why Data Augmentation?

1. **Increase Dataset Size**: Artificially expand training data
2. **Improve Generalization**: Model learns to handle variations
3. **Reduce Overfitting**: More diverse training examples
4. **Handle Real-world Variations**: Rotation, zoom, lighting changes

### Augmentation Techniques Applied:

#### 1. Rotation (±20°)
- **Purpose**: Handle images taken from different angles
- **Effect**: Model learns orientation-invariant features

#### 2. Zoom (±20%)
- **Purpose**: Handle animals at different distances
- **Effect**: Model learns scale-invariant features

#### 3. Horizontal Flip
- **Purpose**: Double the dataset with mirror images
- **Effect**: Model learns left-right symmetry

#### 4. Brightness Adjustment (±20%)
- **Purpose**: Handle different lighting conditions underwater
- **Effect**: Model becomes robust to illumination changes

#### 5. Rescaling (0-1 normalization)
- **Purpose**: Standardize pixel values
- **Effect**: Faster and more stable training

---

## 📈 Data Generator Configuration

### Training Data Generator:
```python
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest'
)
```

### Validation/Test Data Generator:
```python
valid_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)
```

**Note**: No augmentation on validation/test sets to ensure fair evaluation

---

## 🔍 Key Findings

### 1. Dataset Quality
- ✅ All images successfully loaded
- ✅ No corrupted files detected
- ✅ Consistent image formats (JPG)
- ✅ Proper folder structure maintained

### 2. Class Distribution
- ⚠️ Moderate class imbalance (ratio: 2.51)
- ✅ All classes have sufficient samples (176-442 images)
- ✅ No severely underrepresented classes

### 3. Data Split
- ✅ Proper train/validation/test split
- ✅ Adequate validation set (26%)
- ✅ Sufficient test set (28%)

---

## 🚀 Usage Instructions

### Run Data Loading Script:
```bash
cd Week5
python train_model.py
```

### Expected Output:
```
Found 5854 images belonging to 23 classes.
Found 3357 images belonging to 23 classes.
Found 3502 images belonging to 23 classes.

Class Mapping (Starting from 1)
--------------------------------
1 : Clams
2 : Corals
...

Dataset Summary
--------------------
Train images: 5854
Validation images: 3357
Test images: 3502
Total images: 12713

Class Imbalance Analysis
-----------------------
Max images in class: 442
Min images in class: 176
Imbalance Ratio: 2.51
Status: Dataset is Imbalanced

Dataset report saved successfully!
Location: outputs/dataset_report.txt
```

---

## 📊 Generated Outputs

### 1. dataset_report.txt
Comprehensive report containing:
- Dataset split information
- Class mapping (1-23)
- Class distribution per training set
- Class imbalance analysis
- Total image counts

**Location**: `Week5/outputs/dataset_report.txt`

---

## 🔧 Technical Specifications

### ImageDataGenerator Parameters:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| rescale | 1./255 | Normalize pixels to 0-1 |
| rotation_range | 20 | Random rotation ±20° |
| zoom_range | 0.2 | Random zoom ±20% |
| horizontal_flip | True | Random horizontal flip |
| brightness_range | [0.8, 1.2] | Brightness ±20% |
| fill_mode | 'nearest' | Fill empty pixels |
| target_size | (224, 224) | Resize all images |
| batch_size | 32 | Images per batch |
| class_mode | 'categorical' | Multi-class classification |

---

## 🎯 Achievements

### Week 5 Deliverables:
- ✅ Data loading pipeline established
- ✅ Data augmentation implemented
- ✅ Train/validation/test generators created
- ✅ Class mapping system defined
- ✅ Dataset statistics generated
- ✅ Class imbalance identified
- ✅ Comprehensive report created

---

## ⚠️ Identified Challenges

### 1. Class Imbalance (Ratio: 2.51)
**Problem**: Some classes have 2.5x more images than others

**Solutions for Week 6**:
- Use class weights during training
- Apply weighted loss function
- Consider oversampling minority classes
- Use stratified sampling

### 2. Underwater Image Characteristics
**Challenges**:
- Color distortion (blue/green dominance)
- Variable lighting conditions
- Complex backgrounds
- Similar-looking species

**Solutions Applied**:
- Data augmentation (brightness, rotation)
- Transfer learning (pre-trained models)
- Proper preprocessing (normalization)

---

## 🔄 Next Steps (Week 6)

### Model Training Phase:
1. ✅ Use prepared data generators
2. ✅ Implement CNN architectures
3. ✅ Apply class weights for imbalance
4. ✅ Train multiple models (CNN, MobileNetV2, ResNet50)
5. ✅ Monitor training with validation data
6. ✅ Save best models
7. ✅ Generate training visualizations

---

## 📚 Code Structure

### Main Components:

1. **Path Setup**: Define dataset directories
2. **Data Generators**: Create augmented data pipelines
3. **Data Loading**: Load train/validation/test sets
4. **Class Mapping**: Create index-to-class mapping
5. **Statistics**: Calculate dataset metrics
6. **Imbalance Analysis**: Detect class distribution issues
7. **Report Generation**: Save comprehensive statistics

---

## 🎓 Learning Outcomes

### Technical Skills Developed:
- ✅ Keras ImageDataGenerator usage
- ✅ Data augmentation techniques
- ✅ Batch processing implementation
- ✅ Class imbalance handling
- ✅ Data pipeline optimization

### Best Practices Applied:
- ✅ Separate augmentation for train/validation/test
- ✅ Consistent image sizing
- ✅ Proper normalization
- ✅ Batch processing for efficiency
- ✅ Comprehensive documentation

---

## 📊 Performance Considerations

### Data Loading Efficiency:
- **Batch Size**: 32 (balanced for memory and speed)
- **Image Size**: 224x224 (standard for CNNs)
- **Augmentation**: Applied on-the-fly (memory efficient)
- **Caching**: Not implemented (can be added for speed)

### Memory Usage:
- **Per Batch**: ~32 MB (32 images × 224 × 224 × 3 × 4 bytes)
- **Total Dataset**: ~2.5 GB (all images)
- **Recommendation**: Use batch processing (already implemented)

---

## ✅ Validation Checklist

- [x] Data generators created successfully
- [x] All 23 classes loaded correctly
- [x] Image counts match expected values
- [x] Augmentation working properly
- [x] Class mapping established
- [x] Statistics report generated
- [x] No errors or warnings
- [x] Ready for model training

---

## 📝 Summary

Week 5 successfully established the complete data loading and preprocessing pipeline. The implementation includes:

- **Robust data generators** with proper augmentation
- **Comprehensive statistics** about the dataset
- **Class imbalance detection** for informed training
- **Standardized preprocessing** for consistent model input
- **Ready-to-use data pipeline** for Week 6 training

**Status**: ✅ Complete and Ready for Model Training

---

**Date Completed**: Week 5  
**Next Phase**: Week 6 - Model Training and Evaluation  
**Dependencies**: Week 4 Dataset Collection  
**Outputs**: Data generators, dataset_report.txt