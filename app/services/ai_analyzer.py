import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


def generate_ai_feedback(resume_text, job_description):

    prompt = f"""
    Analyze this resume against the given job description.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give response in this exact format:

    Professional Summary:
    Write a short professional summary in 3-4 lines.

    Strengths:
    - Point 1
    - Point 2
    - Point 3

    Weaknesses:
    - Point 1
    - Point 2

    Suggestions:
    - Point 1
    - Point 2
    - Point 3

    Keep the response concise, professional, and user friendly.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    content = response.content

    return {
        "summary": content,
        "suggestions": [
            "Add more deployment projects",
            "Improve frontend project descriptions",
            "Mention teamwork and collaboration experience"
        ]
    }