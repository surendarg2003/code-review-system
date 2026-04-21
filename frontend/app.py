import streamlit as st
import requests
import json
import re
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Code Review Assistant", layout="wide", page_icon="🔍")
st.title("🔍 AI-Powered Code Review Assistant")
st.caption("Paste your code below and get instant, structured feedback on bugs, security, style, and complexity.")

language_options = ["Python", "JavaScript", "SQL", "TypeScript", "Java", "Go", "Rust", "C#", "C++"]
col1, col2 = st.columns([3, 1])

with col1:
    code_input = st.text_area("Paste your code here", height=300, placeholder="# Your code here...")

with col2:
    language = st.selectbox("Language", language_options)
    submit_btn = st.button("🚀 Review Code", type="primary", use_container_width=True)

def stream_response(code: str, lang: str):
    """Generator that yields raw tokens from the backend streaming endpoint."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/review/stream",
            json={"code": code, "language": lang},
            stream=True,
            timeout=90
        )
        response.raise_for_status()
        for chunk in response.iter_content(chunk_size=64, decode_unicode=True):
            if chunk:
                yield chunk
    except requests.exceptions.RequestException as e:
        yield f"\n\n⚠️ Error: {str(e)}"

if submit_btn:
    if not code_input.strip():
        st.warning("Please paste some code to review.")
    else:
        # Show streaming animation & accumulate text
        st.info("🤖 AI is analyzing your code...")
        streamed_text = st.write_stream(stream_response(code_input, language.lower()))
        st.success("✅ Review complete!")

        st.divider()
        
        # Parse the accumulated streaming output
        try:
            match = re.search(r'\{.*\}', streamed_text, re.DOTALL)
            if match:
                review_data = json.loads(match.group(0))
            else:
                review_data = json.loads(streamed_text)

            st.subheader("📊 Review Summary")
            st.info(review_data.get("summary", "No summary provided."))

            issues = review_data.get("issues", [])
            if issues:
                st.subheader("🐛 Identified Issues")
                for i, issue in enumerate(issues, 1):
                    severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue.get("severity", "low"), "⚪")
                    with st.expander(f"{severity_emoji} Issue {i}: {issue['type'].upper()} (Line {issue.get('line', '?')})", expanded=True):
                        st.markdown(f"**Description:** {issue['description']}")
                        st.markdown(f"**Suggestion:** {issue['suggestion']}")
            else:
                st.success("✅ No major issues detected. Code looks solid!")

            refactored = review_data.get("refactored_code", "")
            if refactored:
                st.subheader("✨ Refactored Code")
                st.code(refactored, language=language.lower())

        except json.JSONDecodeError as e:
            st.error("❌ Failed to parse the streaming response as valid JSON.")
            with st.expander("🔍 View raw response"):
                st.code(streamed_text, language="json")