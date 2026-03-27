# Week 2: Tools and Technologies

## 📋 Overview
This document outlines all the tools, technologies, frameworks, and libraries required for the Underwater Animal Detection project using CNN and LLM.

---

## 🛠️ Development Environment

### 1. Programming Language
- **Python 3.7+**
  - Reason: Industry standard for machine learning and deep learning
  - Extensive library support
  - Easy to learn and implement

### 2. IDE / Code Editor
- **Visual Studio Code** (Recommended)
  - Python extension
  - Jupyter extension
  - Git integration
- **PyCharm** (Alternative)
- **Jupyter Notebook** (For experimentation)

### 3. Version Control
- **Git**
  - Track code changes
  - Collaborate with team
  - Maintain project history
- **GitHub** (Repository hosting)

---

## 🧠 Deep Learning Frameworks

### 1. TensorFlow 2.x
- **Purpose**: Primary deep learning framework
- **Features**:
  - Build and train CNN models
  - Pre-trained models (Transfer Learning)
  - GPU acceleration support
  - Production deployment ready
- **Installation**: `pip install tensorflow`

### 2. Keras (Integrated with TensorFlow)
- **Purpose**: High-level neural network API
- **Features**:
  - Easy model building
  - Sequential and Functional API
  - Pre-trained models (MobileNet, ResNet, VGG)
  - Simple training and evaluation
- **Installation**: Included with TensorFlow 2.x

---

## 📊 Data Processing Libraries

### 1. NumPy
- **Purpose**: Numerical computing
- **Usage**:
  - Array operations
  - Mathematical computations
  - Data manipulation
- **Installation**: `pip install numpy`

### 2. Pandas
- **Purpose**: Data analysis and manipulation
- **Usage**:
  - Dataset statistics
  - CSV file handling
  - Data cleaning
  - Report generation
- **Installation**: `pip install pandas`

### 3. OpenCV (cv2)
- **Purpose**: Computer vision and image processing
- **Usage**:
  - Image loading and preprocessing
  - Image transformations
  - Color space conversions
  - Image augmentation
- **Installation**: `pip install opencv-python`

### 4. Pillow (PIL)
- **Purpose**: Image processing library
- **Usage**:
  - Image loading
  - Format conversions
  - Basic image operations
- **Installation**: `pip install Pillow`

---

## 📈 Visualization Libraries

### 1. Matplotlib
- **Purpose**: Data visualization
- **Usage**:
  - Plot training curves (accuracy, loss)
  - Display images
  - Create charts and graphs
- **Installation**: `pip install matplotlib`

### 2. Seaborn
- **Purpose**: Statistical data visualization
- **Usage**:
  - Confusion matrix heatmaps
  - Distribution plots
  - Enhanced visualizations
- **Installation**: `pip install seaborn`

---

## 🔬 Machine Learning Libraries

### 1. Scikit-learn
- **Purpose**: Machine learning utilities
- **Usage**:
  - Train-test split
  - Classification metrics (precision, recall, F1-score)
  - Confusion matrix
  - Class weight computation
- **Installation**: `pip install scikit-learn`

---

## 🤖 LLM Integration (Phase 2 - Future)

### 1. OpenAI API
- **Purpose**: GPT models for text generation
- **Usage**: Generate animal descriptions
- **Installation**: `pip install openai`

### 2. Hugging Face Transformers
- **Purpose**: Open-source LLM models
- **Usage**: Local LLM deployment
- **Installation**: `pip install transformers`

### 3. LangChain
- **Purpose**: LLM application framework
- **Usage**: Chain CNN predictions with LLM descriptions
- **Installation**: `pip install langchain`

---

## 💾 Data Storage and Management

### 1. File System
- **Structure**: Organized folder hierarchy
- **Format**: Images (JPG, PNG)
- **Organization**: Class-based folders

### 2. CSV Files
- **Purpose**: Dataset metadata and reports
- **Usage**: Class distribution, predictions, metrics

---

## 🖥️ Hardware Requirements

### Minimum Requirements:
- **CPU**: Intel i5 or equivalent
- **RAM**: 8 GB
- **Storage**: 10 GB free space
- **OS**: Windows 10/11, macOS, Linux

### Recommended Requirements:
- **CPU**: Intel i7 or equivalent
- **RAM**: 16 GB
- **GPU**: NVIDIA GPU with CUDA support (GTX 1060 or better)
- **Storage**: 20 GB free space
- **OS**: Windows 10/11, macOS, Linux

