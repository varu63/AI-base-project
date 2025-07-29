import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv
 
 
 
load_dotenv()
st.set_page_config(page_title="AI Resume critiquer",page_icon="",layout="centered")
st.title("AI Resume Critiquer")
st.markdown("Upload a resume and get AI powered feedback tailored to your needs!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

Uploaded_file = st.file_uploader("Upliade your reaume(PDF , text)",type=["PDF","text"])
job_role = st.text_input("Enter the job role you are targetting(optionL)")

analyze = st.button("Analyze Resume")

def extreact_text_from_pdf(pdf_file):
    pdf_rader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_rader.pages:
        text += page.extract_text()+"\n"
    return text
def extreact_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extreact_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
if analyze and Uploaded_file:
    try:
        file_content = extreact_text_from_file(Uploaded_file)

        if not file_content.strip():
            st.error("File does not have any content")
            st.stop()

        prompt = f"""Please analyze this resume and provide constructive feedback.
        Focud on the following aspects:
        1. content clarity and impact
        2. Skill presentation
        3. Experience description 
        4. Specific improvements for{job_role if job_role else"General job application"}
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear , structured format with specific recommendations."""

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4O-mini",
            massages = [
                {"role":"system","content":"You are an expert resume reviewer with years of experience in HR and recruirment"},
                {"role":"user" , "content":prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        st.markdown("### Analysis Result")
        st.markdown(response.choices[0].massage.content)
    
    except Exception as e:
        st.error(f"An error occurd:{str(e)}")