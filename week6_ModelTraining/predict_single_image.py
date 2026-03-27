"""
Underwater Animal Detection - Single Image Prediction Script
This script loads a trained model and predicts the animal class for a single input image.
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import json
import argparse

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "mobilenet_model.h5")
IMG_SIZE = 224

# Class names mapping (23 underwater animals)
CLASS_NAMES = [
    "Clams",
    "Corals", 
    "Crabs",
    "Dolphin",
    "Eel",
    "Fish",
    "Jelly Fish",
    "Lobster",
    "Nudibranchs",
    "Octopus",
    "Otter",
    "Penguin",
    "Puffers",
    "Sea Rays",
    "Sea Urchins",
    "Seahorse",
    "Seal",
    "Sharks",
    "Shrimp",
    "Squid",
    "Starfish",
    "Turtle_Tortoise",
    "Whale"
]

# -----------------------------
# Load Model
# -----------------------------
def load_model(model_path):
    """Load the trained model"""
    if not os.path.exists(model_path):
        print(f"❌ Error: Model not found at {model_path}")
        print("Please train a model first using train_mobilenet.py or train_cnn_model.py")
        sys.exit(1)
    
    print(f"Loading model from: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print("✅ Model loaded successfully!")
    return model

# -----------------------------
# Preprocess Image
# -----------------------------
def preprocess_image(img_path, img_size=224):
    """Load and preprocess image for prediction"""
    if not os.path.exists(img_path):
        print(f"❌ Error: Image not found at {img_path}")
        sys.exit(1)
    
    # Load image
    img = image.load_img(img_path, target_size=(img_size, img_size))
    
    # Convert to array
    img_array = image.img_to_array(img)
    
    # Normalize pixel values (0-1)
    img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

# -----------------------------
# Make Prediction
# -----------------------------
def predict_animal(model, img_path, top_k=3):
    """Predict animal class for input image"""
    
    print(f"\n🔍 Analyzing image: {img_path}")
    
    # Preprocess image
    processed_img = preprocess_image(img_path, IMG_SIZE)
    
    # Make prediction
    predictions = model.predict(processed_img, verbose=0)
    
    # Get predicted class
    predicted_class_idx = np.argmax(predictions[0])
    confidence = predictions[0][predicted_class_idx] * 100
    
    # Get top K predictions
    top_indices = np.argsort(predictions[0])[-top_k:][::-1]
    
    # Display results
    print("\n" + "="*60)
    print("🐠 PREDICTION RESULTS")
    print("="*60)
    print(f"\n🎯 Predicted Animal: {CLASS_NAMES[predicted_class_idx]}")
    print(f"📊 Confidence: {confidence:.2f}%")
    
    print(f"\n📈 Top {top_k} Predictions:")
    print("-" * 60)
    for i, idx in enumerate(top_indices, 1):
        animal_name = CLASS_NAMES[idx]
        conf = predictions[0][idx] * 100
        bar = "█" * int(conf / 2)
        print(f"{i}. {animal_name:<20} {conf:>6.2f}% {bar}")
    
    print("="*60 + "\n")
    
    return {
        "predicted_class": CLASS_NAMES[predicted_class_idx],
        "confidence": float(confidence),
        "top_predictions": [
            {
                "class": CLASS_NAMES[idx],
                "confidence": float(predictions[0][idx] * 100)
            }
            for idx in top_indices
        ]
    }

# -----------------------------
# Save Prediction Results
# -----------------------------
def save_results(results, output_path):
    """Save prediction results to JSON file"""
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"💾 Results saved to: {output_path}")

# -----------------------------
# Main Function
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Predict underwater animal from image using trained CNN model"
    )
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to input image"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=MODEL_PATH,
        help="Path to trained model (default: outputs/mobilenet_model.h5)"
    )
    parser.add_argument(
        "--top_k",
        type=int,
        default=3,
        help="Number of top predictions to show (default: 3)"
    )
    parser.add_argument(
        "--save",
        type=str,
        default=None,
        help="Path to save prediction results as JSON"
    )
    
    args = parser.parse_args()
    
    # Load model
    model = load_model(args.model)
    
    # Make prediction
    results = predict_animal(model, args.image, args.top_k)
    
    # Save results if requested
    if args.save:
        save_results(results, args.save)
    
    print("✅ Prediction completed successfully!")

# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()

# Made with Bob
