import json
import streamlit as st
from PIL import Image
import pdf2image
import google.generativeai as genai 
import io
import base64

# 1. Field to put the job description
# 2. Upload the PDF
# 3. PDF to image --> processing --> google gemini pro
# 4. Prompt template[Multiple Prompts]

with open('config.json', 'r') as f:
    config_data = json.load(f)

GOOGLE_API_KEY = config_data['GOOGLE_API_KEY']

genai.configure(api_key= GOOGLE_API_KEY)

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    # Converting the PDF to image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        
        # convert the image to byte
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": 'image/jpeg',
                'data': base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")

# Streamlit App
st.set_page_config(page_title = 'AI ATS Resume Expert')
st.header('AI ATS Expert')
input_text = st.text_area("Enter you job description:", key = "input")
uploaded_file = st.file_uploader("Upload Your Resume PDF....", type = ['pdf'])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell me about the Resume")

# submit2 = st.button('How Can I Improvise my Skills')

submit3 = st.button("Percentage match")

input_prompt1 = """
    You are an experienced HR with tech experience in the filed of any one job role from Data Science or Full Stack web development or big data engineering or Devops or data analyst, your task is to review the provided resume against the job description for this profiles.
    Please share you professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the strengths and weakness of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science or Full Stack web development or big data engineering or Devops or data analyst and deep ATS functionality or your task is to evaluate the resume against the provided job description. give me the percentage of mathc if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is : ")
        st.write(response)
    else:
        st.write("Please upload the resume")