import streamlit as st
import streamlit.components.v1 as components
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
if "spoken_state" not in st.session_state:
    st.session_state.spoken_state = False

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
                response = f"An issue occurred: {str(api_err)}"

        with st.chat_message("assistant"):
            st.write(response)
        
        active_history.append({"role": "assistant", "content": response})
        st.session_state[history_key] = active_history

# ---------------------------------------------------
# MODULE LOGIC: STRATEGIC INTERVIEW SIMULATOR (AUDIO CAPABLE)
# ---------------------------------------------------
elif module == "Strategic Interview Simulator":
    st.subheader("🎯 Core Competency Audio Interview Simulator")
    st.write("Practice real-time oral interview evaluations with verbal Indian-accent prompts and multi-aspect feedback metrics.")

    role = st.selectbox(
        "Target Assessment Tracks",
        ["HR Executive", "Marketing Executive", "Finance Executive", "MBA Graduate", "Business Analyst"]
    )

    if st.button("Generate & Speak Next Interview Question", type="primary"):
        st.session_state.spoken_state = False
        with st.spinner("Synthesizing context-driven assessment tracks..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a Chief Human Resources Officer conducting an executive evaluation interview. Ask exactly ONE concise behavioral interview question."},
                        {"role": "user", "content": f"Generate a creative situational interview question evaluating core competencies for a prospective {role}."}
                    ]
                )
                st.session_state.interview_question = completion.choices[0].message.content.replace('"', '\\"')
            except Exception as e:
                st.error(f"Error connecting to analytical models: {str(e)}")

    if st.session_state.interview_question:
        st.info(f"**Interviewer Prompt (Text View):** {st.session_state.interview_question}")
        
        # Indian Accent Web Speech Synthesis Javascript Injection Engine
        if not st.session_state.spoken_state:
            tts_js = f"""
            <script>
                function speakQuestion() {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        var msg = new SpeechSynthesisUtterance("{st.session_state.interview_question}");
                        var voices = window.speechSynthesis.getVoices();
                        
                        // Look specifically for English India regional system voice identifiers
                        var indianVoice = voices.find(function(v) {{
                            return v.lang.includes('en-IN') || v.name.includes('India') || v.name.includes('Indian');
                        }});
                        
                        if (indianVoice) {{
                            msg.voice = indianVoice;
                        }}
                        msg.rate = 0.95;
                        msg.pitch = 1.0;
                        window.speechSynthesis.speak(msg);
                    }}
                }}
                // Execute on load and backup trigger loop if voices take a moment to bind
                speakQuestion();
                if (window.speechSynthesis.onvoiceschanged !== undefined) {{
                    window.speechSynthesis.onvoiceschanged = speakQuestion;
                }}
            </script>
            """
            components.html(tts_js, height=0, width=0)
            st.session_state.spoken_state = True

    st.markdown("---")
    st.markdown("### 🎙️ Submit Your Response")
    
    # Clean fallback standard mic device recorder input layer
    audio_data = st.audio_input("Record your verbal answer response here")
    if audio_data is not None:
        st.success("Audio data successfully captured and securely mapped to frame!")

    st.markdown("### 📝 Response Transcript Frame")
    answer = st.text_area(
        "Paste speech-to-text transcript or outline your verbal answer structure parameters here:",
        value=st.session_state.interview_answer,
        placeholder="Type or paste your spoken answer script parameters for full structural alignment checks..."
    )
    st.session_state.interview_answer = answer

    if st.button("Execute Performance Analysis Matrix"):
        if not st.session_state.interview_answer.strip():
            st.warning("Please outline your answer framework in the transcript box before compiling metrics.")
        else:
            with st.spinner("Analyzing performance indicators..."):
                try:
                    evaluation = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert executive assessment panel. Analyze the candidate response thoroughly. "
                                    "You must break down your critique into explicit feedback metrics covering:\n"
                                    "1. ANSWER RELEVANCE (Alignment with the target role and scenario questions)\n"
                                    "2. FLUENCY & COHERENCE (Structural logic flow, vocabulary accuracy, and tone composition)\n"
                                    "3. DOMAIN MASTERY (Use of professional terminology and actionable metrics)\n"
                                    "Provide specific examples from their response and clear recommendations for improvement."
                                )
                            },
                            {"role": "user", "content": f"Question: {st.session_state.interview_question}\nCandidate Response: {st.session_state.interview_answer}"}
                        ]
                    )
                    st.success("Multi-Aspect Performance Analysis Compiled Successfully")
                    st.markdown(evaluation.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error compiling performance data elements: {str(e)}")

# ---------------------------------------------------
# MODULE LOGIC: EXECUTIVE VISUAL ASSET BUILDER (FLOWCHART RENDERING ENGINE)
# ---------------------------------------------------
elif module == "Executive Visual Asset Builder":
    st.subheader("🎨 Executive Visual Flowchart & Asset Builder")
    st.write("Generate interactive, professional corporate flowcharts and strategic diagrams live using code syntax.")

    st.markdown("### 🎛️ 1. Asset Configuration")
    asset_topic = st.text_input(
        "What sequential business model, lifecycle, or flowchart concept are you building?",
        value="Supply Chain Optimization Flowchart",
        placeholder="e.g., Marketing Funnel Sequence, Client Onboarding Flow, Product Lifecycle"
    )

    st.markdown("### 📝 2. Outline the Process Steps")
    user_data = st.text_area(
        "Describe the chronological flow or blocks you want inside your visual flowchart:",
        value="1. Supplier Logistics ships raw parts.\n2. Inbound Warehouse sorts inventory.\n3. Quality Assurance checks metrics.\n4. If approved, route to Distribution Hub. If failed, return to Supplier.",
        height=100
    )

    if st.button("Generate Visual Interactive Flowchart", type="primary"):
        st.markdown("---")
        st.markdown(f"### 📊 Rendered Flowchart Canvas: {asset_topic}")
        
        with st.spinner("Compiling structural chart graphics..."):
            try:
                system_prompt = (
                    "You are a backend business systems architect. Convert the user's process sequence into an "
                    "isolated, valid Mermaid.js flowchart string. Start strictly with 'graph TD' or 'graph LR'. "
                    "Use clear uppercase text labels inside blocks. Output ONLY the raw diagram code text. Do not wrap in markdown fences or talk."
                )
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Convert this process into a flowchart code block: {user_data}"}
                    ]
                )
                
                mermaid_code = response.choices[0].message.content.strip()
                if "```" in mermaid_code:
                    mermaid_code = mermaid_code.split("```")[1].replace("mermaid", "").strip()

                html_canvas = f"""
                <div style="background: white; border: 1px solid #E2E8F0; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                    <script type="module">
                        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                        mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
                    </script>
                    <pre class="mermaid" style="display: flex; justify-content: center; background: white;">
                        {mermaid_code}
                    </pre>
                </div>
                """
                
                components.html(html_canvas, height=450, scrolling=True)
                st.success("Vector flowchart successfully built on page!")
                
                with st.expander("Show Blueprint Syntax"):
                    st.code(mermaid_code, language="markdown")
                    
            except Exception as e:
                st.error(f"Error mapping interactive flowchart matrices: {str(e)}")

# ---------------------------------------------------
# PERSISTENT FOOTER SECTION
# ---------------------------------------------------
st.markdown("---")
st.caption("ChatGBM System Architecture • Built for High Contrast Professional Presentation Modules")
