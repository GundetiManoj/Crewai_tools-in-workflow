from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os
import requests

class SummarizationTool(BaseTool):  
    # Define required fields
    name: str = "SummarizationTool"  
    description: str = "A tool to summarize text using a large language model."
    api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY"))
    model: str = "llama-3.1-8b-instant"
    base_url: str = "https://api.groq.com/openai/v1/chat/completions"
    
    def _run(self, text: str, max_words: int = 50) -> str:
        """
        Summarize the given text using the summarization API.
        
        This method implements the abstract '_run' method.
        
        Args:
            text (str): Text to be summarized
            max_words (int, optional): Maximum number of words in summary
        
        Returns:
            str: Summarized text
        """
        try:
            # Validate input
            if not text or not isinstance(text, str):
                return "Error: Invalid input. Please provide a non-empty string."
            
            # Construct prompt for summarization
            prompt = f"""
            Summarize the following text concisely, capturing the most important points:
            
            TEXT:
            {text}
            
            Guidelines:
            - Preserve the main ideas and key insights
            - Be extremely concise
            - Limit the summary to approximately {max_words} words
            - Focus on the core message of the text
            """
            
            # Prepare API request payload
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant skilled in creating concise summaries."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 150  # Adjust based on max_words
            }
            
            # Make API call
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            # Check response
            response.raise_for_status()
            
            # Extract summary
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            
            return summary
        
        except requests.RequestException as e:
            return f"API Request Error: {str(e)}"
        except Exception as e:
            return f"Summarization error: {str(e)}"
    