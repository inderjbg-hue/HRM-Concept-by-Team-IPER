import streamlit as st
from openai import OpenAI
import PyPDF2
import urllib.parse  # Used to safely encode the image prompt text into a URL

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
# PROFESSIONAL EXECUTIVE THEME (HIGH CONTRAST & VISIBILITY)
# ---------------------------------------------------
st.markdown("""
<style>
/* Import Inter Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');

/* Apply global font settings */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
}

/* --- SIDEBAR VISIBILITY FIXES --- */
[data-testid="stSidebar"] {
    background-color: #0F172A !important; /* Premium Dark Navy */
}

/* Force bright contrast on all text, headers, labels inside sidebar */
[data-testid="stSidebar"] *, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] span {
    color: #FFFFFF !important;
}

/* Keep dropdown field input dark text for basic form text entry readability */
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #0F172A !important;
}

/* --- MAIN WINDOW TEXT VISIBILITY FIXES --- */
/* Executive Indigo Blue for Titles */
h1 {
    color: #1E3A8A !important; 
    font-weight: 700 !important;
    font-size: 2.4rem !important;
    margin-bottom: 1rem !important;
}

h2, h3, h4 {
    color: #0F172A !important;
    font-weight: 600 !important;
    margin-top: 1.5rem !important;
}

/* Body Text / Paragraphs Visibility */
.stMarkdown p, p, li, span {
    color: #1E293B !important; /* Crisp Dark Charcoal Slate */
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* Custom Executive Accent Highlight Container */
.executive-highlight {
    background-color: #EFF6FF !important;
    border-left: 5px solid #2563EB !important;
    padding: 16px !important;
    border-radius: 6px !important;
    margin: 18px 0 !important;
}
.executive-highlight p {
    color: #1E40AF !important;
    font-weight: 500 !important;
    margin: 0 !important;
}

/* Chat Input Elements Configuration */
.stChatInput input {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
    border: 1px solid #94A3B8 !important;
}

/* Standardize Interactive Form Component Titles */
label p {
    color: #0F172A !important;
    font-weight: 600 !important;
}

/* Hide Streamlit Native Footer */
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# GROQ CLIENT INITIALIZATION
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
        "Select Learning Module",
        [
            "AI Chatbot",
            "PDF Assistant",
            "AI Interview Simulator",
            "AI Image Generator"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Status:** Workspace Connected ✅")
    st.markdown("**Engine:** Llama-3.1-8b-Instant")

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

st.write("""
ChatGBM delivers targeted executive guidance spanning Human Resource Management, Strategic Frameworks, 
Organizational Performance Architecture, Leadership Theory, Talent Acquisition Frameworks, and Core Analytics.
""")

st.markdown("---")

# ---------------------------------------------------
# MODULE LOGIC: CHATBOT & PDF CONTEXT ASSISTANT
# ---------------------------------------------------
if module in ["AI Chatbot", "PDF Assistant"]:
    st.subheader(f"🛠️ Active Workspace: {module}")
    
    st.write(
        "Submit a programmatic operational challenge or conceptual framework question directly to the executive mentor engine below."
    )

    # Document Extraction Layer
    document_text = ""
    if module == "PDF Assistant":
        uploaded_file = st.file_uploader(
            "Upload Academic Syllabus or PDF Notes",
            type=["pdf"]
        )

        if uploaded_file is not None:
            with st.spinner("Extracting text from PDF..."):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        document
