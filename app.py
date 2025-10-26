
import sys
sys.path.insert(0,'./src')
import streamlit as st 
from model import predict_disease
import requests

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #f6fff5; font-family: 'Poppins', sans-serif; }
    h1, h2, h3 { color: #1b5e20; text-align: center; }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 12px;
        font-size: 16px;
        padding: 8px 16px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #388e3c;
        color: white;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #444;
        margin-top: 40px;
    }
    .recommend-box {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 12px 18px;
        border-radius: 10px;
        margin-top: 10px;
    }
    .dos, .donts {
        font-size: 15px;
        line-height: 1.8;
    }
    .dos { color: #2e7d32; }
    .donts { color: #c62828; }
    .title-box {
        background-color: #dcedc1;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title(" AgriAI: Crop Disease Detector")
st.markdown("### Empowering Farmers with Artificial Intelligence for a Healthier Harvest ")
st.markdown("Upload a clear crop photo, and let AgriAI detect diseases, suggest treatments, and provide prevention tips in seconds! 🚜")
st.write("---")

# Sidebar Tips
st.sidebar.title(" AgriAI Tips")
st.sidebar.markdown("☘ For Best Results:")
st.sidebar.markdown("- Upload clear, well-lit photos of crops.")
st.sidebar.markdown("- Focus on diseased leaves or fruits.")
st.sidebar.markdown("- Check weather alerts for prevention.")
st.sidebar.markdown("---")
st.sidebar.markdown("☘ ABOUT: AI-powered tool for farmers to detect diseases quickly.")

# File Upload Section
uploaded_file = st.file_uploader("📸 Upload your crop image (JPG/PNG)...", type=["jpg", "jpeg", "png"])

# Prediction and Recommendations
if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(uploaded_file, caption="📷 Uploaded Image", use_column_width=True)

    with col2:
        with st.spinner("🔍 Analyzing your crop... please wait..."):
            advice = predict_disease(uploaded_file)

        # Disease-based Recommendations
        recommendations = {
            "Healthy": {
                "Treatment": "Your plant looks healthy! Maintain regular sunlight, proper watering, and good soil nutrition.",
                "Prevention": "Keep monitoring for early signs of pests or nutrient deficiencies. Use organic compost and neem oil periodically.",
                "Organic Tip": "Spray neem oil biweekly to prevent pests naturally."
            },
            "Tomato___Early_blight": {
                "Treatment": "Detected Tomato Early Blight. Remove affected leaves immediately and apply mancozeb fungicide.",
                "Prevention": "Avoid overhead watering, rotate crops yearly, and maintain good ventilation.",
                "Organic Tip": "Use compost tea or garlic spray weekly to strengthen plant immunity."
            },
            "Tomato___Late_blight": {
                "Treatment": "Detected Tomato Late Blight. Prune infected leaves and apply copper fungicide promptly.",
                "Prevention": "Water at soil level, avoid overcrowding, and ensure proper airflow.",
                "Organic Tip": "Spray neem oil + baking soda solution weekly to reduce infection risk."
            },
            "Potato___Early_blight": {
                "Treatment": "Detected Potato Early Blight. Prune damaged leaves and apply appropriate fungicide.",
                "Prevention": "Practice crop rotation and water at soil level only.",
                "Organic Tip": "Compost tea or garlic spray can help prevent fungal infections naturally."
            },
            "Potato___Late_blight": {
                "Treatment": "Detected Potato Late Blight. Remove infected parts and apply fungicide immediately.",
                "Prevention": "Avoid overhead watering and maintain proper ventilation.",
                "Organic Tip": "Neem oil applications weekly help reduce spread."
            },
            "Tomato___Virus": {
                "Treatment": "Detected Tomato Virus. Remove infected plants to prevent spread.",
                "Prevention": "Use virus-resistant varieties and control insect vectors like whiteflies.",
                "Organic Tip": "Maintain clean tools and healthy soil to reduce susceptibility."
            },
            "Potato___Virus": {
                "Treatment": "Detected Potato Virus. Destroy infected plants and clean surrounding soil.",
                "Prevention": "Use certified seed potatoes and control aphid populations.",
                "Organic Tip": "Regularly apply organic mulch to improve soil health."
            },
            "Spot": {
                "Treatment": "Detected leaf spots. Prune affected areas and apply fungicide if necessary.",
                "Prevention": "Avoid wetting leaves during irrigation and provide proper spacing.",
                "Organic Tip": "Neem oil spray or baking soda solution helps control spot infections."
            },
            "Other": {
                "Treatment": "Your crop may have an uncommon issue. Monitor closely and consult an expert if it persists.",
                "Prevention": "Maintain good hygiene, proper watering, and soil nutrition.",
                "Organic Tip": "Use natural sprays like neem oil or garlic solution periodically."
            }
        }

        st.success(f" AI Diagnosis: {advice}")

        # Match recommendation to disease
        disease = None
        for key in recommendations.keys():
            if key.lower() in advice.lower():
                disease = key
                break

        if disease:
            rec = recommendations[disease]
            st.markdown("###  Recommendations Based on Result")
            st.markdown(f"""
                            *Treatment:* {rec['Treatment']}  
                             *Prevention:* {rec['Prevention']}  
                             *Organic Tip:* {rec['Organic Tip']}
                             """)
        else:
            st.info(" Monitor your crops regularly for early signs of infection.")

        # Farmer Health Tracker
        st.markdown("###  Recent Diagnoses Tracker")
        if 'history' not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(advice)
        for i, item in enumerate(st.session_state.history[-5:], 1):  # Show last 5
            st.write(f"{i}. {item}")

        # Weather Alert
        api_key = "d13e7d45edaf98c04a596864b3227d0d"  # Replace with your API key
        city = "Bengaluru"
        try:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['description'].capitalize()
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                st.info(f"🌤 Weather in {city}: {weather}, {temp}°C, Humidity: {humidity}%")
        except:
            st.warning("⚠ Unable to fetch weather details right now.")

st.write("---")

# Do's and Don’ts Section
st.subheader(" Do’s and  Don’ts for Sustainable Farming")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="dos">
    ✅ Regularly check leaves and soil condition.<br>
    ✅ Use organic compost and biofertilizers.<br>
    ✅ Water early in the morning.<br>
    ✅ Practice crop rotation.<br>
    ✅ Keep your garden tools clean.
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="donts">
    ❌ Don’t use chemical sprays unnecessarily.<br>
    ❌ Avoid stagnant water around crops.<br>
    ❌ Don’t mix diseased plants with healthy ones.<br>
    ❌ Don’t overwater plants.<br>
    ❌ Don’t ignore early yellow or brown leaf spots.
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# Footer
st.markdown("""
<div style='text-align:center; font-size:20px; font-weight:bold; color:#2e7d32; margin-top:30px;'>
 Together, let's help farmers achieve a greener and healthier future 
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
Built with  using Python, TensorFlow & Streamlit<br>
 <b>Contact:</b> thantrysharanya@gmail.com<br>
© 2025 AgriAI - Smart Farming Companion
</div>
""", unsafe_allow_html=True)
