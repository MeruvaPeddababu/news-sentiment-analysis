import streamlit as st
import requests

st.set_page_config(page_title="News Sentiment Analysis", layout="wide")

# 🎨 Sidebar for company selection
st.sidebar.title("🔍 Select Company")
companies = ["Tesla", "Apple", "Google", "Microsoft", "OpenAI", "Facebook"]
company = st.sidebar.selectbox("Choose a company", companies)

st.sidebar.write("Or enter a custom company:")
custom_company = st.sidebar.text_input("Enter company name")

# Use custom company if entered
selected_company = custom_company if custom_company else company

# Main title
st.title("📰 News Sentiment Analysis & Hindi Speech")

if st.sidebar.button("Fetch News"):
    with st.spinner("Fetching latest news..."):
        api_url = f"http://127.0.0.1:5000/news?company={selected_company}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            
            st.subheader(f"📌 News for {data['Company']}")

            # ✅ Display JSON output instead of markdown text
            st.json(data)

            # 🎧 Download Hindi Speech
            st.sidebar.subheader("🎙️ Download Hindi Speech")
            audio_url = f"http://127.0.0.1:5000/download-audio?company={selected_company}"
            st.sidebar.markdown(f"[⬇ Download MP3]({audio_url})", unsafe_allow_html=True)

        else:
            st.error("Failed to fetch news. Please try again.")
