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

    box_start_x = int(width * 0.35)
    box_start_y = int(height * 0.20)
    box_end_x = int(width * 0.65)
    box_end_y = int(height * 0.75)
    
    cv2.rectangle(img, (box_start_x, box_start_y), (box_end_x, box_end_y), (235, 99, 37), 2)
    cv2.putText(
        img, "ALIGN EYES HERE", (box_start_x + 5, box_start_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (235, 99, 37), 1, cv2.LINE_AA
    )
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# ---------------------------------------------------
# ENTERPRISE EXECUTIVE THEME DESIGN (CLEAN CSS)
# ---------------------------------------------------
css_payload = "<style>" \
              "@import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap'); " \
              "html, body, [data-testid='stAppViewContainer'], [data-testid='stHeader'] { font-family: 'Inter', sans-serif !important; background-color: #F8FAFC !important; } " \
              "[data-testid='stSidebar'] { background-color: #0F172A !important; border-right: 1px solid #1E293B !important; } " \
              "[data-testid='stSidebar'] *, [data-testid='stSidebar'] p, [data-testid='stSidebar'] label, [data-testid='stSidebar'] span { color: #F1F5F9 !important; font-size: 14px; } " \
              "[data-testid='stSidebar'] h3 strong { color: #FFFFFF !important; font-size: 18px !important; } " \
              "[data-testid='stSidebar'] div[data-baseweb='select'] * { color: #0F172A !important; font-weight: 500; } " \
              "h1 { color: #1E3A8A !important; font-weight: 700 !important; font-size: 2.6rem !important; letter-spacing: -0.03em !important; margin-bottom: 0.5rem !important; } " \
              "h2, h3, h4 { color: #0F172A !important; font-weight: 600 !important; letter-spacing: -0.01em !important; margin-top: 1.8rem !important; margin-bottom: 0.8rem !important; } " \
              ".stMarkdown-container p, .stMarkdown-container li { color: #334155 !important; font-size: 15px !important; line-height: 1.7 !important; } " \
              ".executive-highlight { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%) !important; border-left: 6px solid #2563EB !important; padding: 20px !important; border-radius: 8px !important; margin: 24px 0 !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); } " \
              ".executive-highlight p { color: #1E40AF !important; font-weight: 500 !important; margin: 0 !important; font-size: 15px !important; } " \
              ".stTextArea textarea, .stTextInput input, .stChatInput input { color: #0F172A !important; background-color: #FFFFFF !important; border: 1px solid #CBD5E1 !important; border-radius: 6px !important; padding: 12px !important; } " \
              ".stTextArea textarea:focus, .stTextInput input:focus { border-color: #2563EB !important; box-shadow: 0 0 0 1px #2563EB !important; } " \
              "label p { color: #1E293B !important; font-weight: 600 !important; font-size: 14px !important; text-transform: uppercase; letter-spacing: 0.05em; } " \
              "footer { visibility: hidden; }" \
              "</style>"

st.markdown(css_payload, unsafe_allow_html=True)

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

    for message in active_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask an executive-level management question...")

    if question:
        active_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Processing analytical framework compilation..."):
            system_prompt = """You are an expert Data-Driven Human Resource Management Professor and Executive MBA Mentor.
Follow these operational guidelines strictly:
1. Answer clear questions directly from provided source context with exact structural alignments.
2. Structure summaries, matrices, financial numbers, or metrics into clean markdown tables when requested."""
            
            user_payload = question
            if module == "Document Knowledge Assistant" and document_content:
                safe_context = document_content[:12000]
                user_payload = f"Context:\n{safe_context}\n\nQuestion:\n{question}"

            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_payload}
                    ]
                )
                response = completion.choices[0].message.content
            except Exception as api_err:
                response = f"An processing transaction issue occurred: {str(api_err)}"

        with st.chat_message("assistant"):
            st.write(response)
        
        active_history.append({"role": "assistant", "content": response})
        st.session_state[history_key] = active_history

