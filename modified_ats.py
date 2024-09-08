import json
import streamlit as st
import google.generativeai as genai 
import PyPDF2 as pdf

with open('config.json', 'r') as f:
    config_data = json.load(f)

GOOGLE_API_KEY = config_data['GOOGLE_API_KEY']

genai.configure(api_key= GOOGLE_API_KEY)

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploade_file):
    reader = pdf.PdfReader(uploade_file)
    text = ""
    
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of tech field, data science, data analyst, machine learning, ML engineer, Software engineering and baig data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very cometitive and you should provide best assistance for improving the resumes. Assign the percentage Matching based on JD and the missing keywords with high accuracy
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match":"%", "MissingKeywords:[]", "Profile Summary":""}}
"""

# Streamlit App
st.title('AI ATS Resume Expert')
st.text('Improve your resume ATS')
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type = 'pdf', help = "Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.write(response)