import streamlit as st
import requests

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume & analyze it using Gemini AI.")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# ⚠️ CHANGE THIS when deploying backend
API_URL = "http://127.0.0.1:8000/upload"

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

        with st.spinner("AI is analyzing resume..."):

            try:
                response = requests.post(API_URL, files=files, timeout=60)

                if response.status_code == 200:

                    data = response.json().get("extracted_data", {})

                    st.divider()
                    st.header("👤 Candidate Information")

                    st.subheader("Name")
                    st.success(data.get("name", "Not Found"))

                    st.subheader("Email")
                    st.info(data.get("email", "Not Found"))

                    st.subheader("Phone")
                    st.info(data.get("phone", "Not Found"))

                    st.subheader("📊 ATS Score")
                    st.metric("ATS Resume Score", f"{data.get('ats_score', 0)}/100")

                    st.subheader("📝 Resume Summary")
                    st.write(data.get("summary", "No summary available"))

                    # ---------------- SKILLS ----------------
                    st.subheader("🛠 Skills")
                    skills = data.get("skills", [])
                    if isinstance(skills, list):
                        st.write(", ".join(skills))
                    else:
                        st.write(skills)

                    # ---------------- MISSING SKILLS ----------------
                    st.subheader("❌ Missing Skills")
                    st.write(", ".join(data.get("missing_skills", [])))

                    # ---------------- EDUCATION ----------------
                    st.subheader("🎓 Education")
                    for edu in data.get("education", []):
                        st.markdown(f"""
- **{edu.get('degree')}**
  - {edu.get('institution')}
  - {edu.get('years')}
  - {edu.get('details')}
""")

                    # ---------------- EXPERIENCE ----------------
                    st.subheader("💼 Experience")
                    for exp in data.get("experience", []):
                        st.markdown(f"""
- **{exp.get('title')}** at **{exp.get('organization')}**
  - {exp.get('dates')}
  - {exp.get('description')}
""")

                    # ---------------- PROJECTS ----------------
                    st.subheader("🚀 Projects")
                    for proj in data.get("projects", []):
                        st.markdown(f"""
- **{proj.get('title')}**
  - {proj.get('description')}
""")

                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.write(response.text)

            except Exception as e:
                st.error("❌ Backend connection failed")
                st.code(str(e))
