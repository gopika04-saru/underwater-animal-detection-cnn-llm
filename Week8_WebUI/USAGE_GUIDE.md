# 🚀 Web UI Usage Guide - Quick Reference

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Single Image Upload](#single-image-upload)
3. [Bulk Image Upload](#bulk-image-upload)
4. [Using OpenAI GPT](#using-openai-gpt)
5. [Understanding Results](#understanding-results)
6. [Tips & Tricks](#tips--tricks)

---

## ⚡ Quick Start

### **3 Simple Steps:**

1. **Start the server**
   ```bash
   cd Week8_WebUI
   ./run.sh          # macOS/Linux
   # OR
   run.bat           # Windows
   ```

2. **Open browser**
   ```
   http://localhost:5000
   ```

3. **Upload & Analyze!**
   - Drag & drop images
   - Click "Analyze"
   - View results instantly

---

## 📷 Single Image Upload

### **Method 1: Click to Upload**
1. Click on the **"📷 Single Image"** tab
2. Click the blue upload area
3. Select an image from your computer
4. Click **"🔍 Analyze Image"**

### **Method 2: Drag & Drop**
1. Open the **"📷 Single Image"** tab
2. Drag an image file from your computer
3. Drop it on the upload area
4. Click **"🔍 Analyze Image"**

### **What You'll See:**
- 🐠 **Animal Name**: Detected species
- 📊 **Confidence**: Prediction accuracy (%)
- 📈 **Top 3 Predictions**: Alternative possibilities
- 📖 **Description**: Educational information
- 🖼️ **Image Preview**: Your uploaded image

---

## 📁 Bulk Image Upload

### **Upload Multiple Images:**
1. Click on the **"📁 Bulk Upload"** tab
2. Click the upload area or drag multiple files
3. Review the file list
4. (Optional) Remove unwanted files
5. Click **"🔍 Analyze All Images"**

### **Features:**
- ✅ Upload up to 10+ images at once
- ✅ See all files before processing
- ✅ Remove individual files from list
- ✅ Process all images in one go
- ✅ View results for each image

### **Results Display:**
Each image shows:
- Image preview
- Predicted animal
- Confidence score
- Top 3 predictions
- Detailed description

---

## 🤖 Using OpenAI GPT

### **Enable AI-Generated Descriptions:**

1. **Set up API key** (one-time setup):
   ```bash
   export OPENAI_API_KEY="sk-your-key-here"
   ```

2. **In the web UI:**
   - Check the box: ☑️ "Use OpenAI GPT for descriptions"
   - Upload and analyze as normal

### **Benefits:**
- 🎯 Dynamic, unique descriptions
- 📚 More detailed information
- 🌟 Natural language explanations
- 🔄 Varied content each time

### **Without OpenAI:**
- Uses curated fallback descriptions
- Still high-quality and educational
- Completely free
- Works offline

---

## 📊 Understanding Results

### **Prediction Card:**

```
┌─────────────────────────────────────┐
│  🖼️ Image Preview                   │
│                                     │
│  🐠 Dolphin                         │
│  📊 Confidence: 94.32%              │
│                                     │
│  📈 Top 3 Predictions:              │
│  1. Dolphin    94.32% ████████████  │
│  2. Whale       3.21% █             │
│  3. Seal        1.15%               │
│                                     │
│  📖 Description                     │
│  Dolphins are highly intelligent... │
│                                     │
│  Source: 🤖 OpenAI GPT              │
└─────────────────────────────────────┘
```

### **Confidence Levels:**

| Confidence | Meaning | Action |
|------------|---------|--------|
| 90-100% | Very High | Trust the prediction |
| 70-89% | High | Likely correct |
| 50-69% | Moderate | Check top 3 predictions |
| Below 50% | Low | Image may be unclear |

### **Top 3 Predictions:**
- Shows alternative possibilities
- Helps understand model uncertainty
- Useful when confidence is moderate

---

## 💡 Tips & Tricks

### **For Best Results:**

1. **Image Quality:**
   - ✅ Clear, well-lit images
   - ✅ Animal is main subject
   - ✅ Minimal background clutter
   - ❌ Avoid blurry images
   - ❌ Avoid extreme angles

2. **File Format:**
   - ✅ JPG/JPEG (recommended)
   - ✅ PNG
   - ✅ BMP
   - ❌ GIF, TIFF, RAW

3. **File Size:**
   - ✅ Under 16MB per image
   - ✅ Recommended: 1-5MB
   - ⚠️ Large files take longer

### **Keyboard Shortcuts:**
- **Ctrl+V**: Paste image from clipboard (in some browsers)
- **Ctrl+R**: Refresh page to start over
- **F5**: Reload page

### **Browser Compatibility:**
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ⚠️ Internet Explorer (not recommended)

---

## 🎯 Common Use Cases

### **1. Educational Learning**
- Upload images of marine animals
- Learn about different species
- Share with students

### **2. Species Identification**
- Identify unknown animals from photos
- Verify species during diving
- Catalog marine life observations

### **3. Research Documentation**
- Process multiple field photos
- Generate species reports
- Track marine biodiversity

### **4. Fun Exploration**
- Test with different animals
- Compare similar species
- Learn marine biology

---

## 🔍 Example Workflow

### **Single Image Analysis:**
```
1. Open http://localhost:5000
2. Click "📷 Single Image" tab
3. Drag dolphin.jpg to upload area
4. Click "🔍 Analyze Image"
5. Wait 1-2 seconds
6. View results:
   - Dolphin (94.32%)
   - Description about dolphins
7. Try another image!
```

### **Bulk Analysis:**
```
1. Open http://localhost:5000
2. Click "📁 Bulk Upload" tab
3. Select 5 underwater images
4. Review file list
5. Click "🔍 Analyze All Images"
6. Wait 5-10 seconds
7. Scroll through all results
8. Each image has its own prediction
```

---

## 📱 Mobile Usage

### **On Mobile Devices:**
1. Open browser on phone/tablet
2. Navigate to: `http://your-computer-ip:5000`
3. Use camera to take photos
4. Upload directly from camera roll
5. View results on mobile screen

### **Mobile Tips:**
- Use landscape mode for better view
- Tap upload area to access camera
- Swipe to view multiple results
- Pinch to zoom on images

---

## 🐛 Quick Troubleshooting

### **Problem: Can't access the website**
**Solution:** 
- Check server is running
- Verify URL: `http://localhost:5000`
- Try: `http://127.0.0.1:5000`

### **Problem: Upload fails**
**Solution:**
- Check file size (max 16MB)
- Verify file format (JPG, PNG, BMP)
- Try a different image

### **Problem: Slow predictions**
**Solution:**
- Reduce image size
- Use fewer images in bulk
- Close other applications
- Disable OpenAI if slow

### **Problem: Wrong predictions**
**Solution:**
- Check image quality
- Ensure animal is clearly visible
- Try different angle/lighting
- Check top 3 predictions

---

## 📊 Performance Guide

### **Expected Times:**

| Operation | Time | Notes |
|-----------|------|-------|
| Single image | 1-2s | Without OpenAI |
| Single + OpenAI | 2-4s | With description |
| Bulk (5 images) | 5-8s | Without OpenAI |
| Bulk + OpenAI | 10-15s | With descriptions |

### **Optimization:**
- Use JPG format (smaller files)
- Resize large images before upload
- Process in smaller batches
- Use fallback descriptions for speed

---

## ✅ Best Practices

### **Do:**
- ✅ Use clear, focused images
- ✅ Upload appropriate file sizes
- ✅ Check top 3 predictions
- ✅ Read descriptions to learn
- ✅ Try multiple images

### **Don't:**
- ❌ Upload extremely large files
- ❌ Use blurry or dark images
- ❌ Expect 100% accuracy always
- ❌ Upload non-animal images
- ❌ Refresh during processing

---

## 🎓 Learning Resources

### **Understanding Results:**
- High confidence = Model is certain
- Low confidence = Model is unsure
- Top 3 shows alternatives
- Description provides context

### **Marine Biology:**
- Read descriptions carefully
- Learn about habitats
- Understand behaviors
- Discover conservation status

---

## 🆘 Need Help?

1. **Check README.md** - Full documentation
2. **Review troubleshooting** - Common issues
3. **Test with sample images** - Verify setup
4. **Check server logs** - Error messages

---

## 🎉 Quick Tips for Success

1. **Start Simple**: Try single image first
2. **Use Good Photos**: Clear, well-lit images
3. **Explore Features**: Try both tabs
4. **Read Descriptions**: Learn about animals
5. **Have Fun**: Experiment with different images!

---

**Ready to start? Open http://localhost:5000 and begin exploring! 🐠🌊**

---

**Last Updated:** Week 8  
**Version:** 1.0  
**Status:** ✅ Ready to Use