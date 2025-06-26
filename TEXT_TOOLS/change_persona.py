# tools/change_persona_tool.py

import torch
from typing import Type
from transformers import pipeline
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class ChangePersonaInput(BaseModel):
    """Input format: 'persona=IIT Professor:::This is the original content.'"""
    text: str = Field(..., description="Input should be in format: 'persona=XYZ:::your content'")

class ChangePersonaTool(BaseTool):
    name: str = "change_persona_tool"
    description: str = "Rewrites text using a specified persona. Format: 'persona=XYZ:::text'"
    args_schema: Type[BaseModel] = ChangePersonaInput

    def _run(self, text: str) -> str:
        if "persona=" not in text or ":::" not in text:
            return "❌ Invalid input format. Use: 'persona=XYZ:::your text here'"

        try:
            persona, input_text = text.split("persona=")[1].split(":::", maxsplit=1)
        except ValueError:
            return "❌ Parsing error. Format must be 'persona=XYZ:::text'"

        model_id = "EleutherAI/gpt-neo-125m"  # much better than 125M
        device = 0 if torch.cuda.is_available() else -1

        try:
            generator = pipeline(
                "text-generation",
                model=model_id,
                device=device
            )

            prompt = (
                f"Rewrite the following paragraph in the style of a {persona.strip()}:\n\n"
                f"{input_text.strip()}\n\n"
                f"Rewritten version:"
            )

            output = generator(
                prompt,
                max_length=min(len(prompt) + 100, 512),  # stay safe with max length
                temperature=0.7,
                num_return_sequences=1
            )
            return output[0]["generated_text"]
        except Exception as e:
            return f"❌ Error during generation: {str(e)}"
