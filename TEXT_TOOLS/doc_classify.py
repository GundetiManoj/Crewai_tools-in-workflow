# tools/document_classification_tool.py

from typing import Type
from pydantic import BaseModel, Field
from transformers import pipeline
from crewai.tools import BaseTool
import torch

class DocumentClassificationInput(BaseModel):
    text: str = Field(..., description="Text content of the document to classify.")

class DocumentClassificationTool(BaseTool):
    name: str = "document_classification_tool"
    description: str = (
        "Classifies a document into one of: News, Sports, Finance, Technology, Health, Entertainment "
        "using GPT-Neo-125M via prompt-based generation."
    )
    args_schema: Type[BaseModel] = DocumentClassificationInput

    def _run(self, text: str) -> str:
        try:
            model_id = "openai-community/gpt2"
            device = 0 if torch.cuda.is_available() else -1

            generator = pipeline(
                "text-generation",
                model=model_id,
                device=device
            )

            categories = ["News", "Sports", "Finance", "Technology", "Health", "Entertainment"]
            prompt = (
                "Classify the following document into one of these categories:\n"
                f"{', '.join(categories)}\n\n"
                f"Document:\n{text.strip()}\n\n"
                "Your answer (one category only):"
            )

            response = generator(
                prompt,
                max_length=prompt.count(" ") + 40,  # basic length control
                temperature=0.3,
                num_return_sequences=1
            )

            generated_text = response[0]["generated_text"]
            predicted = self._extract_category(generated_text, categories)
            return f"📄 The document is classified as: **{predicted}**"
        except Exception as e:
            return f"❌ Error during classification: {str(e)}"

    def _extract_category(self, output: str, categories: list) -> str:
        output = output.lower()
        for category in categories:
            if category.lower() in output:
                return category
        return "Unknown"
