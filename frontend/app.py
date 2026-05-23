import streamlit as st
import requests

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume & analyze it using Gemini AI.")

uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])

# 🔥 CHANGE ONLY THIS LINE AFTER DEPLOYMENT
API_URL = "https://YOUR-BACKEND-URL/upload"

if uploaded_file is not None:

    st.success("Resume uploaded successfully ✅")

    if st.button("Analyze Resume"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:
            response = requests.post(API_URL, files=files, timeout=60)

            if response.status_code == 200:

                data = response.json().get("extracted_data", {})

                st.header("👤 Candidate Information")

                st.success(data.get("name", "Not Found"))
                st.info(data.get("email", "Not Found"))
                st.info(data.get("phone", "Not Found"))

                st.metric("ATS Score", f"{data.get('ats_score', 0)}/100")

                st.subheader("📝 Summary")
                st.write(data.get("summary", ""))

                st.subheader("🛠 Skills")
                st.write(", ".join(data.get("skills", [])))

                st.subheader("❌ Missing Skills")
                st.write(", ".join(data.get("missing_skills", [])))

            else:
                st.error("Backend Error")
                st.write(response.text)

        except Exception as e:
            st.error("❌ Backend connection failed")
            st.code(str(e))
