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

            response = requests.post(
                "http://127.0.0.1:8000/upload",
                files=files
            )

            if response.status_code == 200:

                data = response.json()["extracted_data"]

                st.divider()

                # CANDIDATE INFO
                st.header("👤 Candidate Information")

                # NAME
                st.subheader("Name")
                st.success(
                    data.get("name", "Not Found")
                )

                # EMAIL
                st.subheader("Email")
                st.info(
                    data.get("email", "Not Found")
                )

                # PHONE
                st.subheader("Phone")
                st.info(
                    data.get("phone", "Not Found")
                )

                # ATS SCORE
                st.subheader("📊 ATS Score")

                ats = data.get(
                    "ats_score",
                    "0"
                )

                st.metric(
                    label="ATS Resume Score",
                    value=f"{ats}/100"
                )

                # SUMMARY
                st.subheader("📝 Resume Summary")

                st.write(
                    data.get(
                        "summary",
                        "No summary available"
                    )
                )

                # MISSING SKILLS
                st.subheader("❌ Missing Skills")

                missing = data.get(
                    "missing_skills",
                    []
                )

                if missing:

                    for skill in missing:
                        st.markdown(f"- {skill}")

                else:
                    st.write(
                        "No missing skills found"
                    )

                # SKILLS
                st.subheader("🛠 Skills")

                skills = data.get(
                    "skills",
                    []
                )

                if skills:

                    for skill in skills:
                        st.markdown(f"- {skill}")

                else:
                    st.write("No skills found")

                # EDUCATION
                st.subheader("🎓 Education")

                education = data.get(
                    "education",
                    []
                )

                if education:

                    for edu in education:

                        st.markdown(f"""
### {edu.get("degree", "")}

🏫 **Institution:** {edu.get("institution", "")}

📅 **Years:** {edu.get("years", "")}

📌 **Details:** {edu.get("details", "")}
""")

                        st.divider()

                else:
                    st.write(
                        "No education data found"
                    )

                # EXPERIENCE
                st.subheader("💼 Experience")

                experience = data.get(
                    "experience",
                    []
                )

                if experience:

                    for exp in experience:

                        st.markdown(f"""
### {exp.get("title", "")}

🏢 **Company:** {exp.get("company", "")}

📅 **Duration:** {exp.get("years", "")}
""")

                        descriptions = exp.get(
                            "description",
                            []
                        )

                        if isinstance(
                            descriptions,
                            str
                        ):

                            st.markdown(
                                descriptions
                            )

                        else:

                            for d in descriptions:
                                st.markdown(f"- {d}")

                        st.divider()

                else:
                    st.write(
                        "No experience found"
                    )

                # PROJECTS
                st.subheader("🚀 Projects")

                projects = data.get(
                    "projects",
                    []
                )

                if projects:

                    for project in projects:

                        st.markdown(f"""
### {project.get("title", "")}
""")

                        descriptions = project.get(
                            "description",
                            []
                        )

                        if isinstance(
                            descriptions,
                            str
                        ):

                            st.markdown(
                                descriptions
                            )

                        else:

                            for d in descriptions:
                                st.markdown(f"- {d}")

                        st.divider()

                else:
                    st.write(
                        "No projects found"
                    )

                # DOWNLOAD BUTTON
                st.download_button(
                    label="⬇ Download Extracted JSON",
                    data=response.text,
                    file_name="resume_data.json",
                    mime="application/json"
                )

            else:

                st.error(
                    "Something went wrong while analyzing the resume."
                )