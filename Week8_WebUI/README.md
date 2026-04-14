# Week 8: Web UI for Underwater Animal Detection

## 📋 Overview
A modern, user-friendly web interface for the Underwater Animal Detection system. Upload single or multiple images to get instant CNN predictions with AI-generated descriptions.

---

## ✨ Features

### 🎯 Core Features
- **Single Image Upload**: Upload and analyze one image at a time
- **Bulk Upload**: Process multiple images simultaneously
- **Drag & Drop**: Easy file upload with drag-and-drop support
- **Real-time Results**: Instant predictions with confidence scores
- **AI Descriptions**: Educational descriptions powered by LLM
- **Beautiful UI**: Modern, responsive design with smooth animations

### 🤖 AI Integration
- **CNN Prediction**: 23 underwater animal classes
- **Confidence Scores**: Top-3 predictions with percentages
- **LLM Descriptions**: Choose between OpenAI GPT or curated descriptions
- **Image Preview**: See uploaded images with results

---

## 🚀 Quick Start

### **Step 1: Install Dependencies**

```bash
# Navigate to Week8_WebUI folder
cd Week8_WebUI

# Install Flask and dependencies
pip install flask werkzeug

# Or install from requirements file
pip install -r requirements_web.txt
```

### **Step 2: Ensure Model is Trained**

The web app requires a trained CNN model. If you haven't trained one yet:

```bash
cd ../week6_ModelTraining
python train_mobilenet.py
```

This will create `mobilenet_model.h5` in the `outputs` folder.

### **Step 3: Run the Web Application**

```bash
cd Week8_WebUI
python app.py
```

### **Step 4: Open in Browser**

Open your web browser and go to:
```
http://localhost:5000
```

---

## 💻 Usage Guide

### **Single Image Upload**

1. Click on the **"📷 Single Image"** tab
2. Click the upload area or drag & drop an image
3. (Optional) Check "Use OpenAI GPT" for AI-generated descriptions
4. Click **"🔍 Analyze Image"**
5. View results with prediction and description

### **Bulk Upload**

1. Click on the **"📁 Bulk Upload"** tab
2. Click the upload area or drag & drop multiple images
3. (Optional) Check "Use OpenAI GPT" for AI-generated descriptions
4. Review the file list (you can remove files)
5. Click **"🔍 Analyze All Images"**
6. View results for all images

---

## 🎨 UI Features

### **Modern Design**
- Gradient backgrounds
- Smooth animations
- Responsive layout
- Mobile-friendly

### **Interactive Elements**
- Drag-and-drop file upload
- Progress indicators
- Visual confidence bars
- Expandable results

### **User Experience**
- Clear error messages
- Loading states
- File size validation
- Format validation

---

## 🔧 Configuration

### **File Upload Settings**

Edit `app.py` to customize:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}
```

### **Model Path**

By default, the app looks for the model at:
```
../week6_ModelTraining/outputs/mobilenet_model.h5
```

To use a different model, edit `MODEL_PATH` in `app.py`:
```python
MODEL_PATH = "path/to/your/model.h5"
```

### **OpenAI API Key**

To use OpenAI GPT for descriptions:

```bash
# Set environment variable
export OPENAI_API_KEY="sk-your-key-here"

# Or add to ~/.bashrc for permanent setup
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

---

## 📁 Project Structure

```
Week8_WebUI/
├── app.py                      # Flask backend application
├── requirements_web.txt        # Web dependencies
├── README.md                   # This file
├── templates/
│   └── index.html             # Frontend HTML/CSS/JavaScript
├── uploads/                   # Uploaded images (auto-created)
└── results/                   # Processing results (auto-created)
```

---

## 🌐 API Endpoints

### **POST /predict**
Predict single image

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: 
  - `file`: Image file
  - `use_openai`: Boolean (optional)

**Response:**
```json
{
  "success": true,
  "prediction": {
    "animal": "Dolphin",
    "confidence": 94.32,
    "top_predictions": [...]
  },
  "description": "Dolphins are...",
  "description_source": "openai",
  "image": "base64_encoded_image"
}
```

### **POST /predict_bulk**
Predict multiple images

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body:
  - `files[]`: Multiple image files
  - `use_openai`: Boolean (optional)

**Response:**
```json
{
  "success": true,
  "total": 5,
  "results": [...]
}
```

