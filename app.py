# =============================================================
# LAB — AI HR RECRUITMENT ASSISTANT
# =============================================================
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("Groq API Key loaded:", bool(api_key))
from typing import TypedDict, List
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import re
import json


console = Console()
load_dotenv()


# -------------------------------------------------------------
# STEP 1: Connect to Groq cloud model (no local Ollama required)
# -------------------------------------------------------------

def get_llm():
    """Create the hosted chat model only when an AI request is made."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add your Groq API key to the .env file "
            "or your hosting provider's environment variables."
        )

    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        temperature=0,
        api_key=api_key,
        timeout=60,
        max_retries=2,
    )


# -------------------------------------------------------------
# STEP 2: Define the State
# -------------------------------------------------------------

class HRState(TypedDict):

    resume: str
    job_description: str

    resume_skills: List[str]
    job_skills: List[str]

    matching_skills: List[str]
    missing_skills: List[str]

    match_score: float

    retrieved_knowledge: str

    interview_questions: List[str]

    final_answer: str


# -------------------------------------------------------------
# STEP 3: Skill Database
# -------------------------------------------------------------

SKILLS = [

    # Programming
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "typescript",
    "sql",

    # Web
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "django",
    "flask",
    "spring",

    # Data Science
    "machine learning",
    "deep learning",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "statistics",

    # AI
    "artificial intelligence",
    "generative ai",
    "llm",
    "nlp",
    "natural language processing",
    "rag",
    "retrieval augmented generation",
    "prompt engineering",
    "agentic ai",

    # Cloud
    "aws",
    "azure",
    "google cloud",
    "gcp",
    "docker",
    "kubernetes",

    # Database
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "redis",

    # Tools
    "git",
    "github",
    "streamlit",
    "jupyter",

    # Soft skills
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "critical thinking",
    "time management"
]


# -------------------------------------------------------------
# STEP 4: HR Knowledge Base
# -------------------------------------------------------------

HR_KNOWLEDGE = [

    """
    Resume screening should compare candidate qualifications
    with job requirements. Important factors include technical
    skills, relevant experience, education, projects and
    certifications.
    """,

    """
    Skill matching should focus on job-related skills.
    Candidates with a higher percentage of required skills
    generally have a stronger technical match.
    """,

    """
    Relevant projects and internships can demonstrate practical
    experience even when the candidate has limited professional
    experience.
    """,

    """
    Interview questions should be based on the job description
    and the candidate's resume. Questions may cover technical
    knowledge, projects, problem solving and behavioral skills.
    """,

    """
    Recruitment systems should focus on job-related qualifications.
    Personal characteristics that are unrelated to job performance
    should not influence recruitment decisions.
    """,

    """
    AI recruitment systems should support HR professionals rather
    than completely replace human decision making.
    """
]


# -------------------------------------------------------------
# STEP 5: TOOL 1 — Extract Skills
# -------------------------------------------------------------

@tool
def extract_skills(text: str) -> List[str]:
    """
    Extract technical and professional skills from text.
    """

    text_lower = text.lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):

            if skill not in found:
                found.append(skill)

    return sorted(found)


# -------------------------------------------------------------
# STEP 6: TOOL 2 — Match Candidate Skills
# -------------------------------------------------------------

@tool
def match_skills(
    resume_skills: List[str],
    job_skills: List[str]
) -> dict:
    """
    Compare resume skills with job requirements.
    """

    resume_set = set(resume_skills)

    job_set = set(job_skills)

    matching = sorted(
        resume_set.intersection(job_set)
    )

    missing = sorted(
        job_set - resume_set
    )

    if len(job_set) == 0:

        score = 0

    else:

        score = (
            len(matching) /
            len(job_set)
        ) * 100

    return {

        "matching_skills": matching,

        "missing_skills": missing,

        "match_score": round(score, 2)
    }


# -------------------------------------------------------------
# STEP 7: TOOL 3 — HR RAG Retrieval
# -------------------------------------------------------------

@tool
def retrieve_hr_knowledge(query: str) -> str:
    """
    Retrieve relevant HR recruitment guidelines from
    the local knowledge base.
    """

    query_words = set(
        query.lower().split()
    )

    scored_documents = []

    for document in HR_KNOWLEDGE:

        document_words = set(
            document.lower().split()
        )

        overlap = len(
            query_words.intersection(
                document_words
            )
        )

        scored_documents.append(
            (overlap, document)
        )

    scored_documents.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    top_documents = scored_documents[:2]

    result = "\n\n".join(
        document
        for score, document in top_documents
    )

    return result


# -------------------------------------------------------------
# STEP 8: TOOL 4 — Generate Interview Questions
# -------------------------------------------------------------

@tool
def generate_interview_questions(
    matching_skills: List[str],
    missing_skills: List[str]
) -> List[str]:
    """
    Generate interview questions based on candidate
    skills and job requirements.
    """

    questions = []

    # Questions based on matching skills

    for skill in matching_skills[:5]:

        questions.append(
            f"Can you explain your experience with "
            f"{skill} and describe a project where "
            f"you used it?"
        )

    # Questions based on missing skills

    for skill in missing_skills[:3]:

        questions.append(
            f"This role requires {skill}. "
            f"What is your current knowledge of "
            f"{skill}, and how would you improve it?"
        )

    # General questions

    questions.append(
        "Tell me about your most relevant project "
        "for this position."
    )

    questions.append(
        "Describe a difficult technical problem "
        "you faced and how you solved it."
    )

    questions.append(
        "How do you approach learning a new technology?"
    )

    return questions[:10]


# -------------------------------------------------------------
# STEP 9: Resume Analysis Node
# -------------------------------------------------------------

def analyze_resume(state: HRState) -> HRState:
    """
    Extract skills from the candidate resume.
    """

    console.print(
        "[bold cyan]🔍 Analyzing candidate resume...[/bold cyan]"
    )

    result = extract_skills.invoke(
        {
            "text": state["resume"]
        }
    )

    state["resume_skills"] = result

    console.print(
        f"[green]✓ Skills detected: "
        f"{', '.join(result)}[/green]"
    )

    return state


# -------------------------------------------------------------
# STEP 10: Job Description Analysis Node
# -------------------------------------------------------------

def analyze_job(state: HRState) -> HRState:
    """
    Extract required skills from the job description.
    """

    console.print(
        "[bold cyan]💼 Analyzing job description...[/bold cyan]"
    )

    result = extract_skills.invoke(
        {
            "text": state["job_description"]
        }
    )

    state["job_skills"] = result

    console.print(
        f"[green]✓ Required skills: "
        f"{', '.join(result)}[/green]"
    )

    return state


# -------------------------------------------------------------
# STEP 11: Skill Matching Node
# -------------------------------------------------------------

def calculate_match(state: HRState) -> HRState:
    """
    Match candidate skills with job requirements.
    """

    console.print(
        "[bold cyan]📊 Matching candidate with job...[/bold cyan]"
    )

    result = match_skills.invoke(
        {
            "resume_skills": state["resume_skills"],
            "job_skills": state["job_skills"]
        }
    )

    state["matching_skills"] = result[
        "matching_skills"
    ]

    state["missing_skills"] = result[
        "missing_skills"
    ]

    state["match_score"] = result[
        "match_score"
    ]

    console.print(
        f"[bold green]✓ Match Score: "
        f"{state['match_score']}%[/bold green]"
    )

    return state


# -------------------------------------------------------------
# STEP 12: RAG Node
# -------------------------------------------------------------

def retrieve_knowledge(state: HRState) -> HRState:
    """
    Retrieve relevant HR knowledge before final analysis.
    """

    console.print(
        "[bold cyan]📚 Retrieving HR knowledge using RAG...[/bold cyan]"
    )

    query = f"""
    Candidate recruitment evaluation.

    Candidate skills:
    {", ".join(state["resume_skills"])}

    Job requirements:
    {", ".join(state["job_skills"])}

    Matching skills:
    {", ".join(state["matching_skills"])}

    Missing skills:
    {", ".join(state["missing_skills"])}
    """

    result = retrieve_hr_knowledge.invoke(
        {
            "query": query
        }
    )

    state["retrieved_knowledge"] = result

    console.print(
        "[green]✓ Relevant HR knowledge retrieved[/green]"
    )

    return state


# -------------------------------------------------------------
# STEP 13: Interview Question Node
# -------------------------------------------------------------

def create_questions(state: HRState) -> HRState:
    """
    Generate interview questions.
    """

    console.print(
        "[bold cyan]🎤 Generating interview questions...[/bold cyan]"
    )

    result = generate_interview_questions.invoke(
        {
            "matching_skills": state["matching_skills"],
            "missing_skills": state["missing_skills"]
        }
    )

    state["interview_questions"] = result

    console.print(
        f"[green]✓ Generated {len(result)} questions[/green]"
    )

    return state


# -------------------------------------------------------------
# STEP 14: AI Recruitment Agent Node
# -------------------------------------------------------------


def recruitment_agent(state: HRState) -> HRState:
    """
    Generates a simple, structured and professional
    recruitment analysis using the hosted Groq model.
    """

    console.print(
        "[bold cyan]🤖 HR Recruitment Agent is generating "
        "final analysis...[/bold cyan]"
    )

    prompt = f"""
