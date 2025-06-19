import os
import streamlit as st
from utils import fetch_topic_data, generate_podcast_script, generate_audio_file, logger
import datetime

st.set_page_config(page_title="WhisperCast - AI Podcast Generator")

st.markdown("""
    <h2 style="text-align: center; margin: 0; padding: 0; margin-top: -2rem;">WhisperCast</h2>
    <p style="text-align: center; margin: 0; padding: 0; margin-top: 10px; margin-left: -10px; margin-bottom: 3rem;">Turn your ideas into podcasts in no time!</p>
""", unsafe_allow_html=True)



topic = st.text_input("What's the topic for this podcast?", placeholder="e.g. 'The Future of Space Travel'")
generate = st.button("🚀 Generate Podcast")

log_area = st.empty()

if generate and topic:
    log_buffer = []

    def log(msg, level="info"):
        log_buffer.append(f"> {msg}")
        log_area.code("\n".join(log_buffer), language="bash")

    try:
        # Step 1: Fetch data
        log("Fetching topic data")
        content = fetch_topic_data(topic)
        log("Topic data fetched")

        # Step 2: Generate script
        log("Generating podcast script...")
        script = generate_podcast_script(topic, content)
        if not script:
            log("Script generation failed ❌", "error")
            st.error("Script generation failed.")
            st.stop()
        log("Podcast script generated")

        # Step 3: Generate audio
        log("Generating audio file...")
        audio_path = generate_audio_file(script, topic.capitalize())
        if not audio_path:
            log("Audio generation failed", "error")
            st.error("Audio generation failed.")
            st.stop()
        log("Podcast audio ready")

        # Step 4: Output results
        st.success("🎧 Your podcast is ready!")
        st.audio(audio_path)

        with open(audio_path, "rb") as f:
            st.download_button("Download MP3", f, file_name=os.path.basename(audio_path))

        with st.expander("📜 View Transcript"):
            st.markdown(script)

    except Exception as e:
        log(f"Something went wrong: {e}", "error")
        st.error("Oops! Failed to generate podcast. Check logs above.")

elif generate and not topic:
    st.warning("Please enter a topic to begin.")