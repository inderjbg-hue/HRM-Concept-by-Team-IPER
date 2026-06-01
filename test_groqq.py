code = """import streamlit as st
from openai import OpenAI
import PyPDF2

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="ChatGBM",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# PROFESSIONAL EXECUTIVE THEME (CLEAN & HIGH CONTRAST)
# ---------------------------------------------------
st.markdown(\"\"\"
<style>
/* Import a highly professional corporate font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Apply global font and main app background */
.stApp {
    font-family: 'Inter', sans-serif;
    background-color: #F8FAFC;
}

/* --- SIDEBAR VISIBILITY FIXES --- */
[data-testid="stSidebar"] {
    background-color: #0F172A !important; /* Deep Navy Blue */
}

/* Force high contrast white color on all text/labels inside the sidebar */
[data-testid="stSidebar"] .stMarkdown, 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] div {
    color: #FFFFFF !important;
}

/* Style the dropdown label inside sidebar specifically */
[data-testid="stSidebar"] data-testid="stWidgetLabel" p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* --- MAIN WINDOW TEXT VISIBILITY FIXES --- */
/* Titles & Headings */
h1 {
    color: #1E3A8A !important; /* Premium Executive Blue */
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    letter-spacing: -0.025em;
    margin-bottom: 1rem !important;
}

h2, h3, h4 {
    color: #0F172A !important; /* Dark Slate Blue */
    font-weight: 600 !important;
}

/* Body / Paragraph Text in Main Window */
.stMarkdown p, p, li, span {
    color: #334155 !important; /* Slate Gray (highly readable, modern alternative to pure black) */
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* Highlight boxes */
.highlight-container {
    background-color: #EFF6FF;
    border-left: 4px solid #3B82F6;
    padding: 15px;
    border-radius: 4px;
    margin: 15px 0;
}

/* Input Boxes */
.stChatInput input {
    border-radius: 8px !important;
    border: 1px solid #CBD5E1 !important;
    color: #0F172A !important;
}

/* Chat Message Styling */
[data-testid="stChatMessageContent"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
}

/* Form Fields Context Text */
label {
    color: #1E293B !important;
    font-weight: 500 !important;
}

/* Footer Hide */
footer {
    visibility: hidden;
}
</style>
\"\"\", unsafe_allow_html=True)

# ---------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# ---------------------------------------------------
# SIDEBAR NAVIGATION
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
    st.markdown("**Status:** System Connected ✅")
    st.markdown("**Model:** Llama-3.1-8b-Instant")

# ---------------------------------------------------
# MAIN CONTENT HEADER
# ---------------------------------------------------
st.title("💼 ChatGBM")

# Styled Highlight Box for Intro Summary Text
st.markdown(\"\"\"
<div class="highlight-container">
    <strong>Generative Business Management Platform</strong><br>
    An advanced AI environment developed to enhance professional training, conceptual understanding, and academic expertise across key management verticals.
</div>
\"\"\", unsafe_allow_html=True)

st.write(\"\"\"
The platform delivers deep academic and conceptual simulation workflows spanning 
Human Resource Management, Organizational Behaviour, Corporate Strategy, Business Analytics, 
Talent Acquisition, and Leadership Development.
\"\"\")

st.markdown("---")

# ---------------------------------------------------
# WORKFLOW 1: CHATBOT & PDF ASSISTANT
# ---------------------------------------------------
if module in ["AI Chatbot", "PDF Assistant"]:
    st.subheader(f"🛠️ Module Mode: {module}")
    
    st.write(
        "Engage with your AI Graduate Advisor. Ask any contextual business management, framework, or operational strategy question below."
    )

    # Document upload workflow if explicitly in PDF assistant mode
    document_text = ""
    if module == "PDF Assistant":
        uploaded_file = st.file_uploader(
            "Upload PDF Reference Materials / Notes",
            type=["pdf"]
        )

        if uploaded_file is not None:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    document_text += text
            st.success("Reference document context loaded successfully!")

    # --- CHAT REGION ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Previous History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User Input Field
    question = st.chat_input("Enter your business management query...")

    if question:
        # Save & Render User Query
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        # Generate Contextual Response Loop
        with st.spinner("Analyzing executive framework models..."):
            
            # Formulate the contextual framing based on file existence
            system_prompt = """You are an expert Human Resource Management Professor and Executive MBA Mentor.
Your responses should be highly structured, academic yet practical, include formal framework definitions, and give concrete executive examples."""
            
            user_prompt = question
            if module == "PDF Assistant" and document_text:
                user_prompt = f"Use the following referenced material to answer the question.\\n\\n[DOCUMENT CONTENT]:\\n{document_text}\\n\\n[USER QUESTION]:\\n{question}"

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            response = completion.choices[0].message.content

        # Save & Render Agent Answer
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

# ---------------------------------------------------
# WORKFLOW 2: INTERVIEW SIMULATOR
# ---------------------------------------------------
if module == "AI Interview Simulator":
    st.subheader("🎯 Executive Performance Interview Simulator")
    
    st.write(
        "Simulate full-panel enterprise or leadership recruitment tracks. Answer structural open-ended prompts to receive objective domain score matrixing."
    )

    role = st.selectbox(
        "Target Organizational Function",
        [
            "HR Executive",
            "Marketing Executive",
            "Finance Executive",
            "MBA Graduate",
            "Business Analyst"
        ]
    )

    if st.button("Generate Interview Question", type="primary"):
        with st.spinner("Formulating behavioral indicator question..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a senior Corporate HR Director conducting a behavioral interview."},
                    {"role": "user", "content": f"Generate one complex, situation-based interview question for a {role} role."}
                ]
            )
            st.session_state.interview_question = completion.choices[0].message.content

    if "interview_question" in st.session_state:
        st.info(st.session_state.interview_question)

        answer = st.text_area("Your Executive Response Input:")

        if st.button("Evaluate Response Performance"):
            if answer.strip() == "":
                st.warning("Please type your answer response before evaluating.")
            else:
                with st.spinner("Matrixing core competencies..."):
                    evaluation = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": \"\"\"Evaluate the candidate interview response analytically.
Provide clear breakdown metrics for:
1. Communication Crispness /10
2. Professional Delivery /10
3. Conceptual Domain Knowledge /10
4. Core Structural Strengths
5. Critical Improvement Items
6. Enterprise Match Recommendation\"\"\"
                            },
                            {"role": "user", "content": answer}
                        ]
                    )
                    st.success("Evaluation Report Generated Successfully")
                    st.markdown(evaluation.choices[0].message.content)

# ---------------------------------------------------
# APP FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("ChatGBM Framework • Powered by AI + Streamlit + Groq Architecture")
"""

with open("test_groqq-v2.py", "w") as f:
    f.write(code)

print("Successfully generated test_groqq-v2.py")
