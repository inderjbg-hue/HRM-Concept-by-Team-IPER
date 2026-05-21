import streamlit as st
from openai import OpenAI

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="ChatGBM",
    page_icon="🤖",
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

    st.title("🎓 ChatGMB")

    st.markdown("---")

    st.subheader("📚 BM Learning Modules")
    
st.write("""
ChatGBM is a Generative Business Management platform powered by Artificial Intelligence, developed to enhance learning, conceptual understanding, and professional development in the field of management education.

The platform provides intelligent academic assistance across areas including Human Resource Management, Organizational Behaviour, Leadership, Strategic Management, Talent Development, Business Analytics, Recruitment, Employee Engagement, and MBA-level concept learning.
""")

    st.markdown("---")

    st.info("AI-Powered MBA HR Learning Assistant")

# ---------------------------------------------------
# MAIN TITLE
# ---------------------------------------------------
st.title("🤖 ChatGBM")

st.write(
    "Welcome to your AI-powered Human Resource Management Mentor. Ask any HRM, MBA, leadership, or organizational behaviour question."
)

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
    with st.spinner("Analyzing HRM Concepts..."):

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
            "role": "assistant",
            "content": response
        }
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")

st.caption("🚀 Developed by Team IPER | Powered by AI + Streamlit + Groq")
