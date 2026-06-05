import streamlit as st
from openai import OpenAI
import io

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
        
        img_file = st.camera_input("Capture/Verify Executive Camera Feed Connection")
        if img_file is not None:
            st.success("Camera feed linked successfully! Proceed with framing your verbal response below.")

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
    st.subheader("🎨 Executive Visual Matrix Blueprint Builder")
    st.write("Construct real-time corporate SWOT models and quadrants without any API external network blockers.")

    st.markdown("### 🎛️ Input Matrix Content Parameters")
    
    # 4 clean distinct inputs for an executive SWOT grid layout mapping
    col_s, col_w = st.columns(2)
    with col_s:
        val_s = st.text_input("💪 Core Internal Strengths (S)", "Internal brand value, unique proprietary technology pipelines.")
    with col_w:
        val_w = st.text_input("⏳ Identified Weaknesses (W)", "High overhead infrastructure dependencies, reliance on single supply line hubs.")

    col_o, col_t = st.columns(2)
    with col_o:
        val_o = st.text_input("🚀 Emerging Market Opportunities (O)", "Expanding vertical channels across growing regional economies.")
    with col_t:
        val_t = st.text_input("⚡ Mitigating Risks & Threats (T)", "Socio-political framework changes, accelerating market entry rates.")

    st.markdown("---")
    st.markdown("### 🖼️ Generated Live Dashboard Presentation Canvas")

    # High fidelity SVG layout drawing vectors. Fast, lightweight, renders crisp text on all displays.
    svg_canvas = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" style="width:100%; height:auto; background:#F8FAFC; border-radius:12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); font-family:'Inter', system-ui, sans-serif;">
        <!-- STRENGTHS QUADRANT -->
        <rect x="20" y="20" width="370" height="220" rx="8" fill="#F0FDF4" stroke="#BBF7D0" stroke-width="2"/>
        <text x="40" y="60" font-size="20" font-weight="700" fill="#166534">💪 STRENGTHS (S)</text>
        <foreignObject x="40" y="85" width="330" height="140">
            <p style="margin:0; font-size:14px; line-height:1.6; color:#14532D; font-weight:500;">{val_s}</p>
        </foreignObject>

        <!-- WEAKNESSES QUADRANT -->
        <rect x="410" y="20" width="370" height="220" rx="8" fill="#FFF5F5" stroke="#FEB2B2" stroke-width="2"/>
        <text x="430" y="60" font-size="20" font-weight="700" fill="#9B2C2C">⏳ WEAKNESSES (W)</text>
        <foreignObject x="430" y="85" width="330" height="140">
            <p style="margin:0; font-size:14px; line-height:1.6; color:#742A2A; font-weight:500;">{val_w}</p>
        </foreignObject>

        <!-- OPPORTUNITIES QUADRANT -->
        <rect x="20" y="260" width="370" height="220" rx="8" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="2"/>
        <text x="40" y="300" font-size="20" font-weight="700" fill="#1E40AF">🚀 OPPORTUNITIES (O)</text>
        <foreignObject x="40" y="325" width="330" height="140">
            <p style="margin:0; font-size:14px; line-height:1.6; color:#1E3A8A; font-weight:500;">{val_o}</p>
        </foreignObject>

        <!-- THREATS QUADRANT -->
        <rect x="410" y="260" width="370" height="220" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="2"/>
        <text x="430" y="300" font-size="20" font-weight="700" fill="#92400E">⚡ THREATS (T)</text>
        <foreignObject x="430" y="325" width="330" height="140">
            <p style="margin:0; font-size:14px; line-height:1.6; color:#78350F; font-weight:500;">{val_t}</p>
        </foreignObject>
    </svg>
    """
    
    # Inject directly into the Streamlit app view
    st.markdown(svg_canvas, unsafe_allow_html=True)
    st.success("Executive SWOT Asset Vector Layout rendered live below panel!")

# ---------------------------------------------------
# PERSISTENT FOOTER SECTION
# ---------------------------------------------------
st.markdown("---")
st.caption("ChatGBM System Architecture • Built for High Contrast Professional Presentation Modules")
