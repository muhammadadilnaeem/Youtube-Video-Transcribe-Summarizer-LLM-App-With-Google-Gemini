# Importing Libraries that will be used in this project
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt for the gemini model
prompt = """
You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 300 words. Please provide the summary of the text given here:  
"""

# Define the function to get the gemini response
def get_gemini_response(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(transcript_text + prompt)
    return response.text

# Define the function to extract the transcript details
def extract_transcript_details(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry['text'] for entry in transcript_list])
        return transcript

    except Exception as e:
        raise e

# Function to extract video ID from URL
def extract_video_id(youtube_url):
    patterns = [
        r'v=([^&]+)',  # Standard YouTube URL
        r'youtu\.be/([^?]+)',  # Shortened YouTube URL
    ]
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

# Setup Streamlit app
st.set_page_config(page_title="📹 YouTube Video Transcribe Summarizer")
st.markdown("<h1 style='text-align: center; color: #FF5733;'>📹 YouTube Video Transcribe Summarizer</h1>", unsafe_allow_html=True)

youtube_link = st.text_input("🔗 Enter YouTube Video Link...")

# When the button is clicked
if youtube_link:
    video_id = extract_video_id(youtube_link)
    if video_id:
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("📝 Get Detailed Notes"):
    video_id = extract_video_id(youtube_link)
    if video_id:
        try:
            transcript = extract_transcript_details(video_id)
            gemini_response = get_gemini_response(transcript, prompt)
            st.markdown("<h2 style='color: #1E90FF;'>📝 Generated Summary:</h2>", unsafe_allow_html=True)
            st.markdown(f"<div style='background-color: #F0F8FF; padding: 10px; border-radius: 5px;'>{gemini_response}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Invalid YouTube URL")
