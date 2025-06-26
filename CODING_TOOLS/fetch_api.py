import os
import re
import requests
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool

# Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY: {GROQ_API_KEY}")  # Debugging line to check if the key is loaded
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Define the External API Finder Tool
@tool("find_external_apis_tool")
def find_external_apis_tool(code_snippet: str) -> str:
    """Detects and returns all external API URLs being invoked in a given code snippet."""

    # Prompt for LLM
    prompt = f"""
    You are an expert in analyzing source code. Extract and return all external API URLs being called in the given code.

    **Input Code:**
    {code_snippet}
    ```

    **Extracted API URLs:**
    - List all detected API URLs.
    """

    # Send request to Groq API
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "system", "content": "You are a tool that extracts all external API URLs from a given code snippet."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.3
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    # Extract LLM output (No JSON Parsing, Just Text)
    llm_result = response.text.strip() if response.status_code == 200 else f"Error: {response.status_code}, {response.text}"

    # Backup: Detect API URLs using Regex
    url_pattern = re.compile(r'https?://[^\s"\']+')
    regex_result = list(set(url_pattern.findall(code_snippet)))

    # Return combined results
    return f"**LLM Detected URLs:**\n{llm_result}\n\n**Regex Detected URLs:**\n{regex_result}"

