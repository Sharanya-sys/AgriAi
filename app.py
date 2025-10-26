import sys
sys.path.insert(0,'.')
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

st.title("🌾 AgriAI: Crop Disease Detector")
#  Box-style Header
#st.markdown('<div class="title-box"><h1>🌾 AgriAI - Smart Crop Disease Detector</h1></div>', unsafe_allow_html=True)

st.markdown("### Empowering Farmers with Artificial Intelligence for a Healthier Harvest 🌿")
st.markdown("Upload a clear crop photo, and let AgriAI detect diseases, suggest treatments, and provide prevention tips in seconds! 🚜")
st.write("---")
#  Sidebar Tips
st.sidebar.title("🌱 AgriAI Tips")
st.sidebar.markdown("*☘ For Best Results:*")
st.sidebar.markdown("- Upload clear, well-lit photos of crops.")
st.sidebar.markdown("- Focus on diseased leaves or fruits.")
st.sidebar.markdown("- Check weather alerts for prevention.")
st.sidebar.markdown("---")
st.sidebar.markdown("*☘ ABOUT:* AI-powered tool for farmers to detect diseases quickly.")





#  File Upload Section
uploaded_file = st.file_uploader("📸 Upload your crop image (JPG/PNG)...", type=["jpg", "jpeg", "png"])

#  Prediction and Recommendations
if uploaded_file is not None:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(uploaded_file, caption="📷 Uploaded Image", use_column_width=True)

    with col2:
        with st.spinner("🔍 Analyzing your crop... please wait..."):
            advice = predict_disease(uploaded_file)

        #  Disease-based Recommendations
        recommendations = {
            "Healthy": {
                "Treatment": "No treatment required — your plant looks healthy! 🌱",
                "Prevention": "Maintain good sunlight and regular watering.",
                "Organic Tip": "Spray neem oil biweekly to keep leaves pest-free."
            },
            "Tomato___Late_blight": {
                "Treatment": "Remove affected leaves and apply copper fungicide.",
                "Prevention": "Avoid overhead watering and ensure ventilation.",
                "Organic Tip": "Spray neem oil + baking soda solution weekly."
            },
            "Potato___Early_blight": {
                "Treatment": "Use mancozeb fungicide early on and prune damaged leaves.",
                "Prevention": "Water at soil level and rotate crops yearly.",
                "Organic Tip": "Compost tea and garlic spray are effective naturally."
            },
            "Apple___Scab": {
                "Treatment": "Use sulfur-based fungicide and prune diseased twigs.",
                "Prevention": "Clear fallen leaves; improve air circulation.",
                "Organic Tip": "Apply lime-sulfur spray during dormant stage."
            },
            "Corn___Common_rust": {
                "Treatment": "Apply foliar fungicide; remove heavily infected leaves.",
                "Prevention": "Grow rust-resistant varieties and irrigate carefully.",
                "Organic Tip": "Use milk-water spray (1:10 ratio) twice a week."
            }
        }

        st.success(f"✅ AI Diagnosis: {advice}")

        #  Match recommendation to disease
        disease = None
        for key in recommendations.keys():
            if key.lower() in advice.lower():
                disease = key
                break

        if disease:
            rec = recommendations[disease]
            st.markdown("### 🌿 Recommendations Based on Result")
            st.markdown(f"""
            <div class="recommend-box">
            <b>Treatment:</b> {rec['Treatment']}<br>
            <b>Prevention:</b> {rec['Prevention']}<br>
            <b>Organic Tip:</b> {rec['Organic Tip']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("🌱 Monitor your crops regularly for early signs of infection.")

        #  Farmer Health Tracker
        st.markdown("### 📊 Recent Diagnoses Tracker")
        if 'history' not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append(advice)
        for i, item in enumerate(st.session_state.history[-5:], 1):  # Show last 5
            st.write(f"{i}. {item}")

        #  Weather Alert
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

#  Do's and  Don’ts Section
st.subheader("✅ Do’s and ❌ Don’ts for Sustainable Farming")
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

#  Footer
st.markdown("""
<div style='text-align:center; font-size:20px; font-weight:bold; color:#2e7d32; margin-top:30px;'>
🌾 Together, let's help farmers achieve a greener and healthier future 🌿
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
Built with ❤ using Python, TensorFlow & Streamlit<br>
📧 <b>Contact:</b> thantrysharanya@gmail.com<br>
© 2025 AgriAI - Smart Farming Companion
</div>
""", unsafe_allow_html=True)
