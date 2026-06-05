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
                response = f"An issue occurred: {str(api_err)}"

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
            st.warning("Please submit a structured text summary framework prior to running analytical matrices.")
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
                # Direct prompt instructing Groq to output only structural Mermaid chart markup
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
                # Fixed string literal split syntax
                if "```" in mermaid_code:
                    mermaid_code = mermaid_code.split("```")[1].replace("mermaid", "").strip()

                # Build an isolated, secure HTML iframe payload to inject Mermaid.js CDN and draw clean canvas shapes
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
                
                # Render the responsive canvas vector graphic directly on the interface window
                components.html(html_canvas, height=450, scrolling=True)
                st.success("Vector flowchart successfully built on page! (Right-click chart to save as file image)")
                
                with st.expander("Show Blueprint Syntax"):
                    st.code(mermaid_code, language="markdown")
                    
            except Exception as e:
                st.error(f"Error mapping interactive flowchart matrices: {str(e)}")

# ---------------------------------------------------
# PERSISTENT FOOTER SECTION
# ---------------------------------------------------
st.markdown("---")
st.caption("ChatGBM System Architecture • Built for High Contrast Professional Presentation Modules")
