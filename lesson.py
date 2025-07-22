import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re
from PyPDF2 import PdfReader

# Load environment variables and API key
load_dotenv()
api_key = os.getenv( "Gemini_Api_key")

# Configure Generative AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Clean and preprocess text: remove extra spaces, lowercase
def clean_text(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

# Extract text from a fixed local PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        reader = PdfReader("yearly year lesson plan by mahwish.pdf")
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    except Exception as e:
        return f"Error reading PDF: {e}"
    return clean_text(text)

# Generate answers using Gemini API
def generate_answers(content, query):
    prompt = f'''
You have the following lesson content from a phonics PDF:
{content}
Answer the question clearly and concisely:
{query}

If the question is about lessons or phonics sounds, focus on explaining those from the content.
'''
    try:
        response = model.generate_content(prompt)
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and candidate.content:
                parts = getattr(candidate.content, 'parts', [])
                if parts and len(parts) > 0:
                    return parts[0].text
                else:
                    return candidate.content.text if hasattr(candidate.content, 'text') else "No answer generated."
        return "No answer generated."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI setup
st.set_page_config(page_title="Kindergarten Syllabus Assistant")

# Header and Description
st.title("📚 Kindergarten Syllabus Assistant")
st.markdown("""
Welcome to the **Kindergarten Syllabus Assistant**! 👶✏️  
This app provides instant answers from a fixed PDF syllabus designed for Kindergarten students.

**Created by Mahwish**, this tool is especially helpful for:
- 🧑‍🏫 Teachers planning their yearly curriculum  
- 👨‍👩‍👧 Parents supporting their child's early learning journey  

Ask any question about the lesson plan below! ⬇️
""")

# Path to your local PDF file (adjust if needed)
PDF_FILE_PATH = r"C:\Users\Computer House\Downloads\yearly year lesson plan by mahwish.pdf"

# Load PDF content once
if 'pdf_content' not in st.session_state:
    st.session_state['pdf_content'] = extract_text_from_pdf(PDF_FILE_PATH)

# Display status
if st.session_state['pdf_content'].startswith("Error"):
    st.error(st.session_state['pdf_content'])
else:
    st.success("PDF content loaded successfully!")

# User input
user_query = st.text_input("Enter your question:")

# Generate answer
if st.button("Generate Answer") and st.session_state['pdf_content']:
    if user_query.strip() == "":
        st.warning("Please enter a question.")
    else:
        answer = generate_answers(st.session_state['pdf_content'], user_query)
        st.subheader("Generated Answer:")
        st.text(answer)

# ----------------------------------------
# 💌 Contact & Credits Section
# ----------------------------------------
st.markdown("---")
st.markdown("""
### 💬 Need More Help?

For custom **worksheets**, **phonics sounds**, or help with your child's learning journey, feel free to reach out! 😊  
I'm happy to help teachers & parents make learning **fun and easy**. 🎉📖

📧 **Email**: [mahwishpy@gmail.com](mailto:mahwishpy@gmail.com)  
🔗 **Facebook**: [Share on Facebook](https://www.facebook.com/share/1BBXjgbXPS/)  
🔗 **LinkedIn**: [Mahwish Kiran on LinkedIn](https://www.linkedin.com/in/mahwish-kiran-842945353)

_🧠 Made with care by Mahwish – because every little learner deserves the best start! 🌈_
""")