# ---------------------------------------------------
# MODULE LOGIC: STRATEGIC INTERVIEW SIMULATOR
# ---------------------------------------------------
elif module == "Strategic Interview Simulator":
    st.subheader("🎯 Core Competency Interview Simulator")
    st.write("Practice scenario-based hiring sequences using written responses or live webcam evaluation presentations.")

    col_track, col_mode = st.columns(2)
    with col_track:
        role = st.selectbox(
            "Target Assessment Tracks",
            ["HR Executive", "Marketing Executive", "Finance Executive", "MBA Graduate", "Business Analyst"]
        )
    with col_mode:
        st.session_state.interview_mode = st.radio(
            "Select Response Framework",
            ["Written Narrative Framework", "Live Video Presentation Mode"],
            horizontal=True
        )

    if st.button("Generate Interview Assessment Scenario", type="primary"):
        with st.spinner("Synthesizing specialized interview track scenarios..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a Chief Human Resources Officer conducting an executive evaluation interview."},
                        {"role": "user", "content": f"Generate one context-driven behavioral evaluation question for a prospective {role}."}
                    ]
                )
                st.session_state.interview_question = completion.choices[0].message.content
            except Exception as e:
                st.error(f"Error connecting to analytical models: {str(e)}")

    if st.session_state.interview_question:
        st.info(f"**Interviewer Assessment Prompt:** {st.session_state.interview_question}")

    st.markdown("---")

    if st.session_state.interview_mode == "Live Video Presentation Mode":
        st.markdown("### 🎥 Live Executive Presentation Panel")
        
        # Security & Infrastructure Guideline Alert Box
        st.warning(
            "💡 **Camera Troubleshooting:** If the video box below spins infinitely or stays black, verify that: "
            "1) Your browser address bar begins with **HTTPS://** (security protocol requirement). "
            "2) You have explicitly permitted camera access to this webpage."
        )
        
        webrtc_streamer(
            key="interview-video-stream",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]},
                    {"urls": ["stun:stun1.l.google.com:19302"]}
                ]
            },
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True
        )

        st.markdown("### 📝 Response Mapping & Evaluation Context")
        answer = st.text_area(
            "Provide brief talking points or a full summary frame of your video answer for metric evaluation parsing:",
            value=st.session_state.interview_answer,
            key="persistent_interview_input"
        )
        st.session_state.interview_answer = answer

    else:
        st.markdown("### 📝 Written Narrative Framework Panel")
        answer = st.text_area(
            "Provide Professional Written Response Architecture:",
            value=st.session_state.interview_answer,
            key="persistent_interview_input",
            placeholder="Document your comprehensive STAR-method framework response parameters here..."
        )
        st.session_state.interview_answer = answer

    if st.button("Execute Performance Analysis Matrix"):
        if not st.session_state.interview_answer.strip():
            st.warning("Please submit a structured text summary or verbal transcript framework prior to running analytical matrices.")
        else:
            with st.spinner("Analyzing performance score indicators..."):
                try:
                    evaluation = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": "Evaluate the interview response framework rigorously. Provide exact scoring components out of 10 for: Communication Clarity, Domain Mastery, and Executive Presence. Conclude with notable Candidate Strengths and Key Areas of Development."
                            },
                            {"role": "user", "content": f"Question asked: {st.session_state.interview_question}\nCandidate Response: {st.session_state.interview_answer}"}
                        ]
                    )
                    st.success("Analysis Cycle Matrix Finished")
                    st.markdown(evaluation.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error compiling performance data elements: {str(e)}")

# ---------------------------------------------------
# MODULE LOGIC: EXECUTIVE VISUAL ASSET BUILDER
# ---------------------------------------------------
elif module == "Executive Visual Asset Builder":
    st.subheader("🎨 Executive Visual Asset Builder")
    st.write("Construct professional framework layouts, structural concepts, and data blueprints seamlessly.")

    st.markdown("### 🎛️ 1. Define Asset Structure")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        layout_style = st.selectbox(
            "Visual Blueprint Layout",
            ["Flat Minimalist Infographic Diagram", "2x2 Strategic Matrix Grid", "Sequential Flowchart Process Map", "Clean Executive Presentation Slide Design"]
        )
    with col2:
        color_palette = st.selectbox(
            "Corporate Color Architecture",
            ["Modern Tech (Navy, Blue, White Background)", "Executive Classic (Charcoal, Indigo, Gray Background)"]
        )
    with col3:
        aspect_ratio = st.selectbox("Canvas Aspect Ratio Target", ["16:9 (Widescreen Presentation)", "1:1 (Square Grid Asset)"])

    st.markdown("### 📝 2. Describe Your Core Business Concept")
    user_concept = st.text_input(
        "What operational model or strategic theme should this asset represent visually?",
        value=st.session_state.image_prompt_value,
        key="persistent_image_input",
        placeholder="e.g., A 3-step modern talent pipeline outlining alignment, talent acquisition, and performance analytics grids"
    )
    st.session_state.image_prompt_value = user_concept

    if st.button("Synthesize Executive Visual Asset", type="primary"):
        if not st.session_state.image_prompt_value.strip():
            st.warning("Please outline an operational business concept value before launching synthesis models.")
        else:
            with st.spinner("Compiling structural constraints and canvas matrix layers..."):
                constructed_prompt = (
                    f"A crisp corporate {layout_style} depicting: {st.session_state.image_prompt_value}. "
                    f"Color palette settings: {color_palette}. Flat vector design, minimalist presentation deck layout, production ready."
                )
                
                width, height = 1024, 1024
                if "16:9" in aspect_ratio:
                    width, height = 1280, 720

                # FIXED PATHWAY: Cleaned arguments, dropped unstable custom model string params causing 422/400 errors
                encoded_prompt = urllib.parse.quote(constructed_prompt)
                generation_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&nologo=true"
                
                try:
                    response = requests.get(generation_url, timeout=45)
                    if response.status_code == 200:
                        st.session_state.current_image_bytes = response.content
                    else:
                        st.error(f"The synthesis engine encountered an line asset generation error exception. (Status Code: {response.status_code})")
                except Exception as e:
                    st.error(f"Network processing transaction interruption: {str(e)}")

    if st.session_state.current_image_bytes:
        st.markdown("---")
        st.markdown("### 🖼️ Synthesized Blueprint Output")
        st.image(st.session_state.current_image_bytes, use_container_width=True)
        st.success("Visual asset blueprint compiled and anchored successfully!")

# ---------------------------------------------------
# PERSISTENT FOOTER SECTION
# ---------------------------------------------------
st.markdown("---")
st.caption("ChatGBM System Architecture • Built for High Contrast Professional Presentation Modules")
