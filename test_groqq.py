import streamlit as st
from openai import OpenAI
import urllib.parse
import requests
import io
import cv2
import av

# Import WebRTC core framework components safely
from streamlit_webrtc import webrtc_streamer, WebRtcMode

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="ChatGBM Workspace",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# GLOBAL STATE INITIALIZATION
# ---------------------------------------------------
if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = []
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []
if "interview_question" not in st.session_state:
    st.session_state.interview_question = ""
if "interview_answer" not in st.session_state:
    st.session_state.interview_answer = ""
if "image_prompt_value" not in st.session_state:
    st.session_state.image_prompt_value = ""
if "current_image_bytes" not in st.session_state:
    st.session_state.current_image_bytes = None
if "interview_mode" not in st.session_state:
    st.session_state.interview_mode = "Written Narrative Framework"

# ---------------------------------------------------
# STABLE DOCUMENT EXTRACTION CACHE LAYER
# ---------------------------------------------------
@st.cache_data(show_spinner=False)
def extract_text_from_pdf(file_bytes):
    import pypdf
    extracted_text = ""
    try:
        pdf_stream = io.BytesIO(file_bytes)
        pdf_reader = pypdf.PdfReader(pdf_stream)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text
    except Exception as e:
        return f"Extraction Error: {str(e)}"
    return extracted_text

# ---------------------------------------------------
# ADVANCED VIDEO FILTER & ALIGNMENT PROCESSOR
# ---------------------------------------------------
def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    """
    Applies an inline digital alignment grid using OpenCV.
    Ensures candidates maintain clean eye-contact and professional executive centering.
    """
    img = frame.to_ndarray(format="bgr24")
    height, width, _ = img.shape

    # Centering framework parameters (Golden Ratio alignment metrics)
    box_start_x = int(width * 0.35)
    box_start_y = int(height * 0.20)
    box_end_x = int(width * 0.65)
    box_end_y = int(height * 0.75)
    
    # Render a professional corporate blue framing boundary layout overlay
    cv2.rectangle(img, (box_start_x, box_start_y), (box_end_x, box_end_y), (235, 99, 37), 2)
    
    cv2.putText(
        img, "ALIGN EYES HERE", (box_start_x + 5, box_start_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (235, 99, 37), 1, cv2.LINE_AA
    )

    return av.VideoFrame.from_ndarray(img, format="bgr24")

# ---------------------------------------------------
# ENTERPRISE EXECUTIVE THEME DESIGN (CUSTOM CSS STYLE)
# ---------------------------------------------------
st.markdown("""
<style>
/* Import Clean Professional Inter Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');

/* Global Font Override */
html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #F8FAFC !important; /* Premium Off-White Slate */
}

/* --- SIDEBAR VISIBILITY & CONTRAST CONFIGURATION --- */
[data-testid="stSidebar"] {
    background-color: #0F172A !important; /* Deep Slate Blue Navy */
    border-right: 1px solid #1E293B !important;
}
[data-testid="stSidebar"] *, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] span {
    color: #F1F5F9 !important; /* Soft Ice White Text */
    font-size: 14px;
}
[data-testid="stSidebar"] h3 strong {
    color: #FFFFFF !important;
    font-size: 18px !important;
}
[data-testid="stSidebar"] div
