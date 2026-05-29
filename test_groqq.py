import streamlit as st
from openai import OpenAI
import PyPDF2

from streamlit_webrtc import webrtc_streamer
import av
import cv2

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="ChatGBM",
    page_icon="GBM",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CORPORATE MBA THEME
# ---------------------------------------------------
st.markdown("""
<style>

/* Main App Background */
.main {
    background-color: #F4F6F9;
}

/* Main Title */
h1 {
    color: #1E3A5F;
    text-align: center;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Normal Text */
.stMarkdown, p {
    color: #2C3E50;
    font-size: 16px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1E3A5F;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Chat Input Box */
.stChatInput input {
    background-color: white;
    border-radius: 10px;
    border: 1px solid #B0BEC5;
    padding: 10px;
}

/* Chat Messages */
[data-testid="stChatMessageContent"] {
    background-color: white;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #E0E0E0;
}

/* Buttons */
.stButton button {
    background-color: #1E3A5F;
    color: white;
    border-radius: 8px;
    border: none;
}

/* Footer Hide */
footer {
    visibility: hidden;
}

/* Top Toolbar Hide */
header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    color: #4B0082;
    text-align: center;
    font-weight: bold;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

[data-testid="stSidebar"] {
    background-color: #ece6ff;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# GROQ CLIENT
# ---------------------------------------------------
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.title("ChatGMB")

    st.markdown("---")

    st.subheader("BM Learning Modules")

    module = st.selectbox(
    "Select Module",
    [
        "AI Chatbot",
        "PDF Assistant",
        "AI Interview Simulator"
    ]
)
    
st.write("""
ChatGBM is a Generative Business Management platform powered by Artificial Intelligence, developed to enhance learning, conceptual understanding, and professional development in the field of management education.

The platform provides intelligent academic assistance across areas including Human Resource Management, Organizational Behaviour, Leadership, Strategic Management, Talent Development, Business Analytics, Recruitment, Employee Engagement, and MBA-level concept learning.
""")

st.markdown("---")

st.info("AI-Powered MBA HR Learning Assistant")

if module in ["AI Chatbot", "PDF Assistant"]:
# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------
st.title("ChatGBM")

st.write(
    "Welcome to your AI-powered Education Mentor. Ask any HRM, Marketing, Finance, leadership, or organizational behaviour question."
)

# ---------------------------------------------------
# PDF DOCUMENT UPLOAD
# ---------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload PDF Notes or Documents",
    type=["pdf"]
)

document_text = ""

if uploaded_file is not None:

    pdf_reader = PyPDF2.PdfReader(uploaded_file)

    for page in pdf_reader.pages:

        text = page.extract_text()

        if text:
            document_text += text

    st.success("Document uploaded successfully!")
    
# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------
question = st.chat_input("Ask Your HRM Question")

# ---------------------------------------------------
# AI RESPONSE
# ---------------------------------------------------
if question:

    # Store User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Show User Message
    with st.chat_message("user"):
        st.write(question)

    # Generate AI Response
    with st.spinner("Analyzing Business Management Concepts..."):

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an expert Human Resource Management Professor and MBA Mentor.

                    Your responses should:
                    - Be professional
                    - Include definitions
                    - Explain concepts deeply
                    - Give practical HR insights
                    - Include examples
                    - Use MBA-level explanations
                    - Be structured and educational
                    """
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        response = completion.choices[0].message.content

    # Show AI Response
    with st.chat_message("assistant"):
        st.write(response)

    # Store AI Response
    st.session_state.messages.append(
        {
            
    "role": "user",
    "content": f"""
    You are an expert Business Management and HRM mentor.

    Use the uploaded document below to answer the user's question.

    DOCUMENT CONTENT:
    {document_text}

    USER QUESTION:
    {question}

    Give detailed, professional and MBA-level explanations.
    """

        }
    )
if module == "AI Interview Simulator":

    st.title("AI Interview Simulator")

    st.write(
        "Practice HR, Marketing, Finance and MBA interviews using AI."
    )

    st.subheader("Live Camera")

    webrtc_streamer(
        key="camera"
    )

    role = st.selectbox(
        "Select Interview Role",
        [
            "HR Executive",
            "Marketing Executive",
            "Finance Executive",
            "MBA Graduate",
            "Business Analyst"
        ]
    )

    if st.button("Generate Interview Question"):

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "Act as an HR interviewer."
                },
                {
                    "role": "user",
                    "content": f"Generate one interview question for {role}"
                }
            ]
        )

        st.session_state.interview_question = (
            completion.choices[0].message.content
        )

    if "interview_question" in st.session_state:

        st.info(st.session_state.interview_question)

        answer = st.text_area(
            "Type Your Answer"
        )

        if st.button("Evaluate Answer"):

            evaluation = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Evaluate interview responses.

                        Provide:

                        1. Communication Score /10
                        2. Confidence Score /10
                        3. Subject Knowledge Score /10
                        4. Strengths
                        5. Areas of Improvement
                        6. Final Recommendation
                        """
                    },
                    {
                        "role": "user",
                        "content": answer
                    }
                ]
            )

            st.success(
                evaluation.choices[0].message.content
            )
# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.caption("Developed by Teaching Enthusiast for Learning Enthusiasts | Powered by AI + Streamlit + Groq")
