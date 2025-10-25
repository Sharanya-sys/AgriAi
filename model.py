import tensorflow as tf   
from tensorflow.keras.preprocessing import image   
import numpy as np  

model = tf.keras.applications.MobileNetV2(weights='imagenet')

def predict_disease(img_path):
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array /= 255.0

            predictions = model.predict(img_array)
            decoded = tf.keras.applications.imagenet_utils.decode_predictions(predictions, top=1)[0]
            top_class = decoded[0][1].lower()

            disease_map = {
    'apple': 'Apple Blight - Apply copper fungicide and prune affected leaves.',
    'leaf': 'Leaf Rust - Use neem oil spray and improve air circulation.',
    'banana': 'Banana Wilt - Remove infected plants and use resistant varieties.',
    'potato': 'Potato Blight - Apply fungicide and avoid overhead watering.',
    'granny_smith': 'Healthy Apple - No action needed; monitor regularly.',
    'bell_pepper': 'Healthy Pepper - No action needed; monitor regularly.',
    
    'plant': 'General Plant Issue - Check for pests or nutrients.',
    'foliage': 'Foliage Disease - Possible rust; apply fungicide.',
    'fruit': 'Fruit Disease - Inspect for rot; remove affected parts.',
    'vegetable': 'Vegetable Disease - Monitor soil moisture.',
    'crop': 'Crop Disease - Consult expert for specifics.',
    'plant':'Healthy Plant-Keep up good care.',
}

            
            
            advice = disease_map.get(top_class, 'Unknown Disease - Consult a local agricultural expert for accurate diagnosis.')
            return advice
        
        except Exception as e:
            return f"Error analyzing image: {str(e)}. Please upload a clear photo of the crop."
    