You are a professional AI HR Recruitment Assistant.

Your task is to evaluate a candidate based on the
provided resume and job description.

CANDIDATE RESUME:
{state["resume"]}

JOB DESCRIPTION:
{state["job_description"]}

RESUME SKILLS:
{state["resume_skills"]}

JOB REQUIRED SKILLS:
{state["job_skills"]}

MATCHING SKILLS:
{state["matching_skills"]}

MISSING SKILLS:
{state["missing_skills"]}

SKILL MATCH SCORE:
{state["match_score"]}%

RELEVANT HR KNOWLEDGE:
{state["retrieved_knowledge"]}

Generate the recruitment report using EXACTLY this format:

# CANDIDATE RECRUITMENT REPORT

## 1. Candidate Overview
- Candidate Name:
- Applied Position:
- Education:
- Overall Skill Match: {state["match_score"]}%

## 2. Skills Assessment

### Matching Skills
List the technical skills that match the job description.

### Missing Skills
List the skills that are not found in the resume.

Explain whether these are mandatory or preferred skills
where the job description provides that information.

## 3. Candidate Strengths
Write 4-5 simple bullet points explaining the
candidate's job-related strengths.

## 4. Experience and Projects
Explain relevant internships and projects.
Mention how they relate to the job responsibilities.

