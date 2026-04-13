"""
Underwater Animal Detection with LLM Description
Final Version: CNN + Reliable Descriptions + Optional OpenAI
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json
import argparse
from datetime import datetime

# Try to import OpenAI (optional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not installed. Using fallback descriptions.")

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "week6_ModelTraining", "outputs", "mobilenet_model.h5")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
IMG_SIZE = 224

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Class Names
# -----------------------------
CLASS_NAMES = [
    "Clams", "Corals", "Crabs", "Dolphin", "Eel", "Fish",
    "Jelly Fish", "Lobster", "Nudibranchs", "Octopus", "Otter",
    "Penguin", "Puffers", "Sea Rays", "Sea Urchins", "Seahorse",
    "Seal", "Sharks", "Shrimp", "Squid", "Starfish",
    "Turtle_Tortoise", "Whale"
]

# -----------------------------
# Fallback Descriptions
# -----------------------------
FALLBACK_DESCRIPTIONS = {
    "Clams": "Clams are bivalve mollusks that filter feed by pumping water through their shells. They can live for decades, with some species living over 500 years. Clams burrow in sand or mud and are important filter feeders in marine ecosystems.",
    "Dolphin": "Dolphins are highly intelligent marine mammals known for their playful behavior and social structures. They use echolocation to hunt and navigate, and are found in oceans worldwide.",
    "Sharks": "Sharks are apex predators with excellent senses and over 500 species worldwide. They play a crucial role in maintaining marine ecosystem balance.",
    "Whale": "Whales are the largest animals on Earth and are known for their communication through songs and long migrations.",
    "Octopus": "Octopuses are highly intelligent creatures with eight arms and the ability to change color for camouflage.",
    "Jelly Fish": "Jellyfish are ancient marine animals with no brain or bones, using stinging tentacles to capture prey.",
    "Seahorse": "Seahorses are unique fish where males carry and give birth to offspring. They swim upright and live in shallow waters.",
    "Starfish": "Starfish can regenerate lost arms and move using tube feet along the ocean floor.",
    "Corals": "Corals form reef ecosystems that support marine biodiversity and are highly sensitive to climate change.",
    "Crabs": "Crabs are crustaceans with hard shells and claws, playing important roles in marine ecosystems.",
    "Fish": "Fish are diverse aquatic animals with gills and fins, essential to ocean ecosystems.",
    "Shrimp": "Shrimp are small crustaceans important in aquatic food chains.",
    "Squid": "Squid are fast-swimming cephalopods known for jet propulsion and ink defense.",
    "Seal": "Seals are marine mammals adapted for swimming and deep diving.",
    "Otter": "Sea otters use tools and have dense fur for insulation.",
    "Penguin": "Penguins are flightless birds adapted for swimming in cold waters.",
    "Eel": "Eels are elongated fish that can live in both freshwater and saltwater.",
    "Puffers": "Pufferfish can inflate themselves and contain toxic substances.",
    "Sea Rays": "Rays are flat-bodied fish that glide gracefully through water.",
    "Sea Urchins": "Sea urchins are spiny animals that feed on algae.",
    "Nudibranchs": "Nudibranchs are colorful sea slugs with unique defense mechanisms.",
    "Turtle_Tortoise": "Sea turtles are long-living marine reptiles that migrate long distances."
}

# -----------------------------
# Load Model
# -----------------------------
def load_cnn_model(model_path):
    if not os.path.exists(model_path):
        print(f"❌ Model not found at {model_path}")
        sys.exit(1)

    print(f"Loading CNN model from: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print("✅ CNN model loaded successfully!")
    return model

# -----------------------------
# Preprocess Image
# -----------------------------
def preprocess_image(img_path):
    if not os.path.exists(img_path):
        print(f"❌ Image not found at {img_path}")
        sys.exit(1)

    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# -----------------------------
# Prediction
# -----------------------------
def predict_animal(model, img_path):
    print(f"\n🔍 Analyzing: {img_path}")
    img = preprocess_image(img_path)

    preds = model.predict(img, verbose=0)
    idx = np.argmax(preds[0])

    return {
        "animal": CLASS_NAMES[idx],
        "confidence": float(preds[0][idx] * 100)
    }

# -----------------------------
# OpenAI Description (Optional)
# -----------------------------
def generate_description_openai(animal_name, api_key=None):
    if not OPENAI_AVAILABLE:
        return None

    try:
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Give a 3-4 sentence educational description of {animal_name}"
            }],
            max_tokens=150
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return None

# -----------------------------
# Description Logic
# -----------------------------
def get_description(animal_name, use_openai=False, api_key=None):
    print(f"\n🤖 Generating description for {animal_name}")

    if use_openai:
        desc = generate_description_openai(animal_name, api_key)
        if desc:
            print("✅ Using OpenAI")
            return desc

    print("✅ Using fallback description")
    return FALLBACK_DESCRIPTIONS.get(
        animal_name,
        f"{animal_name} are marine animals found in oceans and play important ecological roles."
    )

# -----------------------------
# Save Results
# -----------------------------
def save_results(prediction, description, img_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"result_{timestamp}"

    data = {
        "image": img_path,
        "prediction": prediction,
        "description": description
    }

    json_path = os.path.join(OUTPUT_DIR, filename + ".json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"💾 Saved: {json_path}")

# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--model", default=MODEL_PATH)
    parser.add_argument("--use_openai", action="store_true")
    parser.add_argument("--api_key", default=None)

    args = parser.parse_args()

    model = load_cnn_model(args.model)
    pred = predict_animal(model, args.image)
    desc = get_description(pred["animal"], args.use_openai, args.api_key)

    print("\n🎯 RESULT")
    print(f"Animal: {pred['animal']}")
    print(f"Confidence: {pred['confidence']:.2f}%")
    print(f"\n📖 Description:\n{desc}")

    save_results(pred, desc, args.image)

    print("\n✅ Done!")

if __name__ == "__main__":
    main()