### **GET /health**
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "openai_available": false
}
```

---

## 🎯 Supported Image Formats

- **JPG/JPEG**: Standard JPEG images
- **PNG**: Portable Network Graphics
- **BMP**: Bitmap images

**Maximum file size:** 16 MB per image

---

## 🔍 How It Works

### **Backend Flow:**

1. **Upload**: User uploads image(s) via web interface
2. **Validation**: Check file format and size
3. **Save**: Store uploaded files temporarily
4. **Preprocess**: Resize to 224x224, normalize pixels
5. **CNN Prediction**: Run through trained model
6. **LLM Description**: Generate or retrieve description
7. **Response**: Send results back to frontend
8. **Display**: Show results with image and description

### **Frontend Flow:**

1. **File Selection**: User selects files via click or drag-drop
2. **Preview**: Display selected files
3. **Submit**: Send files to backend via AJAX
4. **Loading**: Show spinner during processing
5. **Results**: Display predictions with animations
6. **Interaction**: User can analyze more images

---

## 🎨 Customization

### **Change Colors**

Edit the CSS in `templates/index.html`:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Change to your colors */
background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
```

### **Modify Layout**

The UI uses flexbox and is fully responsive. Edit the HTML structure in `templates/index.html`.

### **Add Features**

Extend `app.py` to add new endpoints or functionality:

```python
@app.route('/your-endpoint', methods=['POST'])
def your_function():
    # Your code here
    return jsonify({'result': 'success'})
```

---

## 🐛 Troubleshooting

### **Issue 1: Model Not Found**
```
❌ Error: Model not found at outputs/mobilenet_model.h5
```

**Solution:**
```bash
cd week6_ModelTraining
python train_mobilenet.py
```

### **Issue 2: Port Already in Use**
```
Address already in use
```

**Solution:**
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### **Issue 3: Import Error**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
pip install flask werkzeug
```

### **Issue 4: Large File Upload Fails**
```
413 Request Entity Too Large
```

**Solution:**
Increase max file size in `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
```

### **Issue 5: OpenAI API Error**
```
⚠️ OpenAI API error: Authentication failed
```

**Solution:**
- Check API key is set: `echo $OPENAI_API_KEY`
- Verify key is valid on OpenAI platform
- Use fallback descriptions (uncheck OpenAI option)

---

## 🚀 Deployment

### **Local Network Access**

To access from other devices on your network:

```python
# In app.py, change host to 0.0.0.0
app.run(debug=False, host='0.0.0.0', port=5000)
```

Then access via: `http://your-ip-address:5000`

### **Production Deployment**

For production, use a WSGI server like Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Docker Deployment**

Create a `Dockerfile`:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t underwater-detection .
docker run -p 5000:5000 underwater-detection
```

---

## 📊 Performance

### **Response Times:**
- Single image: ~1-2 seconds
- Bulk (5 images): ~5-8 seconds
- With OpenAI: +1-2 seconds per image

### **Optimization Tips:**
1. Use GPU for faster CNN inference
2. Cache LLM descriptions
3. Implement image compression
4. Use async processing for bulk uploads
5. Add Redis for session management

---

## 🎓 Technical Stack

### **Backend:**
- **Flask**: Web framework
- **TensorFlow/Keras**: CNN model inference
- **OpenAI API**: LLM descriptions (optional)
- **Pillow**: Image processing
- **NumPy**: Numerical operations

### **Frontend:**
- **HTML5**: Structure
- **CSS3**: Styling with gradients and animations
- **JavaScript**: Interactivity and AJAX
- **Fetch API**: HTTP requests

---

## 📝 Example Usage

### **Python API Client:**

```python
import requests

# Single image prediction
with open('dolphin.jpg', 'rb') as f:
    files = {'file': f}
    data = {'use_openai': 'false'}
    response = requests.post('http://localhost:5000/predict', 
                           files=files, data=data)
    result = response.json()
    print(f"Predicted: {result['prediction']['animal']}")
```

### **cURL:**

```bash
# Single image
curl -X POST -F "file=@dolphin.jpg" -F "use_openai=false" \
  http://localhost:5000/predict

# Health check
curl http://localhost:5000/health
```

---

## ✅ Features Checklist

- [x] Single image upload
- [x] Bulk image upload
- [x] Drag and drop support
- [x] CNN prediction integration
- [x] LLM description generation
- [x] OpenAI GPT support
- [x] Fallback descriptions
- [x] Responsive design
- [x] Error handling
- [x] Loading states
- [x] Image preview
- [x] Confidence visualization
- [x] Top-K predictions
- [x] File validation
- [x] Mobile-friendly UI

---

## 🔄 Future Enhancements

- [ ] User authentication
- [ ] Save prediction history
- [ ] Export results to PDF
- [ ] Real-time video detection
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Advanced filters
- [ ] Comparison view
- [ ] Social sharing
- [ ] API rate limiting

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the main project README
3. Check Flask documentation: https://flask.palletsprojects.com/

---

## 🎉 Success!

Your web UI is now ready! Users can:
- Upload underwater animal images
- Get instant AI predictions
- Read educational descriptions
- Process multiple images at once

**Enjoy your underwater animal detection web application! 🐠🌊**

---

**Last Updated:** Week 8  
**Status:** ✅ Complete and Ready to Use  
**Technology:** Flask + TensorFlow + OpenAI (optional)