import streamlit as st
import os
from dotenv import load_dotenv # for loading API keys
load_dotenv() # load all environment variables
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt = "YouTube video summarizer: take the transcript text and summarize the video, providing the important points within 250 words. The transcript text is appended here: "

# Function to extract text from YouTube video
def extract(url):
    try:
        id = url.split("v=")[1].split("&")[0]  # Handle case where URL has additional parameters
        txt = YouTubeTranscriptApi.get_transcript(id)
        # Concatenate transcript text
        text = " ".join([i["text"] for i in txt])
        return text 
    except Exception as e:
        return str(e)

# Function to generate summary using Google Gemini model
def generate_gemini_content(text, prompt):
    try:
        model=genai.GenerativeModel("gemini-pro")
        res=model.generate_content(prompt+text)
        return res.text
    except Exception as e:
        return str(e)

# Creating Streamlit app
st.title("YouTube Video Summarizer")
link = st.text_input("Enter the YouTube Video Link:")

if link:
    try:
        id = link.split("v=")[1].split("&")[0]  # Handle case where URL has additional parameters
        st.image(f"http://img.youtube.com/vi/{id}/0.jpg", use_column_width=True)  # Default image URL to get thumbnail image
    except IndexError:
        st.error("Invalid YouTube URL. Please enter a valid link.")

if st.button("Get Detailed Note"):
    if link:
        txt = extract(link)
        if "Error" in txt or "error" in txt:
            st.error(f"Failed to extract transcript: {txt}")
        else:
            data = generate_gemini_content(txt, prompt)
            if "Error" in data or "error" in data:
                st.error(f"Failed to generate summary: {data}")
            else:
                st.markdown("## Detailed Notes")
                st.write(data)
