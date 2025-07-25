import streamlit as st
from PIL import Image
#import pyttsx3
#import os
import pytesseract  
import google.generativeai as genai
import streamlit.components.v1 as components
from langchain_google_genai import GoogleGenerativeAI

genai.configure(api_key = (st.secrets["google_api"]["GEMINI_API_KEY"]))
# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = r'"C:\Program Files\Tesseract-OCR\tesseract.exe"'

# Initialize Google Generative AI with API Key
#os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = genai.GenerativeModel(model_name = "gemini-1.5-flash-latest")
# Initialize Text-to-Speech engine
#engine = pyttsx3.init()




st.set_page_config(page_title="FriendlyFinder👀🔍", layout="wide", page_icon="🌐🤝")
st.markdown(
    """
    <style>
     .main-title {
        font-size: 48px;
         font-weight: bold;
         text-align: center;
         color: #0662f6;
         margin-top: -20px;
     }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .feature-header {
        font-size: 24px;
        color: #333;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">FriendlyFinder👀🔍</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle"> Bridging Connections with AI Smarts and a Human Touch!🤖❤️</div>', unsafe_allow_html=True)

# Sidebar Features
st.sidebar.image("assets/Logo.jpg", width=350)


# Set up the sidebar for "ℹ️ About" section with concise description
st.sidebar.title("ℹ️ About")
st.sidebar.markdown(
   """
    📌 **Features**
    - 🔍 **Describe Scene**: Get AI insights about the image, including objects and suggestions.
    - 📝 **Extract Text**: Extract visible text using OCR.
    - 🔊 **Text-to-Speech**: Hear the extracted text aloud.

    💡 **How it helps**:
    Assists visually impaired users by providing scene descriptions, text extraction, and speech.

    🤖 **Powered by**:
    - **Google Gemini API** for scene understanding.
    - **Tesseract OCR** for text extraction.
    - **pyttsx3** for text-to-speech.
    """ 
)

# Text box below the sidebar description
st.sidebar.text_area ("📜 Instructions", """Upload an image to begin. Select a feature to proceed:
1️⃣ Describe the Scene
2️⃣ Extract Text
3️⃣ Listen to the Text""")


# Functions for functionality
def extract_text_from_image(image):
    """Extracts text from the given image."""
    return pytesseract.image_to_string(image)

# def text_to_speech(text):
#     """Converts the given text to speech."""
#     engine.say(text)
#     engine.runAndWait()

def tts_browser(text):
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{text}");
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Upload Image Section
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Buttons Section
st.markdown("<h3 class='feature-header'>⚙️ Features</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

scene_button = col1.button("🔍 Scene Description")
ocr_button = col2.button("📝 Text Extraction")
tts_button = col3.button("🔊 Text-to-Speech Conversion")

# Input Prompt for Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Process user interactions
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
            st.write(response)

    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", text, height=150)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                tts_browser(text)
                st.success("✅ Text-to-Speech Conversion Completed!")
            else:
                st.warning("Please provide some text.")

# Footer
st.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Google Gemini API</strong> |👤 Gopisetty Sai Charan| Built with Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <hr>
    <footer style="text-align:center;">
        <p>Powered by <strong>Google Gemini API</strong> | 👤 Gopisetty Sai Charan | Built with Streamlit</p>
    </footer>
    """,
    unsafe_allow_html=True,
)