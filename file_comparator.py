import streamlit as st
import pandas as pd
from difflib import ndiff
import docx
import PyPDF2
from pdfminer.high_level import extract_text

def read_pdf(file):
    try:
        return extract_text(file)
    except Exception as e:
        return f"Error reading PDF: {e}"

def compare_texts(text1, text2):
    diff = list(ndiff(text1.splitlines(), text2.splitlines()))
    return "\n".join(diff)

def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def compare_excels(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    try:
        comparison = df1.compare(df2, align_axis=0)
        return comparison
    except:
        return "Excel files are completely different or uncomparable."

st.title("📁 File Comparator Tool")

file_type = st.radio("Select File Type to Compare", ["Word (.docx)", "PDF (.pdf)", "Excel (.xlsx)"])

file1 = st.file_uploader("Upload First File", type=["docx", "pdf", "xlsx"])
file2 = st.file_uploader("Upload Second File", type=["docx", "pdf", "xlsx"])

if file1 and file2:
    st.markdown("### 🧠 Differences")

    if file_type == "Word (.docx)":
        text1 = read_docx(file1)
        text2 = read_docx(file2)
        result = compare_texts(text1, text2)
        st.text_area("Difference", value=result, height=400)

    elif file_type == "PDF (.pdf)":
        text1 = read_pdf(file1)
        text2 = read_pdf(file2)
        result = compare_texts(text1, text2)
        st.text_area("Difference", value=result, height=400)

    elif file_type == "Excel (.xlsx)":
        result = compare_excels(file1, file2)
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        else:
            st.warning(result)
