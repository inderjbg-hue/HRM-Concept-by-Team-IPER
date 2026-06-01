import streamlit as st
from openai import OpenAI
import PyPDF2

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
            "AI Interview Simulator"
        ]
    )
    
    st.markdown("---")
    st.markdown("**Status:** Workspace Connected ✅")
    st.markdown("**Engine:** Llama-3.1-8b-Instant")
    st.markdown("**Upload Ceiling:** Up to 300MB Configured 📂")

# ---------------------------------------------------
# EXECUTIVE CONTAINER OVERVIEW
# ---------------------------------------------------
st.title("💼 ChatGBM Workspace")

st.markdown("""
<div class="executive-highlight">
    <p><strong>Generative Business Management Platform</strong><br>
    An intelligent, high-contrast suite optimized for deep analytical context processing, document calculations, and executive training workflows.</p>
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
        "Submit a programmatic operational challenge, raw data array, or document question directly to the executive engine below."
    )

    # Enhanced Document Extraction Layer (Optimized safely for mega-files)
    document_text = ""
    if module == "PDF Assistant":
        uploaded_file = st.file_uploader(
            "Upload Large-Scale Reports or PDF Notes",
            type=["pdf"]
        )

        if uploaded_file is not None:
            with st.spinner("Extracting multi-page document blocks... Please wait for large datasets."):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                total_pages = len(pdf_reader.pages)
                
                # Dynamic text extraction
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        document_text += text
                        
                st.success(f"Successfully compiled and parsed {total_pages} pages of data structure!")

    # Message Arrays Construction
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # UI Context Redraw
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input Capturing Trigger
    question = st.chat_input("Ask about facts, formulas, numerical metrics, concepts, or request infographics layout...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.spinner("Processing deep analysis models..."):
            system_prompt = (
                "You are an expert Data-Driven Human Resource Management Professor and Executive MBA Mentor. "
                "Your objective is to thoroughly unpack documents provided by the user. "
                "1. Thoroughly explain any questions asked from the attached text files.\n"
                "2. Identify, define, and dissect core academic and business management concepts.\n"
                "3. Generate highly concise, strategic executive summaries upon request.\n"
                "4. Meticulously analyze, structure, and double-check any numerical or mathematical data present in the document text.\n"
                "5. INFOGRAPHICS REQUESTS: If the user asks for an infographic or visual representation, generate it cleanly within the message markdown using formatted tables, code-block flowcharts, clear section badges, or comprehensive emoji-based metric trees to mock up a stunning visual structure."
            )
            
            user_content = question
            if module == "PDF Assistant" and document_text:
                # SAFE TOKEN LIMITATION GAP CONTROL:
                # Large 200MB+ texts blow past LLM limitations. We truncate the raw string context 
                # safely up to ~40,000 characters (~10,000 words) to prevent OpenAI status crash 
                # while retaining substantial structural reading room.
                truncated_context = document_text[:40000]
                if len(document_text) > 40000:
                    truncated_context += "\n\n[Context truncated by application safety boundaries to protect API token ceiling...]"
                
                user_content = f"Use the following document text reference to fully answer the question:\n\n[REFERENCE CONTENT]:\n{truncated_context}\n\n[USER PROMPT]:\n{question}"

            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ]
                )
                response = completion.choices[0].message.content
            except Exception as api_err:
                response = (
                    "⚠️ **API Token Saturation Limit Encountered:** The text profile payload of this massive document "
                    "exceeded the engine's real-time transactional thresholds. Please try refining your query to ask for "
                    "a more specific chapter, table metric, or summary target area."
                )

        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------------------------------------
# MODULE LOGIC: STRATEGIC INTERVIEW SIMULATOR
# ---------------------------------------------------
if module == "AI Interview Simulator":
    st.subheader("🎯 Core Competency Interview Simulator")
    
    st.write(
        "Practice scenario-based structural hiring sequences. Complete evaluation prompts to access analytical review matrices."
    )

    role = st.selectbox(
        "Target Assessment Tracks",
        [
            "HR Executive",
            "Marketing Executive",
            "Finance Executive",
            "MBA Graduate",
            "Business Analyst"
        ]
    )

    if st.button("Generate Diagnostic Prompt", type="primary"):
        with st.spinner("Synthesizing specialized interview track scenarios..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a Chief Human Resources Officer conducting a leadership evaluation interview."},
                    {"role": "user", "content": f"Generate one highly comprehensive, context-driven behavioral evaluation question for a prospective {role}."}
                ]
            )
            st.session_state.interview_question = completion.choices[0].message.content

    if "interview_question" in st.session_state:
        st.info(st.session_state.interview_question)

        answer = st.text_area("Provide Professional Narrative Response:")

        if st.button("Analyze & Evaluate Performance"):
            if not answer.strip():
                st.warning("Please submit a textual response prior to analysis execution.")
            else:
                with st.spinner("Synthesizing quantitative score matrices..."):
                    evaluation = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": "Evaluate the provided interview response framework strictly. Provide precise marks on: Communication Clarity /10, Domain Concept Application /10, and Analytical Delivery /10. List notable Candidate Strengths, Key Areas of Development, and a firm overall placement recommendation."
                            },
                            {"role": "user", "content": answer}
                        ]
                    )
                    st.success("Analysis Cycle Matrix Finished")
                    st.markdown(evaluation.choices[0].message.content)

# ---------------------------------------------------
# PERSISTENT FOOTER SECTION
# ---------------------------------------------------
st.markdown("---")
st.caption("ChatGBM Architecture • Built for High Contrast Professional Delivery Tracks")
