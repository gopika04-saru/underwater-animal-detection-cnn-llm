"""
Underwater Animal Detection Web Application
Flask-based UI for single and bulk image upload with CNN + LLM integration
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from datetime import datetime
import json
import base64
from io import BytesIO
from PIL import Image

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import OpenAI (optional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# -----------------------------
# Configuration
# -----------------------------
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp'}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "week6_ModelTraining", "outputs", "mobilenet_model.h5")
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')

# Create necessary folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

IMG_SIZE = 224

# Class names mapping
CLASS_NAMES = [
    "Clams", "Corals", "Crabs", "Dolphin", "Eel", "Fish",
    "Jelly Fish", "Lobster", "Nudibranchs", "Octopus", "Otter",
    "Penguin", "Puffers", "Sea Rays", "Sea Urchins", "Seahorse",
    "Seal", "Sharks", "Shrimp", "Squid", "Starfish",
    "Turtle_Tortoise", "Whale"
]

# Fallback descriptions
FALLBACK_DESCRIPTIONS = {
    "Dolphin": "Dolphins are highly intelligent marine mammals known for their playful behavior and complex social structures. They use echolocation to navigate and hunt, and can swim at speeds up to 20 mph. Found in oceans worldwide, dolphins are known for their acrobatic displays and friendly interactions with humans.",
    "Sharks": "Sharks are apex predators that have existed for over 400 million years. They have excellent senses including the ability to detect electrical fields. With over 500 species, sharks play a crucial role in maintaining marine ecosystem balance. Most species are harmless to humans.",
    "Turtle_Tortoise": "Sea turtles are ancient mariners that have been swimming the oceans for over 100 million years. They can hold their breath for hours and migrate thousands of miles. Seven species exist today, all facing conservation challenges. They play important roles in marine ecosystems.",
    "Whale": "Whales are the largest animals on Earth, with blue whales reaching up to 100 feet long. These marine mammals are known for their complex songs and social behaviors. They play crucial roles in ocean ecosystems and can live for decades, with some species living over 100 years.",
    "Octopus": "Octopuses are highly intelligent invertebrates with eight arms and three hearts. They can change color and texture instantly for camouflage, squeeze through tiny spaces, and use tools. Known for their problem-solving abilities, they are masters of escape and disguise.",
    "Jelly Fish": "Jellyfish are ancient creatures that have existed for over 500 million years. They have no brain, heart, or bones, yet are efficient predators. Their tentacles contain stinging cells for capturing prey. Some species are bioluminescent, creating beautiful light displays.",
    "Seahorse": "Seahorses are unique fish where males carry and give birth to babies. They swim upright using their dorsal fin and can change color to match their surroundings. Found in shallow coastal waters, they use their prehensile tail to anchor to seagrass and coral.",
    "Starfish": "Starfish (sea stars) are echinoderms with remarkable regenerative abilities - they can regrow lost arms. They have no brain or blood, using seawater for circulation. With tube feet on their underside, they move slowly across the ocean floor hunting for prey.",
    "Corals": "Corals are colonial animals that build massive reef structures providing habitat for 25% of marine species. They have a symbiotic relationship with algae that gives them color and energy. Coral reefs are among Earth's most diverse ecosystems but are threatened by climate change.",
    "Crabs": "Crabs are crustaceans with a hard exoskeleton and ten legs, including two claws. They walk sideways and can regenerate lost limbs. Found in all oceans, they play important roles as scavengers and prey. Over 6,800 species exist worldwide.",
    "Lobster": "Lobsters are large marine crustaceans with powerful claws and long bodies. They can live for over 100 years and continue growing throughout their lives. Lobsters are bottom-dwellers that hunt at night and are considered a delicacy in many cultures.",
    "Shrimp": "Shrimp are small crustaceans found in both fresh and saltwater. They are important in marine food chains and come in over 2,000 species. Some species can create loud snapping sounds with their claws, while others clean parasites from fish.",
    "Squid": "Squid are cephalopods with eight arms and two longer tentacles. They can change color rapidly, shoot ink for defense, and swim by jet propulsion. Some species can grow to enormous sizes, with giant squid reaching over 40 feet long.",
    "Seal": "Seals are marine mammals that spend time both in water and on land. They are excellent swimmers with streamlined bodies and can dive deep for extended periods. Seals are social animals often found in large colonies on beaches and ice.",
    "Otter": "Sea otters are marine mammals known for using tools to crack open shellfish. They have the densest fur of any animal, with up to 1 million hairs per square inch. Otters are playful, social animals that float on their backs and hold hands while sleeping.",
    "Penguin": "Penguins are flightless birds perfectly adapted for swimming. They can dive deep and hold their breath for extended periods. Living primarily in the Southern Hemisphere, penguins are social birds that form large colonies and mate for life.",
    "Eel": "Eels are elongated fish found in both fresh and saltwater. Some species can generate electric shocks for hunting and defense. They have a complex life cycle, often migrating thousands of miles to spawn. Moray eels are common reef dwellers.",
    "Fish": "Fish are diverse aquatic vertebrates with over 30,000 species. They breathe through gills, have fins for swimming, and come in countless shapes, sizes, and colors. Fish play crucial roles in marine ecosystems as both predators and prey.",
    "Puffers": "Pufferfish can inflate their bodies to several times their normal size when threatened. Many species contain tetrodotoxin, one of the most potent toxins in nature. Despite this, they are considered a delicacy in some cultures when prepared by trained chefs.",
    "Sea Rays": "Rays are flat-bodied fish related to sharks. They glide gracefully through water using wing-like pectoral fins. Some species have venomous barbs for defense. Manta rays are the largest, reaching wingspans of over 20 feet.",
    "Sea Urchins": "Sea urchins are spiny echinoderms that graze on algae and kelp. Their spines provide protection from predators. They move slowly using tube feet and play important roles in controlling algae growth. Some species are harvested for their roe.",
    "Clams": "Clams are bivalve mollusks that filter feed by pumping water through their shells. They can live for decades, with some species living over 500 years. Clams burrow in sand or mud and are important filter feeders in marine ecosystems.",
    "Nudibranchs": "Nudibranchs are colorful sea slugs known as the 'butterflies of the sea.' They come in stunning colors and patterns, often as warning signals of toxicity. These shell-less mollusks can incorporate stinging cells from their prey for their own defense."
}

# Global model variable
model = None

# -----------------------------
# Helper Functions
# -----------------------------
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_model():
    """Load the CNN model"""
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please train the model first.")
        print(f"Loading model from: {MODEL_PATH}")
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Model loaded successfully!")
    return model

def preprocess_image(img_path):
    """Preprocess image for CNN prediction"""
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_animal(img_path, top_k=3):
    """Predict animal class using CNN"""
    model = load_model()
    processed_img = preprocess_image(img_path)
    predictions = model.predict(processed_img, verbose=0)
    
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx] * 100
    predicted_animal = CLASS_NAMES[predicted_class_idx]
    
    top_indices = np.argsort(predictions[0])[-top_k:][::-1]
    
    return {
        "animal": predicted_animal,
        "confidence": float(confidence),
        "top_predictions": [
            {
                "class": CLASS_NAMES[idx],
                "confidence": float(predictions[0][idx] * 100)
            }
            for idx in top_indices
        ]
    }

def generate_description_openai(animal_name, api_key=None):
    """Generate description using OpenAI GPT"""
    if not OPENAI_AVAILABLE:
        return None
    
    try:
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""Provide a detailed, educational description of {animal_name} in 3-4 sentences. 
Include information about:
1. Physical characteristics
2. Habitat and behavior
3. Interesting facts
4. Conservation status (if relevant)

Keep it informative and engaging for general audience."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a marine biology expert providing educational information about underwater animals."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"⚠️ OpenAI API error: {str(e)}")
        return None

def get_animal_description(animal_name, use_openai=False):
    """Get description for the detected animal"""
    # Try OpenAI if requested
    if use_openai and OPENAI_AVAILABLE:
        description = generate_description_openai(animal_name)
        if description:
            return description, "openai"
    
    # Fallback to pre-written descriptions
    description = FALLBACK_DESCRIPTIONS.get(animal_name, 
        f"{animal_name} is a fascinating marine creature found in underwater environments. "
        f"These animals play important roles in ocean ecosystems and exhibit unique adaptations "
        f"for life in aquatic habitats.")
    
    return description, "fallback"

def image_to_base64(img_path):
    """Convert image to base64 for display"""
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle single image prediction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, bmp'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Get prediction
        prediction = predict_animal(filepath)
        
        # Get description
        use_openai = request.form.get('use_openai', 'false').lower() == 'true'
        description, desc_source = get_animal_description(prediction['animal'], use_openai)
        
        # Convert image to base64
        img_base64 = image_to_base64(filepath)
        
        result = {
            'success': True,
            'prediction': prediction,
            'description': description,
            'description_source': desc_source,
            'image': img_base64,
            'filename': filename
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_bulk', methods=['POST'])
def predict_bulk():
    """Handle bulk image prediction"""
    try:
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        files = request.files.getlist('files[]')
        
        if len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        use_openai = request.form.get('use_openai', 'false').lower() == 'true'
        
        for file in files:
            if file and allowed_file(file.filename):
                # Save file
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                
                try:
                    # Get prediction
                    prediction = predict_animal(filepath)
                    
                    # Get description
                    description, desc_source = get_animal_description(prediction['animal'], use_openai)
                    
                    # Convert image to base64
                    img_base64 = image_to_base64(filepath)
                    
                    results.append({
                        'success': True,
                        'filename': file.filename,
                        'prediction': prediction,
                        'description': description,
                        'description_source': desc_source,
                        'image': img_base64
                    })
                
                except Exception as e:
                    results.append({
                        'success': False,
                        'filename': file.filename,
                        'error': str(e)
                    })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        model_loaded = model is not None
        return jsonify({
            'status': 'healthy',
            'model_loaded': model_loaded,
            'openai_available': OPENAI_AVAILABLE
        })
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

# -----------------------------
# Main
# -----------------------------
if __name__ == '__main__':
    print("🐠 Starting Underwater Animal Detection Web App...")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"🧠 Model path: {MODEL_PATH}")
    
    # Load model on startup
    try:
        load_model()
    except Exception as e:
        print(f"⚠️ Warning: Could not load model: {e}")
        print("Please train the model first using train_mobilenet.py")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
