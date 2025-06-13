import streamlit as st
import pandas as pd
import openai
import re

# --- Page Config ---
st.set_page_config(
    page_title="CSV Assistant by Shaloam",
    page_icon="🧠",
    layout="wide"
)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>📊 AI CSV Assistant by Shaloam Mutetwa</h1>", unsafe_allow_html=True)
st.write("Upload a CSV file and ask questions in natural language. Get AI-powered answers instantly.")

# --- Sidebar Branding ---
with st.sidebar:
    st.markdown("### About Me")
    st.markdown("Built by **Shaloam Mutetwa**")
    st.markdown("[ LinkedIn](https://www.linkedin.com/in/shaloam-mutetwa-770b0013a/)")
    st.markdown("[Email](mailto:shalomutetwa@gmail.com)")  # Update your actual email
    st.caption("Powered by OpenAI GPT-4")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 Preview of Uploaded Data")
    st.dataframe(df.head())

    # --- API Key Input ---
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

    # --- Natural Language Input ---
    question = st.text_area("Ask a question about your data:", height=100)
    go = st.button("Submit")

    if go and openai_api_key.startswith("sk-"):
        with st.spinner("Thinking..."):
            openai.api_key = openai_api_key

            # Construct system prompt
            prompt = f"""You are a smart data analyst.

The user has uploaded a dataset, shown below:
{df.head().to_csv(index=False)}

Answer the user's question clearly and concisely.
- Use natural language or SQL-style explanations if needed.
- Do NOT assume the data comes from a CSV file.
- DO NOT use or return Python code.
- Base your response only on the data the user uploaded.

User question: {question}
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "system", "content": prompt}]
                )
                answer = response["choices"][0]["message"]["content"]

                # Strip any Python code just in case
                cleaned = re.sub(r"```python.*?```", "", answer, flags=re.DOTALL)

                st.markdown("### 🤖 Answer")
                st.markdown(cleaned.strip())

            except Exception as e:
                st.error(f"Error from OpenAI: {str(e)}")
    elif go:
        st.error("Please enter a valid OpenAI API key.")

# --- Footer ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        font-size: 0.85em;
        color: gray;
        padding: 0.5em 0;
    }
    </style>
    <div class="footer">
        Created by Shaloam Mutetwa
    </div>
    """,
    unsafe_allow_html=True
)



