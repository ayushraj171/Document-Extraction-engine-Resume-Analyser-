import streamlit as st

st.title("📄 AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

def process_file(file):
    content = file.read()
    return {
        "file_name": file.name,
        "file_size": len(content),
        "status": "processed successfully"
    }

if uploaded_file:
    st.success("Uploaded ✅")

    if st.button("Analyze Resume"):
        result = process_file(uploaded_file)
        st.json(result)
