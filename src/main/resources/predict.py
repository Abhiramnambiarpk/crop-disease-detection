import sys
import os
import warnings
from pathlib import Path

# Suppress all warnings and TensorFlow messages before importing
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow info, warnings, and errors
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN to avoid messages
warnings.filterwarnings('ignore')  # Suppress Python warnings

# Suppress stderr for TensorFlow imports
_stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

import tensorflow as tf
import numpy as np

# Restore stderr
sys.stderr.close()
sys.stderr = _stderr

# Suppress TensorFlow logging
tf.get_logger().setLevel('ERROR')

def predict(image_path, model_path):
    """
    Predict crop disease from an image using the trained Keras model.
    
    Args:
        image_path: Path to the input image
        model_path: Path to the trained Keras model
    
    Returns:
        Tuple of (predicted_class, confidence)
    """
    try:
        # Load the model
        model = tf.keras.models.load_model(model_path)
        
        # Class names based on the training data directory structure
        # These should match the order used during training (alphabetical by default)
        # From the training script: Tomato___healthy, Tomato___Late_blight
        # But TensorFlow sorts them alphabetically, so: Tomato___Late_blight, Tomato___healthy
        class_names = ['Tomato___Late_blight', 'Tomato___healthy']
        
        # Verify image and model paths exist
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load and preprocess the image
        IMG_SIZE = 224
        img = tf.keras.utils.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch
        
        # Preprocess for MobileNetV2
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        
        # Make prediction (suppress all output)
        # Temporarily redirect stderr to suppress TensorFlow messages
        _stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        try:
            predictions = model.predict(img_array, verbose=0)
            score = tf.nn.softmax(predictions[0])
        finally:
            sys.stderr.close()
            sys.stderr = _stderr
        
        # Get predicted class and confidence
        predicted_index = np.argmax(score)
        
        # Ensure index is within bounds
        if predicted_index >= len(class_names):
            raise ValueError(f"Predicted index {predicted_index} is out of bounds for {len(class_names)} classes")
        
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(score)) * 100
        
        # Output format: CLASS_NAME|CONFIDENCE (only to stdout, no newline)
        sys.stdout.write(f"{predicted_class}|{confidence:.2f}")
        sys.stdout.flush()
        
    except Exception as e:
        # Only output error to stdout in the expected format
        sys.stdout.write(f"Error|0.0")
        sys.stdout.flush()
        # Write actual error details to stderr (which Java will capture separately)
        sys.stderr.write(f"Error during prediction: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.stdout.write("Error|0.0")
        sys.stdout.flush()
        sys.exit(1)
    
    image_path = sys.argv[1]
    model_path = sys.argv[2]
    
    # Suppress stderr during execution to hide TensorFlow messages
    _stderr = sys.stderr
    _devnull = open(os.devnull, 'w')
    sys.stderr = _devnull
    
    try:
        predict(image_path, model_path)
    finally:
        sys.stderr.close()
        sys.stderr = _stderr

