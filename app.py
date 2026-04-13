import streamlit as st
import requests

st.set_page_config(page_title="PS-Audit", layout="wide")
st.title("PS-Audit")

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

key_input = st.sidebar.text_input("API Key", type="password")
if key_input:
    st.session_state.api_key = key_input

uploaded = st.sidebar.file_uploader("Upload file", type=["py", "c", "cpp", "java"])

def scan(prompt, code):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": "Bearer " + st.session_state.api_key,
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt + "\n\n" + code}]
        },
        timeout=30
    )
    data = r.json()
    if "choices" not in data:
        return "Error: " + str(data.get("error", {}).get("message", str(data)))
    return data["choices"][0]["message"]["content"]

p1 = """Analyze this code for security vulnerabilities. Use this format:

Vulnerability:
Severity: (Low / Medium / Critical)
Why it matters:
Fix:"""

p2 = """Look for bugs or security issues in this code. Keep it short, just tell what's wrong and show the fix."""

if uploaded and st.session_state.api_key:
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

elif not st.session_state.api_key:
    st.info("Paste your Groq API key in the sidebar to get started.")
elif not uploaded:
    st.info("Upload a .py / .c / .cpp / .java file to begin.")
