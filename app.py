

import streamlit as st  #type: ignore
from model import predict_disease   #type: ignore
import requests   #type: ignore
import os

# Custom CSS for a beautiful, agri-themed UI
st.markdown("""
<style>
    .main { background-color: #f0f8e7; }  /* Light green background */
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 10px; font-size: 16px; }
    .stTextInput, .stFileUploader { border-radius: 10px; }
    .success { color: #2E8B57; font-weight: bold; }
    .warning { color: #FFA500; font-weight: bold; }
    .info { color: #4682B4; font-weight: bold; }
    h1, h2, h3 { color: #228B22; }  /* Dark green headers */
    .footer { text-align: center; font-size: 12px; color: #666; margin-top: 50px; }
</style>
""", unsafe_allow_html=True)
#st.write(f"Debug: Model predicted '{top_class}'")

# Sidebar for tips and navigation
st.sidebar.title("🌱 AgriAI Tips")
st.sidebar.markdown("*For Best Results:*")
st.sidebar.markdown("- Upload clear, well-lit photos of crops.")
st.sidebar.markdown("- Focus on diseased leaves or fruits.")
st.sidebar.markdown("- Check weather alerts for prevention.")
st.sidebar.markdown("---")
st.sidebar.markdown("*About:* AI-powered tool for farmers to detect diseases quickly.")

# Main title and description
st.title("🌾 AgriAI: Crop Disease Detector")
st.markdown("### Empowering Farmers with AI for Healthier Crops")
st.markdown('THIS IS MVP')

st.write("Upload a photo of your crop (e.g., leaves or fruits) to get instant disease diagnosis, advice, and weather insights. Let's protect your harvest! 🚜")

# File uploader with better styling
uploaded_file = st.file_uploader("📸 Choose a crop image (JPG/PNG)...", type=["jpg", "png", "jpeg"], help="Select a clear image for accurate results.")

if uploaded_file is not None:
    # Layout: Image on left, results on right
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(uploaded_file, caption='📷 Uploaded Crop Image', use_column_width=True, width=300)
    
    with col2:
        # AI Analysis with spinner and progress
        with st.spinner('🔍 Analyzing with AI... Please wait!'):
            advice = predict_disease(uploaded_file)
        
        # Display results with color coding
        if "Error" in advice:
            st.error(f"❌ {advice}")
        else:
            st.success(f"✅ *AI Diagnosis & Advice:* {advice}")
            st.markdown("💡 *Next Steps:* Follow the advice to treat your crops and prevent spread.")
        
        # Weather Integration
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your actual key
        city = "London"  # Change to e.g., "Delhi" for relevance
        try:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
            if response.status_code == 200:
                data = response.json()
                weather_desc = data['weather'][0]['description'].capitalize()
                temp = data['main']['temp']
                humidity = data['main']['humidity']
                st.info(f"🌤 *Weather Alert for {city}:* {weather_desc}, {temp}°C, Humidity: {humidity}%. High humidity may increase disease risk—monitor closely!")
            else:
                st.warning("⚠ Weather data unavailable. Check your API key or internet connection.")
        except:
            st.warning("⚠ Unable to fetch weather data.")
        
        # Farm Health Tracker with expandable section
        with st.expander("📊 Farm Health Tracker (Recent Diagnoses)"):
            if 'history' not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(advice)
            for i, item in enumerate(st.session_state.history[-5:], 1):  # Show last 5
                st.write(f"{i}. {item}")
    
    # Clean up temp file
    if os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")

# Footer
st.markdown("---")
st.markdown('<div class="footer">Built with ❤ using Python, TensorFlow, and Streamlit. For scalability, integrate with mobile apps or IoT sensors.   This is MVP</div>', unsafe_allow_html=True)
st.markdown('<div class="footer"> Contact: [thantrysharanya@gmail.com/sharanya]</div>', unsafe_allow_html=True)

        










