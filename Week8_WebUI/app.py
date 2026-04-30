"""
Underwater Animal Detection Web Application
Flask-based UI for single and bulk image upload with CNN + Gemini LLM integration
"""

import os
import sys
import csv
import io
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from datetime import datetime
import json
import base64
from PIL import Image

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import Google Generative AI (Gemini)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Try to import OpenAI (optional fallback)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# -----------------------------
# Configuration
# -----------------------------
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64MB max (for bulk)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "week6_ModelTraining", "outputs", "mobilenet_model.h5")
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')

# Create necessary folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

IMG_SIZE = 224

# Class names mapping (23 underwater animals)
CLASS_NAMES = [
    "Clams", "Corals", "Crabs", "Dolphin", "Eel", "Fish",
    "Jelly Fish", "Lobster", "Nudibranchs", "Octopus", "Otter",
    "Penguin", "Puffers", "Sea Rays", "Sea Urchins", "Seahorse",
    "Seal", "Sharks", "Shrimp", "Squid", "Starfish",
    "Turtle_Tortoise", "Whale"
]

# Fallback descriptions for all 23 classes
FALLBACK_DESCRIPTIONS = {
    "Dolphin": "Dolphins are highly intelligent marine mammals known for their playful behavior and complex social structures. They use echolocation to navigate and hunt, and can swim at speeds up to 20 mph. Found in oceans worldwide, dolphins are recognized for their acrobatic displays and friendly interactions with humans. Conservation status: Least Concern (most species).",
    "Sharks": "Sharks are apex predators that have existed for over 400 million years, predating even dinosaurs. They have extraordinary senses including electroreception to detect prey. With over 500 species ranging from the tiny dwarf lanternshark to the massive whale shark, they are vital to marine ecosystem balance.",
    "Turtle_Tortoise": "Sea turtles are ancient mariners that have been swimming the oceans for over 100 million years. They can hold their breath for several hours and migrate thousands of miles between feeding and nesting grounds. All 7 living sea turtle species are classified as vulnerable to critically endangered.",
    "Whale": "Whales are the largest animals on Earth — blue whales can reach 100 feet and weigh 200 tons. These marine mammals communicate through complex songs spanning hundreds of miles. They play a critical role in ocean carbon cycling, and their dives can exceed 3,000 meters depth.",
    "Octopus": "Octopuses are among the most intelligent invertebrates, with three hearts and blue copper-based blood. Their eight arms contain two-thirds of their neurons, enabling independent movement. Masters of camouflage, they can change skin color and texture in milliseconds.",
    "Jelly Fish": "Jellyfish are 95% water and have existed for over 500 million years — longer than dinosaurs. They have no brain, heart, or bones yet are efficient predators. The immortal jellyfish (Turritopsis dohrnii) can revert to its juvenile form, potentially making it biologically immortal.",
    "Seahorse": "Seahorses are the only animal where males become pregnant and give birth. They are monogamous, greeting their partner daily with a color-changing dance. Despite being poor swimmers, they anchor to coral with their prehensile tails and are masters of ambush hunting.",
    "Starfish": "Sea stars (starfish) are echinoderms capable of regenerating entire lost arms — sometimes a severed arm can regenerate a whole new body. They have no brain or blood; seawater circulates through their hydraulic system. They are keystone predators in intertidal ecosystems.",
    "Corals": "Corals are colonial animals — not plants — that build massive calcium carbonate reef structures. They host zooxanthellae algae in a symbiotic relationship providing 90% of their energy. Coral reefs cover less than 1% of the ocean floor but support 25% of all marine species.",
    "Crabs": "Crabs are crustaceans that walk sideways due to the structure of their legs. They can regenerate lost claws and communicate by waving and drumming. Hermit crabs borrow shells for protection, and some species use tools like sea anemones for defense.",
    "Lobster": "Lobsters are believed to be functionally immortal — they don't weaken or lose fertility with age due to telomerase enzyme activity. They can live over 100 years and continue growing. Their blue blood contains hemocyanin, which turns blue-green when oxygenated.",
    "Shrimp": "Shrimp are vital to marine food webs and come in over 2,000 species. Pistol shrimp can snap claws faster than a bullet, creating cavitation bubbles hotter than the sun's surface. Cleaner shrimp set up 'cleaning stations' removing parasites from fish.",
    "Squid": "Squid are cephalopods with excellent vision — some species have the largest eyes in the animal kingdom. They swim via jet propulsion and can release ink clouds as decoys. The colossal squid, found in Antarctic waters, is the largest invertebrate on Earth.",
    "Seal": "Seals are pinnipeds that converted from land-dwelling ancestors over 23 million years ago. They can dive to 1,500 meters and hold their breath for over 2 hours. Their whiskers are highly sensitive, capable of detecting fish movements from 30 seconds earlier.",
    "Otter": "Sea otters have the densest fur of any animal — up to 1 million hairs per square inch — trapping air for insulation instead of blubber. They are keystone species in kelp forest ecosystems, controlling sea urchin populations. They famously hold hands while sleeping to avoid drifting apart.",
    "Penguin": "Penguins are flightless birds whose wings evolved into flippers for swimming. They can dive to 500 meters and reach speeds of 25 mph underwater. Emperor penguins withstand Antarctic winters at -60°C by huddling in rotating groups. They recognize their mates by call among thousands.",
    "Eel": "Eels are elongated fish making extraordinary migrations — European eels travel 6,000 km to the Sargasso Sea to spawn, then die. Electric eels generate 600-volt shocks to stun prey. Moray eels have a second set of jaws (pharyngeal jaws) that shoot forward to grab prey.",
    "Fish": "Fish are the most diverse group of vertebrates with over 34,000 described species. They were the first vertebrates on Earth, appearing 530 million years ago. Some fish like the mudskipper can walk on land, and the climbing perch can remain out of water for extended periods.",
    "Puffers": "Pufferfish are the second most poisonous vertebrate — their organs contain tetrodotoxin, 1,200 times more toxic than cyanide. They rapidly inflate by swallowing water or air as a defense mechanism. In Japan, fugu prepared by licensed chefs is a luxury dish despite the lethal risk.",
    "Sea Rays": "Rays are cartilaginous fish closely related to sharks. Manta rays, the largest, have wingspans exceeding 7 meters and are filter feeders. Electric rays can generate shocks up to 220 volts. Rays navigate using the Earth's magnetic field during long ocean migrations.",
    "Sea Urchins": "Sea urchins are echinoderms whose spines can deliver painful puncture wounds. Their mouth, called Aristotle's lantern, is a complex jaw structure with five self-sharpening teeth. They are ecological indicators — overgrazing by urchins when predators are removed destroys kelp forests.",
    "Clams": "Clams are bivalve mollusks that filter feed up to 50 pints of water per day. The ocean quahog clam (Arctica islandica) can live over 500 years, making it one of the longest-lived animals. Giant clams can reach 4 feet and weigh 500 pounds.",
    "Nudibranchs": "Nudibranchs are shell-less sea slugs often called 'butterflies of the sea' for their vibrant colors. They can incorporate stinging nematocysts from jellyfish prey into their own skin for defense. Over 3,000 species exist, and many are toxic — their bright colors serve as aposematic warnings."
}

