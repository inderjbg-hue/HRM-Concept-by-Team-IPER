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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #0F172A !important; /* Force Dropdown Menu Font Visibility */
    font-weight: 500;
}

/* --- MAIN CANVAS TYPOGRAPHY & LAYOUT HIERARCHY --- */
h1 {
    color: #1E3A8A !important; /* Corporate Navy Indigo */
    font-weight: 700 !important;
    font-size: 2.6rem !important;
    letter-spacing: -0.03em !important;
    margin-bottom: 0.5rem !important;
}
h2, h3, h4 {
    color: #0F172A !important; /* Crisp Midnight Slate */
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    margin-top: 1.8rem !important;
    margin-bottom: 0.8rem !important;
}

/* Isolated text paragraph overrides to protect system notices */
.stMarkdown-container p, .stMarkdown-container li {
    color: #334155 !important; /* Muted Charcoal Slate Body Text */
    font-size: 15px !important;
    line-height: 1.7 !important;
}

/* Premium Executive Structural Highlight Accent Container */
.executive-highlight {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important;
    border-left: 6px solid #2563EB !important;
    padding: 20px !important;
    border-radius: 8px !important;
    margin: 24px 0 !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.executive-highlight p {
    color: #1E40AF !important; /* Soft Sapphire Blue */
    font-weight: 500 !important;
    margin: 0 !important;
    font-size: 15px !important;
}

/* Interactive Input Elements Framework */
.stTextArea textarea, .stTextInput input, .stChatInput input {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 6px !important;
    padding: 12px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 1px #2563EB !important;
}

/* Standard Form Label Optimization */
label p {
    color: #1E293B !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Hide Native Branding Footers cleanly */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CORE BACKEND ENGINE INITIALIZATION
# ---------------------------------------------------
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# ---------------------------------------------------
# SIDEBAR SYSTEM INTERFACE
# ---------------------------------------------------
with st.sidebar:
    st.markdown("### 🎓 **Navigation Panel**")
    module = st.selectbox(
        "Select Functional Module",
        [
            "Interactive Mentor",
            "Document Knowledge Assistant",
            "Strategic Interview Simulator",
            "Executive Visual Asset Builder"
        ]
    )
    st.markdown("---")
    st.markdown("**Status:** Workspace Connected ✅")
    st.markdown("**Execution Engine:** Llama-3.1-8b-Instant")

# ---------------------------------------------------
# EXECUTIVE CONTAINER OVERVIEW
# ---------------------------------------------------
st.title("💼 ChatGBM Workspace")

st.markdown("""
<div class="executive-highlight">
    <p><strong>Generative Business Management Platform</strong><br>
    An intelligent, high-contrast suite optimized for core conceptual alignment across academic and organizational leadership verticals.</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# MODULE LOGIC: INTERACTIVE MENTOR & DOCUMENT KNOWLEDGE ASSISTANT
# ---------------------------------------------------
if module in ["Interactive Mentor", "Document Knowledge Assistant"]:
    st.subheader(f"🛠️ Active Workspace: {module}")
    st.write("Submit an operational challenge or conceptual framework question directly to the executive mentor engine below.")

    history_key = "chatbot_messages" if module == "Interactive Mentor" else "pdf_messages"
    active_history = st.session_state[history_key]

    document_content = ""
    if module == "Document Knowledge Assistant":
        uploaded_file = st.file_uploader("Upload Academic Syllabus or Reference Notes (PDF Format)", type=["pdf"])
        if uploaded_file is not None:
            with st.spinner("Parsing target document context..."):
                file_bytes = uploaded_file.read()
                document_content = extract_text_from_pdf(file_bytes)
            if document_content.startswith("Extraction Error:"):
                st.error(document_content)
            else:
                st.success("Target document context successfully extracted and compiled!")

    # Render Historical Discussion Elements Stably
    for message in active_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask an executive-level
