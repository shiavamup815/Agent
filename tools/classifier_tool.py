from crewai.tools import BaseTool
from pydantic import Field
from crewai import LLM

class ClassifierTool(BaseTool):
    name: str = Field(default="Classifier", description="LLM-powered domain classifier")
    description: str = Field(default="Uses LLM to classify the document into hospital, academic, or HR")

    def _run(self, text: str) -> str:
        # Load LLM
        llm = LLM(model="gemini/gemini-2.0-flash", provider="google")

        prompt = (
            "You are a domain classification assistant.\n"
            "Classify the domain of the following document into one of these categories:\n"
            "- hospital\n"
            "- academic\n"
            "- HR\n"
            "If it does not fit any, return 'unknown'.\n\n"
            f"Document:\n{text[:3000]}\n\n" 
            "Respond with only one word: hospital, academic, HR, or unknown."
        )

        try:
            response = llm.call(prompt)
            cleaned_response = response.lower()
            return cleaned_response
        except Exception as e:
            return f"unknown (LLM error: {str(e)})"