# Global model variable
model = None
last_bulk_results = []  # Store last bulk results for CSV download

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
    mdl = load_model()
    processed_img = preprocess_image(img_path)
    predictions = mdl.predict(processed_img, verbose=0)

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

def generate_description_gemini(animal_name, api_key=None):
    """Generate educational description using Google Gemini API"""
    if not GEMINI_AVAILABLE:
        return None

    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        return None

    try:
        genai.configure(api_key=key)
        
        # Dynamically find a supported model for this API key
        chosen_model = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                chosen_model = m.name
                if 'flash' in m.name.lower():  # Prefer flash if available
                    break
                    
        if not chosen_model:
            return "⚠️ Gemini API Error: No compatible text generation models found for this API key. Make sure the Generative Language API is enabled."

        gemini_model = genai.GenerativeModel(chosen_model)

        prompt = f"""You are a marine biology expert. Provide a concise yet fascinating educational description of {animal_name} in 3-4 sentences.
Include:
1. One striking physical characteristic
2. A unique behavior or adaptation
3. Its role in the marine ecosystem
4. A surprising or little-known fact

Make it engaging and educational for a general audience. Do NOT use markdown formatting."""

        response = gemini_model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        error_msg = f"⚠️ Gemini API Error: {str(e)}"
        print(error_msg)
        return error_msg

def generate_description_openai(animal_name, api_key=None):
    """Generate description using OpenAI GPT (fallback)"""
    if not OPENAI_AVAILABLE:
        return None

    try:
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        prompt = f"Provide a 3-4 sentence educational description of {animal_name} covering physical traits, behavior, and an interesting fact. No markdown."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a marine biology expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ OpenAI API error: {str(e)}")
        return None