## 5. Areas for Improvement
List the technical skills or knowledge areas
the candidate could improve.

## 6. Suggested Technical Interview Questions
Generate 5 questions based on the candidate's
skills, projects and the job requirements.

## 7. Final HR Recommendation

Choose one:
- Recommended for Technical Interview
- Needs Further Review
- Not Recommended

Explain your recommendation in simple English
using 3-4 sentences.

IMPORTANT INSTRUCTIONS:

1. Use simple and understandable English.
2. Use headings and bullet points.
3. Never generate Markdown tables.
4. Never use HTML tags like <br>.
5. Do not write everything in one paragraph.
6. Avoid unnecessary technical jargon.
7. Do not invent candidate qualifications or experience.
8. If information is unavailable, write
   "Not mentioned in the resume".
9. Do not treat preferred skills as mandatory.
10. Do not make hiring decisions based only on
    the match percentage.
11. Focus only on job-related qualifications.
12. Do not use age, gender, religion, race,
    nationality or other unrelated characteristics.
13. This report is decision support and must
    not replace human HR review.
"""


    llm = get_llm()
    result = llm.invoke(prompt)

    state["final_answer"] = result.content

    return state


# -------------------------------------------------------------
# STEP 15: Build LangGraph
# -------------------------------------------------------------

builder = StateGraph(HRState)


builder.add_node(
    "analyze_resume",
    analyze_resume
)

builder.add_node(
    "analyze_job",
    analyze_job
)

builder.add_node(
    "calculate_match",
    calculate_match
)

builder.add_node(
    "retrieve_knowledge",
    retrieve_knowledge
)

builder.add_node(
    "create_questions",
    create_questions
)

builder.add_node(
    "recruitment_agent",
    recruitment_agent
)


# -------------------------------------------------------------
# STEP 16: Define Graph Flow
# -------------------------------------------------------------

builder.set_entry_point(
    "analyze_resume"
)

builder.add_edge(
    "analyze_resume",
    "analyze_job"
)

builder.add_edge(
    "analyze_job",
    "calculate_match"
)

builder.add_edge(
    "calculate_match",
    "retrieve_knowledge"
)

builder.add_edge(
    "retrieve_knowledge",
    "create_questions"
)

builder.add_edge(
    "create_questions",
    "recruitment_agent"
)


# -------------------------------------------------------------
# STEP 17: Finish Point
# -------------------------------------------------------------

builder.set_finish_point(
    "recruitment_agent"
)


# Compile graph

graph = builder.compile()


# -------------------------------------------------------------
# STEP 18: Sample Resume
# -------------------------------------------------------------

sample_resume = """
Abinaya M

