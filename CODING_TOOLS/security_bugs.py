import os
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Define the Code Bug Fixing Tool
@tool("code_secure_fixer_tool")
def code_secure_fixer_tool(code_snippet: str) -> str:
    """Analyzes a code snippet, identifies security issues, and provides a corrected version."""

    prompt = f"""
    You are a security expert. Analyze the given code snippet for security vulnerabilities and provide a secure version with explanations.

    *Input Code:*
    {code_snippet}

    *Security Issues Found:*
    - [List all vulnerabilities]

    *Secure Version:*
    [Provide the corrected secure code]


    *Explanation:*
    - [Explain security fixes]
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a tool to find and fix security vulnerabilities in given code."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    # Ensure correct response handling without JSON formatting
    if response.status_code == 200:
        return response.text.strip()  # No JSON parsing, just plain text output
    else:
        return f"Error: {response.status_code}, {response.text}"

# Create an agent that utilizes the Code Bug Fixing Tool
