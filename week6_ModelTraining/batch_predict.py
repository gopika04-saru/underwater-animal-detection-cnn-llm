"""
Batch Prediction Script for Multiple Images
Predicts animal classes for multiple images in a directory
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import pandas as pd
from tqdm import tqdm
import argparse

# -----------------------------
# Configuration
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "mobilenet_model.h5")
IMG_SIZE = 224

# Class names mapping
CLASS_NAMES = [
    "Clams", "Corals", "Crabs", "Dolphin", "Eel", "Fish",
    "Jelly Fish", "Lobster", "Nudibranchs", "Octopus", "Otter",
    "Penguin", "Puffers", "Sea Rays", "Sea Urchins", "Seahorse",
    "Seal", "Sharks", "Shrimp", "Squid", "Starfish",
    "Turtle_Tortoise", "Whale"
]

# -----------------------------
# Load Model
# -----------------------------
def load_model(model_path):
    """Load trained model"""
    if not os.path.exists(model_path):
        print(f"❌ Model not found: {model_path}")
        sys.exit(1)
    
    print(f"Loading model: {model_path}")
    model = tf.keras.models.load_model(model_path)
    print("✅ Model loaded!")
    return model

# -----------------------------
# Preprocess Image
# -----------------------------
def preprocess_image(img_path):
    """Preprocess single image"""
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# -----------------------------
# Batch Prediction
# -----------------------------
def batch_predict(model, image_dir, output_csv):
    """Predict for all images in directory"""
    
    # Get all image files
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp')
    image_files = [f for f in os.listdir(image_dir) 
                   if f.lower().endswith(valid_extensions)]
    
    if len(image_files) == 0:
        print(f"❌ No images found in {image_dir}")
        return
    
    print(f"\n🔍 Found {len(image_files)} images")
    print("Processing predictions...\n")
    
    results = []
    
    for img_file in tqdm(image_files):
        img_path = os.path.join(image_dir, img_file)
        
        try:
            # Preprocess and predict
            processed_img = preprocess_image(img_path)
            predictions = model.predict(processed_img, verbose=0)
            
            # Get top prediction
            predicted_idx = np.argmax(predictions[0])
            confidence = predictions[0][predicted_idx] * 100
            
            results.append({
                'image_name': img_file,
                'predicted_class': CLASS_NAMES[predicted_idx],
                'confidence': f"{confidence:.2f}%"
            })
            
        except Exception as e:
            print(f"⚠️ Error processing {img_file}: {str(e)}")
            results.append({
                'image_name': img_file,
                'predicted_class': 'ERROR',
                'confidence': '0.00%'
            })
    
    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)
    
    print(f"\n✅ Predictions completed!")
    print(f"💾 Results saved to: {output_csv}")
    
    # Display summary
    print("\n📊 Prediction Summary:")
    print(df['predicted_class'].value_counts())

# -----------------------------
# Main Function
# -----------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Batch predict underwater animals from images"
    )
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="Directory containing images"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="batch_predictions.csv",
        help="Output CSV file path"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=MODEL_PATH,
        help="Path to trained model"
    )
    
    args = parser.parse_args()
    
    # Load model
    model = load_model(args.model)
    
    # Batch predict
    batch_predict(model, args.input_dir, args.output)

if __name__ == "__main__":
    main()

# Made with Bob
