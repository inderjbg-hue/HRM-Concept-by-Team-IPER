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

    st.subheader("📚 HRM Learning Modules")

    st.write("""
    ✅ Human Resource Management  
    ✅ Recruitment & Selection  
    ✅ Training & Development  
    ✅ Performance Appraisal  
    ✅ Compensation Management  
    ✅ Employee Engagement  
    ✅ Leadership  
    ✅ Organizational Behaviour  
    ✅ HR Analytics  
    ✅ Talent Management  
    ✅ Strategic HRM  
    ✅ Industrial Relations  
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
