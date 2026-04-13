# 🚀 Quick Usage Guide - CNN + LLM Integration

## Simple 3-Step Process

---

## Step 1: Basic Usage (No Setup Required!)

### **Works Immediately with Fallback Descriptions**

```bash
cd Week7_LLM_Integration
python predict_with_llm.py --image path/to/your/image.jpg
```

**Example:**
```bash
python predict_with_llm.py --image ../Week4_Dataset_collection/Dataset/Test/Dolphin/Dolphin\ \(1\).jpg
```

**Output:**
```
🔍 Analyzing image with CNN: Dolphin (1).jpg
🤖 Generating description for: Dolphin
✅ Using curated description

======================================================================
🐠 UNDERWATER ANIMAL DETECTION WITH AI DESCRIPTION
======================================================================

🎯 CNN PREDICTION:
   Animal: Dolphin
   Confidence: 94.32%

📈 Top 3 Predictions:
   1. Dolphin              94.32% ███████████████████████████
   2. Whale                 3.21% █
   3. Seal                  1.15% 

📖 AI-GENERATED DESCRIPTION:
   Dolphins are highly intelligent marine mammals known for their 
   playful behavior and complex social structures. They use 
   echolocation to navigate and hunt, and can swim at speeds up 
   to 20 mph. Found in oceans worldwide, dolphins are known for 
   their acrobatic displays and friendly interactions with humans.

======================================================================
```

---

## Step 2: Advanced Usage (With OpenAI GPT)

### **For Dynamic, AI-Generated Descriptions**

#### **A. Get OpenAI API Key**
1. Go to https://platform.openai.com/
2. Sign up / Log in
3. Create API key
4. Copy the key (starts with "sk-...")

#### **B. Set API Key**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

#### **C. Run with OpenAI**
```bash
python predict_with_llm.py --image dolphin.jpg --use_openai
```

**Benefits:**
- ✅ Dynamic descriptions
- ✅ More detailed information
- ✅ Natural language
- ✅ Varied content each time

**Cost:** ~$0.002 per prediction

---

## Step 3: Output Files (Automatic!)

### **Results Saved Automatically to `outputs/` Folder**

Every prediction automatically creates **TWO files** in the `outputs/` folder:

#### **1. JSON File** (for programmatic access)
`outputs/<image_name>_<timestamp>.json`

#### **2. Text Report** (for human reading)
`outputs/<image_name>_<timestamp>.txt`

**Example Output Files:**
```
outputs/
├── dolphin_20260411_153045.json
├── dolphin_20260411_153045.txt
├── shark_20260411_153120.json
└── shark_20260411_153120.txt
```

**JSON Format:**
```json
{
    "timestamp": "2026-04-11T15:30:45.123456",
    "image_path": "../Week4_Dataset_collection/Dataset/Test/Dolphin/Dolphin (1).jpg",
    "cnn_prediction": {
        "animal": "Dolphin",
        "confidence": 94.32,
        "top_predictions": [
            {"class": "Dolphin", "confidence": 94.32},
            {"class": "Whale", "confidence": 3.21},
            {"class": "Seal", "confidence": 1.15}
        ]
    },
    "llm_description": "Dolphins are highly intelligent..."
}
```

**Text Report Format:**
```
======================================================================
UNDERWATER ANIMAL DETECTION WITH AI DESCRIPTION
======================================================================

Timestamp: 2026-04-11 15:30:45
Image: ../Week4_Dataset_collection/Dataset/Test/Dolphin/Dolphin (1).jpg

----------------------------------------------------------------------
CNN PREDICTION:
----------------------------------------------------------------------
Animal: Dolphin
Confidence: 94.32%

Top 3 Predictions:
  1. Dolphin               94.32%
  2. Whale                  3.21%
  3. Seal                   1.15%

----------------------------------------------------------------------
AI-GENERATED DESCRIPTION:
----------------------------------------------------------------------
Dolphins are highly intelligent marine mammals...

======================================================================
```

### **Disable Auto-Save (Optional)**
If you don't want to save outputs:
```bash
python predict_with_llm.py --image dolphin.jpg --no_save
```

---

## 🎯 Common Use Cases

