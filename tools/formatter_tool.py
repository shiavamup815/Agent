from crewai.tools import BaseTool
from pydantic import Field

class FormatterTool(BaseTool):
    name: str = Field(default="Formatter", description="Formats text for clarity.")
    description: str = Field(default="Formats the summary into markdown or readable format.")

    def _run(self, text: str) -> str:
        return f"### Formatted Output\n\n{text}"
