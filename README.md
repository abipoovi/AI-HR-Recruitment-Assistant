# AI HR Recruitment Assistant

An Agentic AI screening system built for the IBM Internship Project that evaluates resumes against job descriptions, identifies skill alignments, retrieves recruitment policies via RAG, and generates targeted interview questions.

---

## 📌 Project Overview

The system automates preliminary candidate screening by taking four primary inputs:

* Candidate Name
* Target Job Position
* Candidate Resume
* Job Description

It runs automated evaluations using **Python**, **LangChain**, **LangGraph**, **Groq LLM**, **RAG**, and **Flask** to output match metrics, skill gap analyses, and tailored interview questions.

---

## 🎯 Key Objectives

1. Automate resume-to-job matching and scoring.
2. Identify core technical strengths and missing skill sets.
3. Retrieve standard recruitment guidelines using a local RAG pipeline.
4. Generate behavioral and technical interview questions based on candidate profile gaps.
5. Provide data-driven screening recommendations to support HR hiring decisions.

---

## 🧠 Agentic Architecture

* **Recruitment Agent:** Powered by a Groq-hosted LLM to synthesize tool outputs into a final evaluation report.
* **Core Tools:**
* `extract_skills()`: Parses key competencies from raw text.
* `match_skills()`: Compares resume competencies against job prerequisites.
* `retrieve_hr_knowledge()`: Fetches hiring benchmarks and role criteria via RAG.
* `generate_interview_questions()`: Formulates skill-gap and project-based questions.


* **Orchestration:** Built with **LangGraph** to manage state and tool execution.

---

## 📊 Sample Screening Report

**Candidate:** Abinaya M

**Position:** Python AI Developer

**Match Score:** **76.92%**

### Skill Breakdown

| Category | Skills Identified |
| --- | --- |
| **Resume Skills** | Communication, CSS, Git, HTML, Java, Machine Learning, NumPy, Pandas, Problem Solving, Python, RAG, SQL, Streamlit, Teamwork |
| **Job Requirements** | Communication, Docker, Flask, Generative AI, Git, Machine Learning, NumPy, Pandas, Problem Solving, Python, RAG, SQL, Streamlit |
| **Matching Skills** | Communication, Git, Machine Learning, NumPy, Pandas, Problem Solving, Python, RAG, SQL, Streamlit |
| **Missing Skills** | Docker, Flask, Generative AI |

---

### AI Evaluation & Recommendations

* **Suitability:** **High**. Strong alignment with foundational data science and core AI tooling. Projects (AI Resume Screener, RAG Support Chatbot) directly validate applied proficiency.
* **Strengths:** 100% coverage of core programming and data handling requirements (Python, SQL, NumPy, Pandas) and demonstrated practical RAG implementation.
* **Skill Gaps:** Lacks demonstrated production/deployment tools (**Docker**, **Flask**) and deeper end-to-end **Generative AI** workflows (fine-tuning, prompt orchestration beyond basic RAG).
* **Final Verdict:** **Shortlist for Interview**. Missing web/container frameworks are quickly trainable given the candidate's existing foundational skills.

---

### Generated Interview Questions

1. **Machine Learning:** Can you walk through the model selection and evaluation pipeline used in your AI Resume Screening project?
2. **RAG Architecture:** In your Student Support Chatbot, how did you handle chunking strategies, embeddings, and context retrieval latency?
3. **Skill Gap — Docker:** What is your familiarity with containerization, and how would you go about containerizing an AI API for production?
4. **Skill Gap — Flask / APIs:** How would you design a RESTful Flask endpoint to serve model predictions to a web client?
5. **Skill Gap — Generative AI:** Beyond retrieval pipelines, what techniques do you use to mitigate LLM hallucinations and manage prompt context windows?
6. **Problem Solving:** Describe a critical debugging issue you encountered when working with large data matrices in NumPy/Pandas and how you resolved it.