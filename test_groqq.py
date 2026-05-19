import streamlit as st
from openai import OpenAI

# GROQ CLIENT USING OPENAI SDK
client = OpenAI(
    api_key=st.secrets["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"],
    base_url="https://api.groq.com/openai/v1"
)

# TITLE
st.title("🤖 HIM AI HR Mentor")

st.write("Ask any HRM question")

# INPUT
question = st.text_input("Enter Question")

# RESPONSE
if question:

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f'''
                You are an expert HRM Professor.

                Answer professionally with:
                - Definitions
                - Examples
                - Practical HR insights
                - MBA-level explanation

                Question:
                {question}
                '''
            }
        ]
    )

    st.write(completion.choices[0].message.content)
