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
@tool("code_perform_fixer_tool")
def code_perform_fixer_tool(code_snippet: str) -> str:
    """Analyzes a code snippet, identifies security issues, and provides a corrected version."""

    prompt = f"""
    You are a performance optimization expert. Analyze the given code snippet for inefficiencies and suggest an optimized version with explanations.

    *Input Code:*
    {code_snippet}

    *Performance Issues Found:*
    - [List all inefficiencies]

    *Optimized Version:*
    [Provide the improved, optimized code]

    *Explanation:*
    - [Explain performance improvements]
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a tool to optimize the given code."},
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
