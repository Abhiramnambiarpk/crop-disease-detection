import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import numpy as np
import pathlib

# 1. SETUP: Define paths and parameters
# Use pathlib for easy path management
data_dir = pathlib.Path('mini_dataset/')
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 10  # Keep it low for a quick trial

# 2. DATA PIPELINE: Load data and create datasets
# Create a training dataset (80% of the data)
train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE)

# Create a validation dataset (20% of the data)
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE)

# Get the class names from the folder names
class_names = train_ds.class_names
print("Classes found:", class_names)

# Configure the dataset for performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# 3. MODEL BUILDING: Transfer Learning & Anti-Overfitting

# a) Data Augmentation Layer
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.1),
], name="data_augmentation")

# b) Load MobileNetV2 base model
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,  # Don't include the final ImageNet classifier
    weights='imagenet'
)
# Freeze the base model so we only train our new layers
base_model.trainable = False

# c) Build the final model
inputs = keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = data_augmentation(inputs)  # Apply augmentation
x = tf.keras.applications.mobilenet_v2.preprocess_input(
    x)  # Preprocess for MobileNetV2
x = base_model(x, training=False)  # Run the base model
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)  # Regularization to prevent overfitting
outputs = layers.Dense(len(class_names), activation='softmax')(
    x)  # Our classifier head
model = keras.Model(inputs, outputs)

# --- 4. COMPILE AND TRAIN ---
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

print("--- Starting Model Training ---")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)
print("--- Training Complete ---")


# --- 5. VISUALIZE RESULTS (to check for overfitting) ---
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(range(EPOCHS), acc, label='Training Accuracy')
plt.plot(range(EPOCHS), val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(range(EPOCHS), loss, label='Training Loss')
plt.plot(range(EPOCHS), val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


# --- 6. TEST THE MODEL AND GET FARMER TIPS ---

# This dictionary maps the model's prediction to helpful advice
farmer_tips = {
    'Tomato___healthy': "Your plant looks healthy! Keep up the good work. Ensure consistent watering and monitor for any changes.",
    'Tomato___Late_blight': "Late Blight detected.  blight is a fungal disease. \n1. **Action**: Immediately remove and destroy infected leaves. \n2. **Treatment**: Apply a copper-based fungicide. \n3. **Prevention**: Ensure good air circulation around plants and avoid overhead watering."
}

# Function to make a prediction and provide tips


def predict_and_advise(image_path):
    img = tf.keras.utils.load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    predicted_class = class_names[np.argmax(score)]
    confidence = 100 * np.max(score)

    print(f"\n--- Prediction for {image_path.name} ---")
    print(
        f"This leaf is most likely: **{predicted_class}** with {confidence:.2f}% confidence.")
    print("\n💡 **Recommendation:**")
    print(farmer_tips[predicted_class])


# Find an image from your validation set to test
sample_image_path = pathlib.Path(
    'C:/Users/aadis/6890c333-c7d2-4d50-8734-f70b61cef213___GH_HL Leaf 447.1.JPG')
predict_and_advise(sample_image_path)
# (Your existing training code is here...)

print("--- Training Complete ---")
model.save('crop_disease_model.keras')
print("--- Model Saved to crop_disease_model.keras ---")
