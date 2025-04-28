import streamlit as st
from markitdown import MarkItDown
from PIL import Image
import httpx
import time
import base64

# Streamlit page config
st.set_page_config(page_title="YouTube Summarizer", layout="centered")

# Sidebar Inputs
st.sidebar.title("⚙️ Settings")
youtube_url = st.sidebar.text_input("🎥 Paste YouTube URL", placeholder="https://youtu.be/aKsZyLwXtdY")
api_key = st.sidebar.text_input("🔑 SambaNova API Key", type="password")

# Convert logo image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

# Inline logo image
logo_path = r"C:\Users\mkhri\OneDrive\Pictures\Screenshot 2025-04-05 211117.png"
logo_base64 = get_image_base64(logo_path)

# Title and inline image
st.markdown(f"""
# ⚡ World's Fastest YouTube Video Summarizer  
### 🧠 Powered by <img src="data:image/png;base64,{logo_base64}" width="120" style="vertical-align: middle; margin-top: -5px"> Llama-4 Maverick
""", unsafe_allow_html=True)

# Start Analysis
if youtube_url and api_key:
    if st.button("🚀 Summarize Now"):
        try:
            with st.spinner("📦 Converting YouTube video to Markdown..."):
                md = MarkItDown()
                result = md.convert(youtube_url)
                markdown_content = result.text_content

            prompt = f"""
            You are an expert AI video analyst. Your task is to analyze the following YouTube video based on its transcript and content converted to Markdown. Provide a comprehensive breakdown in the following format:

            1. **Main Thesis or Central Claim**
            2. **Key Topics Covered**
            3. **Call to Action or Viewer Engagement**
            4. **Overall Summary**

            ---
            **Transcript (Markdown):**
            {markdown_content}
            ---
            Generate your analysis now.
            """

            # ⏱ Start timer
            start_time = time.time()

            with st.spinner("🤖 Running analysis with SambaNova Llama-4..."):
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "model": "Llama-4-Maverick-17B-128E-Instruct",
                    "messages": [
                        {"role": "user", "content": [{"type": "text", "text": prompt}]}
                    ],
                    "temperature": 0.1,
                    "top_p": 0.1
                }

                response = httpx.post("https://api.sambanova.ai/v1/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()

            # ⏱ End timer and show elapsed time
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 2)

            st.success(f"✅ Summary complete! (⏱ Took {elapsed_time} seconds)")
            st.markdown(result['choices'][0]['message']['content'])

        except Exception as e:
            st.error(f"🚨 Error: {e}")
else:
    st.info("👉 Add a YouTube URL and your SambaNova API Key in the sidebar to get started.")

