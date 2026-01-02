import streamlit as st
from src.helper import extract_text_from_pdf,ask_groq
from src.job_api import fetch_linkedin_jobs

st.set_page_config(page_title="Real-Time Job Listings", page_icon=":briefcase:", layout="wide")
st.title("Real-Time Job Listings Application System")

st.markdown("Upload your resume and get matched with the latest job listings from LinkedIn in real-time, based on your skills and experience.")
uploaded_file = st.file_uploader("Upload your Resume (PDF format only)", type=["pdf"], key="resume_uploader")

if uploaded_file:
    with st.spinner("Processing your resume and fetching job listings..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        st.success("Resume processed successfully!")
    
    with st.spinner("Summarizing your resume..."):
        prompt = f"Summarize the following resume text to extract key skills and experience:\n\n{resume_text}\n\nProvide a concise summary."
        summary = ask_groq(prompt, max_tokens=500)
        st.success("Resume summarized successfully!")


    with st.spinner("Finding Skill Gaps..."):
        skill_gap_prompt = f"Based on the following resume summary, identify potential skill gaps for a job seeker in the current job market:\n\n{summary}\n\nList the skill gaps."
        skill_gaps = ask_groq(skill_gap_prompt, max_tokens=400)
        st.success("Skill gaps identified successfully!")


    with st.spinner("Creating Future Roadmap..."):
        roadmap_prompt = f"Based on the following resume summary and identified skill gaps, create a future roadmap for the job seeker to enhance their skills and improve employability:\n\nResume Summary:\n{summary}\n\nIdentified Skill Gaps:\n{skill_gaps}\n\nProvide a detailed roadmap."
        future_roadmap = ask_groq(roadmap_prompt, max_tokens=600)
        st.success("Future roadmap created successfully!")

    st.markdown("----")
    st.header("Resume Summary")
    st.markdown(summary)

    st.header("Identified Skill Gaps")
    st.markdown(skill_gaps)

    st.header("Future Roadmap")
    st.markdown(future_roadmap)
    
    st.success("All tasks completed successfully!")

    if st.button("Get Job Listings Based on Resume"):
        job_keywords_prompt = f"Based on the following resume summary, extract key job search keywords:\n\n{summary}\n\nList the keywords."
        job_keywords = ask_groq(job_keywords_prompt, max_tokens=200)

        search_keywords = job_keywords.replace("\n", "").strip()
        st.success(f"Extracted Job Search Keywords: {search_keywords}")

        with st.spinner("Fetching job listings from LinkedIn..."):
            Linkedin_jobs = fetch_linkedin_jobs(search_keywords, rows=50)

        st.markdown("----")
        st.header("LinkedIn Job Listings")
        if not Linkedin_jobs:
            st.warning("No job listings found for the extracted keywords.")
        else:
            for job in Linkedin_jobs:
                st.subheader(job.get("title", "No Title"))
                st.markdown(f"**Company:** {job.get('company', 'N/A')}")
                st.markdown(f"**Location:** {job.get('location', 'N/A')}")
                st.markdown(f"**Posted:** {job.get('postedAt', 'N/A')}")
                st.markdown(f"**Link:** [Apply Here]({job.get('url', '#')})")
                st.markdown("---")
        