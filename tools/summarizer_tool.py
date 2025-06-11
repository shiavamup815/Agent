from crewai.tools import BaseTool
from pydantic import Field

class SummarizerTool(BaseTool):
    name: str = Field(default="Summarizer", description="Tool to summarize text.")
    description: str = Field(default="Summarizes the provided text using an LLM.")

    def _run(self, text: str) -> str:
        # Replace with real summarization logic
        return f"Summary:\n{text[:200]}..."