### GPU Acceleration (Optional but Recommended):
- **CUDA Toolkit**: For NVIDIA GPU support
- **cuDNN**: Deep learning GPU acceleration
- **Benefits**: 10-50x faster training

---

## 📦 Package Management

### 1. pip
- **Purpose**: Python package installer
- **Usage**: Install all required libraries
- **Command**: `pip install -r requirements.txt`

### 2. Virtual Environment (Recommended)
- **Purpose**: Isolated Python environment
- **Tools**:
  - `venv` (built-in)
  - `conda` (Anaconda)
- **Benefits**:
  - Avoid dependency conflicts
  - Project-specific packages
  - Easy deployment

**Setup:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🌐 Web Development (Future Enhancement)

### For Web Interface:
- **Flask** or **FastAPI**: Backend framework
- **HTML/CSS/JavaScript**: Frontend
- **Bootstrap**: UI framework
- **jQuery**: JavaScript library

---

## 📱 Deployment Tools (Future)

### 1. Docker
- **Purpose**: Containerization
- **Usage**: Package application with dependencies

### 2. Cloud Platforms
- **AWS**: Amazon Web Services
- **Google Cloud Platform**: GCP
- **Microsoft Azure**: Azure ML
- **Heroku**: Simple deployment

---

## 🔧 Development Tools

### 1. Jupyter Notebook
- **Purpose**: Interactive development
- **Usage**: Experimentation and visualization

### 2. TensorBoard
- **Purpose**: Training visualization
- **Usage**: Monitor training progress
- **Installation**: Included with TensorFlow

### 3. Git
- **Purpose**: Version control
- **Usage**: Track changes, collaborate

---

## 📚 Documentation Tools

### 1. Markdown
- **Purpose**: Documentation format
- **Usage**: README files, project documentation

### 2. Sphinx (Optional)
- **Purpose**: Generate documentation
- **Usage**: API documentation

---

## 🧪 Testing Tools (Optional)

### 1. pytest
- **Purpose**: Unit testing
- **Usage**: Test functions and modules

### 2. unittest
- **Purpose**: Built-in testing framework
- **Usage**: Test code functionality

---

## 📋 Complete Requirements File

**requirements.txt:**
```
tensorflow>=2.10.0
keras>=2.10.0
numpy>=1.21.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
opencv-python>=4.5.0
scikit-learn>=1.0.0
Pillow>=8.3.0
```

**Installation Command:**
```bash
pip install -r requirements.txt
```

---

## 🎯 Technology Stack Summary

| Category | Technology | Purpose |
|----------|-----------|---------|
| Language | Python 3.7+ | Core programming |
| DL Framework | TensorFlow/Keras | Model building & training |
| Image Processing | OpenCV, Pillow | Image manipulation |
| Data Analysis | Pandas, NumPy | Data handling |
| Visualization | Matplotlib, Seaborn | Plotting & charts |
| ML Utilities | Scikit-learn | Metrics & evaluation |
| Version Control | Git/GitHub | Code management |
| IDE | VS Code | Development environment |

---

## 🚀 Setup Instructions

### Step 1: Install Python
```bash
# Check Python version
python --version

# Should be 3.7 or higher
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy as np; print('NumPy:', np.__version__)"
```

### Step 5: GPU Setup (Optional)
```bash
# Check GPU availability
python -c "import tensorflow as tf; print('GPU Available:', tf.config.list_physical_devices('GPU'))"
```

---

## 📖 Learning Resources

### TensorFlow/Keras:
- Official Documentation: https://www.tensorflow.org/
- Keras Guide: https://keras.io/

### OpenCV:
- Documentation: https://docs.opencv.org/

### Python:
- Official Tutorial: https://docs.python.org/3/tutorial/

### Deep Learning:
- Deep Learning Specialization (Coursera)
- Fast.ai Practical Deep Learning

---

## ✅ Week 2 Deliverables

- [x] Identified all required tools and technologies
- [x] Listed hardware requirements
- [x] Created requirements.txt file
- [x] Documented installation procedures
- [x] Prepared development environment setup guide

---

## 🔄 Next Steps (Week 3)

- Research and finalize dataset sources
- Evaluate dataset quality and size
- Plan data collection strategy
- Determine dataset structure

---

**Date Completed:** Week 2  
**Status:** ✅ Complete  
**Next Phase:** Week 3 - Dataset Research