Computer Science Engineering Student

Education:
Bachelor of Engineering in Computer Science

Technical Skills:
Python
Java
SQL
Machine Learning
Pandas
NumPy
Streamlit
Git
HTML
CSS

Projects:

AI Resume Screening System:
Developed a recruitment application using Python,
machine learning and Streamlit.

Student Support Chatbot:
Created a chatbot using RAG and natural language
processing.

Skills:
Communication
Teamwork
Problem Solving
"""


# -------------------------------------------------------------
# STEP 19: Sample Job Description
# -------------------------------------------------------------

sample_job = """
Python AI Developer

We are looking for a Python AI Developer.

Requirements:

Python
Machine Learning
SQL
Pandas
NumPy
Git
RAG
LangChain
LangGraph
Generative AI

Preferred:

Streamlit
Flask
Docker

Candidates should have strong communication
and problem solving skills.

The candidate should be able to develop AI-powered
applications and work with modern AI technologies.
"""


# -------------------------------------------------------------
# STEP 20: Display Results
# -------------------------------------------------------------

def display_results(result):

    console.print("\n")

    console.print(
        Panel(
            f"[bold green]{result['match_score']}%[/bold green]",
            title="[bold cyan]Candidate Match Score[/bold cyan]",
            border_style="cyan"
        )
    )


    # ---------------------------------------------------------
    # Skills Table
    # ---------------------------------------------------------

    table = Table(
        title="Candidate Skill Analysis"
    )

    table.add_column(
        "Category",
        style="cyan"
    )

    table.add_column(
        "Skills"
    )


    table.add_row(
        "Resume Skills",
        ", ".join(
            result["resume_skills"]
        )
    )

    table.add_row(
        "Job Requirements",
        ", ".join(
            result["job_skills"]
        )
    )

    table.add_row(
        "Matching Skills",
        ", ".join(
            result["matching_skills"]
        )
    )

    table.add_row(
        "Missing Skills",
        ", ".join(
            result["missing_skills"]
        )
    )


    console.print(table)


    # ---------------------------------------------------------
    # Final AI Analysis
    # ---------------------------------------------------------

    console.print(
        Panel(
            result["final_answer"],
            title="[bold green]🤖 AI Recruitment Analysis[/bold green]",
            border_style="green"
        )
    )


    # ---------------------------------------------------------
    # Interview Questions
    # ---------------------------------------------------------

    questions = "\n".join(
        f"{i}. {question}"
        for i, question
        in enumerate(
            result["interview_questions"],
            start=1
        )
    )


    console.print(
        Panel(
            questions,
            title="[bold yellow]🎤 Interview Questions[/bold yellow]",
            border_style="yellow"
        )
    )


# -------------------------------------------------------------
# STEP 21: Main Program
# -------------------------------------------------------------

if __name__ == "__main__":

    console.print(
        "\n[bold magenta]"
        "================================================="
        "\n"
        "       AI HR RECRUITMENT ASSISTANT"
        "\n"
        "================================================="
        "[/bold magenta]\n"
    )


    console.print(
        "[bold white]Candidate:[/bold white] Abinaya M"
    )

    console.print(
        "[bold white]Position:[/bold white] Python AI Developer\n"
    )


    # ---------------------------------------------------------
    # Run LangGraph
    # ---------------------------------------------------------

    result = graph.invoke({

        "resume": sample_resume,

        "job_description": sample_job,

        "resume_skills": [],

        "job_skills": [],

        "matching_skills": [],

        "missing_skills": [],

        "match_score": 0,

        "retrieved_knowledge": "",

        "interview_questions": [],

        "final_answer": ""
    })


    # ---------------------------------------------------------
    # Display
    # ---------------------------------------------------------

    display_results(result)


    console.print(
        "\n[bold green]"
        "✓ HR Recruitment Agent completed successfully."
        "[/bold green]\n"
    )