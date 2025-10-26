
import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential, load_model # type: ignore
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam # type: ignore

# ====== Dataset Path ======
dataset_path = r"C:\Users\shara\Downloads\archive\PlantVillage" # <-- update to your dataset path
model_file = "plant_model.h5"

# ====== Load / Train Model ======
if os.path.exists(model_file):
    model = load_model(model_file)
else:
    # Load images
    train_gen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    train_data = train_gen.flow_from_directory(
        dataset_path,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical',
        subset='training'
    )
    # MobileNetV2 base
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
    base_model.trainable = False
# Build model
    model = Sequential([
        base_model,
        Flatten(),
        Dense(128, activation='relu'),
        Dense(len(train_data.class_indices), activation='softmax')
    ])

    model.compile(optimizer=Adam(0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    # Train (MVP: few epochs)
    model.fit(train_data, epochs=5)
    model.save(model_file)

    # Save class mapping
    class_names = {v:k for k,v in train_data.class_indices.items()}
    np.save("class_names.npy", class_names)

# ====== Load class mapping ======
class_names = np.load("class_names.npy", allow_pickle=True).item()

# ====== Prediction Function ======
def predict_disease(img_path):
    try:
        img = image.load_img(img_path, target_size=(224,224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)/255.0

        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions, axis=1)[0]
        class_label = class_names[class_idx]

        return f"Disease Prediction: {class_label}"
    except Exception as e:
        return f"Error: {str(e)}"
