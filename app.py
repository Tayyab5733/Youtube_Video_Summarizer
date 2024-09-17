## Import
import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv() #load all the environment variable
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))




prompt='''You are a Youtube video summarizer. You task is to
take transcript text of entire video and provide important summary in points within 200 words. 
Please provide the summary of the text given here:'''

## Getting data from videos

def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        print(video_id)
        transcript_text =YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " "
        for i in transcript_text:
            transcript += " "+ i["text"]

        return transcript
        

    except Exception as e:
        raise e

## Getting summary
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

## Get link and display thumbnail

st.title("Youtube transcript to detailed notes converter")
youtube_link=st.text_input("Enter video url:")
if youtube_link:
    video_id=youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
if st.button("Get detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("Detailed_Notes")
        st.write(summary)

