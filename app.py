import streamlit as st
import requests
import os

st.set_page_config(page_title="PS-Audit", layout="wide")
st.title("PS-Audit")

api_key = st.secrets.get("OPENROUTER_API_KEY", "") or st.sidebar.text_input("API Key", type="password")
uploaded = st.sidebar.file_uploader("Upload file", type=["py", "c", "cpp", "java"])

def scan(prompt, code):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": "deepseek/deepseek-r1:free",
            "messages": [{"role": "user", "content": f"{prompt}\n\n{code}"}]
        },
        timeout=30
    )
    data = r.json()
    if "choices" not in data:
        return f"API Error: {data.get('error', {}).get('message', str(data))}"
    return data["choices"][0]["message"]["content"]

p1 = """Analyze this code for security vulnerabilities. Use this format:

Vulnerability:
Severity: (Low / Medium / Critical)
Why it matters:
Fix:"""

p2 = """Look for bugs or security issues in this code. Keep it short, just tell what's wrong and show the fix."""

if uploaded and api_key:
    code = uploaded.read().decode("utf-8", errors="ignore")

    st.subheader("Your Code")
    st.code(code, language=uploaded.name.split(".")[-1])

    if st.button("Scan"):
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Analysis 1")
            with st.spinner("scanning..."):
                st.markdown(scan(p1, code))

        with c2:
            st.subheader("Analysis 2")
            with st.spinner("double checking..."):
                st.markdown(scan(p2, code))

elif not api_key:
    st.warning("👈 Paste your OpenRouter API key in the sidebar to get started.")
elif not uploaded:
    st.info("👈 Upload a .py / .c / .cpp / .java file to begin scanning.")
