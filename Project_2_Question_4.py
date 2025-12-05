import streamlit as st
import google.generativeai as genai
import PyPDF2
import docx

GENAI_API_KEY = st.secrets["GEMINI_API_KEY"]   
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("Import to AI - Closed Source Version (Gemini)")

question = st.text_input("Enter your Question:")
uploaded_file = st.file_uploader("Upload attachment:")

def extract_text(file):
    if file is None:
        return ""

    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])

    if file.type == "text/plain":
        return file.read().decode("utf-8")

    return ""

if st.button("Run AI"):
    with st.spinner("Analyzing..."):
        context_text = extract_text(uploaded_file)

        # Build prompt
        if context_text and question:
            prompt = (
                "Document context:\n\n"
                f"{context_text}\n\n"
                f"User question: {question}\n\n"
                "Answer the question based only on the document."
            )
        elif context_text:
            prompt = (
                "The following text may contain a question. "
                "Treat it as a question and provide a clear answer:\n\n"
                f"{context_text}"
            )
        else:
            prompt = question

        response = model.generate_content(prompt)

        st.subheader("AI Response:")
        st.write(response.text)