### **1. Quick Test (Fallback)**
```bash
python predict_with_llm.py --image test.jpg
```

### **2. Production Quality (OpenAI)**
```bash
python predict_with_llm.py --image test.jpg --use_openai
```

### **3. With Custom Model**
```bash
python predict_with_llm.py --image test.jpg --model ../week6_ModelTraining/outputs/resnet_model.h5
```

### **4. Disable Auto-Save**
```bash
python predict_with_llm.py --image test.jpg --no_save
```

### **5. Full Command with OpenAI**
```bash
python predict_with_llm.py \
    --image dolphin.jpg \
    --use_openai \
    --api_key "sk-..."
```

---

## 📊 Comparison: Fallback vs OpenAI

| Feature | Fallback | OpenAI GPT |
|---------|----------|------------|
| **Setup** | None | API key needed |
| **Cost** | Free | ~$0.002/request |
| **Speed** | Instant | 1-2 seconds |
| **Quality** | High (curated) | Excellent (dynamic) |
| **Variety** | Fixed | Varies each time |
| **Offline** | ✅ Yes | ❌ No |

**Recommendation:**
- **Development/Testing:** Use Fallback
- **Demo/Production:** Use OpenAI

---

## 🔧 Troubleshooting

### **Problem 1: Model Not Found**
```
❌ Error: Model not found at outputs/mobilenet_model.h5
```

**Solution:**
```bash
cd week6_ModelTraining
python train_mobilenet.py
```

### **Problem 2: OpenAI Authentication Error**
```
⚠️ OpenAI API error: Authentication failed
```

**Solution:**
- Check API key is correct
- Verify it's set: `echo $OPENAI_API_KEY`
- Try setting it again: `export OPENAI_API_KEY="sk-..."`

### **Problem 3: Image Not Found**
```
❌ Error: Image not found at path/to/image.jpg
```

**Solution:**
- Check file path is correct
- Use absolute path or correct relative path
- Verify file exists: `ls path/to/image.jpg`

---

## 💡 Pro Tips

### **Tip 1: Use Fallback for Development**
Fast, free, and works offline!
```bash
python predict_with_llm.py --image test.jpg
```

### **Tip 2: Batch Process Multiple Images**
```bash
for img in ../Week4_Dataset_collection/Dataset/Test/Dolphin/*.jpg; do
    python predict_with_llm.py --image "$img"
done
```

### **Tip 3: Check Output Files**
Results are automatically saved in the `outputs/` folder:
```bash
ls -lh outputs/
```

### **Tip 4: Test Different Animals**
```bash
# Test dolphin
python predict_with_llm.py --image ../Week4_Dataset_collection/Dataset/Test/Dolphin/Dolphin\ \(1\).jpg

# Test shark
python predict_with_llm.py --image ../Week4_Dataset_collection/Dataset/Test/Sharks/Sharks\ \(1\).jpg

# Test turtle
python predict_with_llm.py --image ../Week4_Dataset_collection/Dataset/Test/Turtle_Tortoise/Turtle_Tortoise\ \(1\).jpg
```

---

## 📝 Command Reference

### **Basic Command:**
```bash
python predict_with_llm.py --image IMAGE_PATH
```

### **All Options:**
```bash
python predict_with_llm.py \
    --image IMAGE_PATH          # Required: Path to image
    --model MODEL_PATH          # Optional: Custom model path
    --use_openai                # Optional: Use OpenAI GPT
    --api_key API_KEY           # Optional: OpenAI API key
    --no_save                   # Optional: Don't save outputs (saves by default)
```

### **Help:**
```bash
python predict_with_llm.py --help
```

---

## ✅ Quick Start Checklist

- [ ] Navigate to Week7_LLM_Integration folder
- [ ] Have a test image ready
- [ ] CNN model trained (mobilenet_model.h5 exists)
- [ ] Run basic command
- [ ] Check console output
- [ ] Check `outputs/` folder for saved results
- [ ] (Optional) Set up OpenAI API key
- [ ] (Optional) Test with OpenAI

---

## 🎉 You're Ready!

**Start with the simplest command:**
```bash
python predict_with_llm.py --image your_image.jpg
```

**It works immediately with no setup! 🚀**