def get_animal_description(animal_name, use_llm=False, gemini_key=None, openai_key=None):
    """Get description for the detected animal — tries Gemini first, then OpenAI, then fallback"""
    if use_llm:
        # Try Gemini first
        description = generate_description_gemini(animal_name, gemini_key)
        if description:
            return description, "gemini"

        # Try OpenAI as secondary
        description = generate_description_openai(animal_name, openai_key)
        if description:
            return description, "openai"

    # Fallback to curated descriptions
    description = FALLBACK_DESCRIPTIONS.get(
        animal_name,
        f"{animal_name} is a fascinating marine creature found in underwater environments. "
        f"These animals play important roles in ocean ecosystems and exhibit unique adaptations "
        f"for life in aquatic habitats."
    )
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
    return render_template('index.html',
                           gemini_available=GEMINI_AVAILABLE,
                           openai_available=OPENAI_AVAILABLE)

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
            return jsonify({'error': 'Invalid file type. Allowed: png, jpg, jpeg, bmp, gif, webp'}), 400

        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Get prediction
        prediction = predict_animal(filepath)

        # Get description
        use_llm = request.form.get('use_llm', 'false').lower() == 'true'
        gemini_key = request.form.get('gemini_key', '').strip() or None
        openai_key = request.form.get('openai_key', '').strip() or None
        description, desc_source = get_animal_description(prediction['animal'], use_llm, gemini_key, openai_key)

        # Convert image to base64
        img_base64 = image_to_base64(filepath)

        return jsonify({
            'success': True,
            'prediction': prediction,
            'description': description,
            'description_source': desc_source,
            'image': img_base64,
            'filename': filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_bulk', methods=['POST'])
def predict_bulk():
    """Handle bulk image prediction"""
    global last_bulk_results
    try:
        files = request.files.getlist('files[]')

        # fallback if frontend uses wrong name
        if not files:
            files = request.files.getlist('file')

        if not files:
            return jsonify({'error': 'No files uploaded'}), 400
        print("DEBUG: Files received =", len(files))
        if len(files) == 0:
            return jsonify({'error': 'No files selected'}), 400

        results = []
        use_llm = request.form.get('use_llm', 'false').lower() == 'true'
        gemini_key = request.form.get('gemini_key', '').strip() or None
        openai_key = request.form.get('openai_key', '').strip() or None

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                saved_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, saved_filename)
                file.save(filepath)

                try:
                    prediction = predict_animal(filepath)
                    description, desc_source = get_animal_description(
                        prediction['animal'], use_llm, gemini_key, openai_key
                    )
                    img_base64 = image_to_base64(filepath)

                    results.append({
                        'success': True,
                        'filename': file.filename,
                        'prediction': prediction,
                        'description': description,
                        'description_source': desc_source,
                        'image': img_base64,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

                except Exception as e:
                    results.append({
                        'success': False,
                        'filename': file.filename,
                        'error': str(e),
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            else:
                results.append({
                    'success': False,
                    'filename': file.filename if file else 'unknown',
                    'error': 'Invalid file type',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        # Cache results for CSV download
        last_bulk_results = results

        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': sum(1 for r in results if r['success']),
            'failed': sum(1 for r in results if not r['success'])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download_csv', methods=['GET'])
def download_csv():
    """Download bulk prediction results as CSV"""
    global last_bulk_results

    if not last_bulk_results:
        return jsonify({'error': 'No results to download. Run bulk prediction first.'}), 400

    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'Filename', 'Predicted Animal', 'Confidence (%)',
        'Top 2 Prediction', 'Top 2 Confidence (%)',
        'Top 3 Prediction', 'Top 3 Confidence (%)',
        'Description', 'Description Source', 'Timestamp', 'Status'
    ])

    for r in last_bulk_results:
        if r['success']:
            pred = r['prediction']
            top = pred['top_predictions']
            writer.writerow([
                r['filename'],
                pred['animal'],
                f"{pred['confidence']:.2f}",
                top[1]['class'] if len(top) > 1 else '',
                f"{top[1]['confidence']:.2f}" if len(top) > 1 else '',
                top[2]['class'] if len(top) > 2 else '',
                f"{top[2]['confidence']:.2f}" if len(top) > 2 else '',
                r.get('description', ''),
                r.get('description_source', ''),
                r.get('timestamp', ''),
                'Success'
            ])
        else:
            writer.writerow([
                r['filename'], '', '', '', '', '', '',
                r.get('error', 'Unknown error'), '', r.get('timestamp', ''), 'Failed'
            ])

    output.seek(0)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=underwater_detection_{timestamp}.csv'
        }
    )


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'model_path_exists': os.path.exists(MODEL_PATH),
        'gemini_available': GEMINI_AVAILABLE,
        'openai_available': OPENAI_AVAILABLE,
        'classes': len(CLASS_NAMES)
    })


# -----------------------------
# Main
# -----------------------------
if __name__ == '__main__':
    print("🐠 Starting Underwater Animal Detection Web App...")
    print(f"📁 Upload folder: {UPLOAD_FOLDER}")
    print(f"🧠 Model path: {MODEL_PATH}")
    print(f"🤖 Gemini available: {GEMINI_AVAILABLE}")
    print(f"🤖 OpenAI available: {OPENAI_AVAILABLE}")

    # Load model on startup
    try:
        load_model()
    except Exception as e:
        print(f"⚠️ Warning: Could not load model: {e}")
        print("Please train the model first using train_mobilenet.py")

    app.run(debug=True, host='0.0.0.0', port=5000)
